import asyncio

from .discord import launch_discord_bot_instance
from .vk import launch_vk_bot_instance
from .telegram import launch_telegram_bot_instance

async def launch_instances() -> None:
    """
    Launching all bot instances of Bozenka platform
    in parallel
    :return: Nothing
    """
    await asyncio.gather(
        launch_discord_bot_instance(),
        launch_vk_bot_instance(),
        launch_telegram_bot_instance()
    )