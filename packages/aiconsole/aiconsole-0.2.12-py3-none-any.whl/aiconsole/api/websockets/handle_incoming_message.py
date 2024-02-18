# The AIConsole Project
#
# Copyright 2023 10Clouds
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import logging
from collections import defaultdict
from typing import Any, Callable, cast
from uuid import uuid4

from aiconsole.api.websockets.client_messages import (
    AcceptCodeClientMessage,
    AcquireLockClientMessage,
    CloseChatClientMessage,
    InitChatMutationClientMessage,
    OpenChatClientMessage,
    ProcessChatClientMessage,
    ReleaseLockClientMessage,
    StopChatClientMessage,
)
from aiconsole.api.websockets.connection_manager import (
    AcquiredLock,
    AICConnection,
    connection_manager,
)
from aiconsole.api.websockets.do_process_chat import do_process_chat
from aiconsole.api.websockets.render_materials_from_message_group import (
    render_materials_from_message_group,
)
from aiconsole.api.websockets.server_messages import (
    ChatOpenedServerMessage,
    NotificationServerMessage,
    ResponseServerMessage,
)
from aiconsole.core.assets.agents.agent import AICAgent
from aiconsole.core.chat.execution_modes.utils.import_and_validate_execution_mode import (
    import_and_validate_execution_mode,
)
from aiconsole.core.chat.locking import DefaultChatMutator, acquire_lock, release_lock
from aiconsole.core.code_running.run_code import reset_code_interpreters
from aiconsole.core.code_running.virtual_env.create_dedicated_venv import (
    WaitForEnvEvent,
)
from aiconsole.core.project import project
from aiconsole.utils.events import internal_events

_log = logging.getLogger(__name__)

_running_tasks: dict[str, dict[str, asyncio.Task]] = defaultdict(dict)


async def handle_incoming_message(connection: AICConnection, json: dict):
    message_type = json["type"]

    handlers = {
        AcquireLockClientMessage.__name__: _handle_acquire_lock_ws_message,
        ReleaseLockClientMessage.__name__: _handle_release_lock_ws_message,
        OpenChatClientMessage.__name__: _handle_open_chat_ws_message,
        StopChatClientMessage.__name__: _handle_stop_chat_ws_message,
        CloseChatClientMessage.__name__: _handle_close_chat_ws_message,
        InitChatMutationClientMessage.__name__: _handle_init_chat_mutation_ws_message,
        AcceptCodeClientMessage.__name__: _handle_accept_code_ws_message,
        ProcessChatClientMessage.__name__: _handle_process_chat_ws_message,
    }

    handler = handlers[message_type]

    _log.info(f"Handling message {message_type}")

    task_id = str(uuid4())
    task = asyncio.create_task(handler(connection, json))
    _running_tasks[json["chat_id"]][task_id] = task
    task.add_done_callback(_get_done_callback(json["chat_id"], task_id))


async def _handle_acquire_lock_ws_message(connection: AICConnection, json: dict):
    message: AcquireLockClientMessage | None = None
    try:
        message = AcquireLockClientMessage(**json)
        await acquire_lock(chat_id=message.chat_id, request_id=message.request_id)

        connection.acquired_locks.append(
            AcquiredLock(
                chat_id=message.chat_id,
                request_id=message.request_id,
            )
        )

        _log.info(f"Acquired lock {message.request_id} {connection.acquired_locks}")
        await connection.send(
            ResponseServerMessage(request_id=message.request_id, payload={"chat_id": message.chat_id}, is_error=False)
        )
    except Exception:
        if message is not None:
            await connection.send(
                ResponseServerMessage(
                    request_id=message.request_id,
                    payload={"error": "Error during acquiring lock", "chat_id": message.chat_id},
                    is_error=True,
                )
            )


async def _handle_release_lock_ws_message(connection: AICConnection, json: dict):
    message = ReleaseLockClientMessage(**json)
    await release_lock(chat_id=message.chat_id, request_id=message.request_id)

    lock_data = AcquiredLock(chat_id=message.chat_id, request_id=message.request_id)

    if lock_data in connection.acquired_locks:
        connection.acquired_locks.remove(lock_data)
    else:
        _log.error(f"Lock {lock_data} not found in {connection.acquired_locks}")


