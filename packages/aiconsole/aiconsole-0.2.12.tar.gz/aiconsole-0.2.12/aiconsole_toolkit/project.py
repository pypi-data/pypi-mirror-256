from typing import cast

from aiconsole.core.assets.agents.agent import AICAgent
from aiconsole.core.assets.load_all_assets import load_all_assets
from aiconsole.core.assets.materials.material import Material
from aiconsole.core.assets.types import AssetType


async def get_all_agents() -> list[AICAgent]:
    lists = (await load_all_assets(AssetType.AGENT)).values()
    return cast(list[AICAgent], (list[0] for list in lists))


async def get_all_materials() -> list[Material]:
    lists = (await load_all_assets(AssetType.MATERIAL)).values()
    return cast(list[Material], (list[0] for list in lists))
