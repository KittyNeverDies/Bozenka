import asyncio
import logging
import sys

from features import get_list_of_features

from social.dsc import launch_discord_bot_instance
from social.vkontakte import launch_vk_bot_instance
from social.telegram import launch_telegram_bot_instance

async def launch_instances() -> None:
    """
    Launch all instances of bozenka bots
    in parallel
    :return: Nothing to return
    """
    features = get_list_of_features()

    discord_task = asyncio.create_task(launch_discord_bot_instance(features))
    vk_task = asyncio.create_task(launch_vk_bot_instance(features))
    telegram_task = asyncio.create_task(launch_telegram_bot_instance(features))

    await asyncio.wait([telegram_task, vk_task, discord_task])


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        stream=sys.stdout
                        )
    asyncio.run(launch_instances())