async def _handle_open_chat_ws_message(connection: AICConnection, json: dict):
    message = OpenChatClientMessage(**json)
    temporary_request_id = str(uuid4())

    try:
        connection.open_chats_ids.add(message.chat_id)

        chat = await acquire_lock(
            chat_id=message.chat_id,
            request_id=temporary_request_id,
            skip_mutating_clients=True,  # Skip because they do not yet have the chat
        )

        if message.chat_id in connection.open_chats_ids:
            await connection.send(
                ResponseServerMessage(
                    request_id=message.request_id, payload={"chat_id": message.chat_id}, is_error=False
                )
            )

            await connection.send(
                ChatOpenedServerMessage(
                    chat=chat,
                )
            )
    except Exception:
        await connection.send(
            ResponseServerMessage(
                request_id=message.request_id,
                payload={"error": "Error during opening chat", "chat_id": message.chat_id},
                is_error=True,
            )
        )
    finally:
        await release_lock(chat_id=message.chat_id, request_id=temporary_request_id)


async def _handle_stop_chat_ws_message(connection: AICConnection, json: dict):
    message: StopChatClientMessage | None = None
    try:
        message = StopChatClientMessage(**json)
        reset_code_interpreters(chat_id=message.chat_id)
        for task in _running_tasks[message.chat_id].values():
            task.cancel()
        await connection.send(
            ResponseServerMessage(request_id=message.request_id, payload={"chat_id": message.chat_id}, is_error=False)
        )
    except Exception:
        if message is not None:
            await connection.send(
                ResponseServerMessage(
                    request_id=message.request_id,
                    payload={"error": "Error during closing chat", "chat_id": message.chat_id},
                    is_error=True,
                )
            )


async def _handle_close_chat_ws_message(connection: AICConnection, json: dict):
    message = CloseChatClientMessage(**json)
    connection.open_chats_ids.discard(message.chat_id)


async def _handle_init_chat_mutation_ws_message(connection: AICConnection | None, json: dict):
    message = InitChatMutationClientMessage(**json)
    mutator = DefaultChatMutator(chat_id=message.chat_id, request_id=message.request_id, connection=connection)

    await mutator.mutate(message.mutation)


async def _handle_accept_code_ws_message(connection: AICConnection, json: dict):
    message = AcceptCodeClientMessage(**json)

    async def _notify(event):
        await connection_manager().send_to_chat(
            NotificationServerMessage(title="Wait", message="Environment is still being created"),
            message.chat_id,
        )

    try:
        chat = await acquire_lock(chat_id=message.chat_id, request_id=message.request_id)

        internal_events().subscribe(
            WaitForEnvEvent,
            _notify,
        )

        chat_mutator = DefaultChatMutator(
            chat_id=message.chat_id,
            request_id=message.request_id,
            connection=None,  # Source connection is None because the originating mutations come from server
        )

        tool_call_location = chat.get_tool_call_location(message.tool_call_id)

        if tool_call_location is None:
            raise Exception(f"Tool call with id {message.tool_call_id} not found")

        agent_id = tool_call_location.message_group.actor_id.id

        agent = project.get_project_agents().get_asset(agent_id)

        if agent is None:
            raise Exception(f"Agent with id {agent_id} not found")

        agent = cast(AICAgent, agent)

        execution_mode = await import_and_validate_execution_mode(agent)

        mats = await render_materials_from_message_group(tool_call_location.message_group, chat_mutator.chat, agent)

        await execution_mode.accept_code(
            chat_mutator=chat_mutator,
            agent=agent,
            materials=mats.materials,
            rendered_materials=mats.rendered_materials,
            tool_call_id=tool_call_location.tool_call.id,
        )
    finally:
        await release_lock(chat_id=message.chat_id, request_id=message.request_id)


async def _handle_process_chat_ws_message(connection: AICConnection, json: dict):
    message = ProcessChatClientMessage(**json)
    try:
        await acquire_lock(chat_id=message.chat_id, request_id=message.request_id)

        chat_mutator = DefaultChatMutator(
            chat_id=message.chat_id,
            request_id=message.request_id,
            connection=None,  # Source connection is None because the originating mutations come from server
        )

        await do_process_chat(chat_mutator)
    finally:
        await release_lock(chat_id=message.chat_id, request_id=message.request_id)


def _get_done_callback(chat_id: str, task_id: str) -> Callable:
    def remove_running_task(_: Any) -> None:
        del _running_tasks[chat_id][task_id]

    return remove_running_task
