# social/vkontakte/main.py
import asyncio
import logging
import os
from vkbottle import Bot, LoopWrapper
from vkbottle.user import Message


async def launch_vk_bot_instance(features: dict[str: list]) -> None:
    """
    Launches vkontakte bot instance
    for bozenka platform
    :return: Nothing
    """



    loop = asyncio.get_running_loop()  # Use get_running_loop()
    loop_wrapper = LoopWrapper(loop=loop)
    bot = Bot(token=os.getenv('VK_TOKEN'), loop_wrapper=loop_wrapper)

    handler_mapping = {
        "private_message": bot.on.private_message,
        "message": bot.on.message,
        "group": bot.on.chat_message
    }

    # Initializing all handlers, written for telegram
    # Register handlers from all features
    for feature_list in features.values():
        for feature in feature_list:
            # Skip if telegram platform not available
            if 'vkontakte' not in feature.platforms_available:
                continue


            # Get telegram handlers
            vk_handlers = feature.platforms_available['vkontakte']['handlers']

            # Register each handler type
            for event_type, handlers in vk_handlers.items():
                if not handlers:  # Skip empty handler lists
                    continue
                register_method = handler_mapping.get(event_type)
                if register_method:
                    for handler_config in handlers:
                        handler_func, filters = handler_config
                        print(handler_func, filters)
                        register_method(*filters)(handler_func) # type: ignore


    # Don't use run_forever(). Use run_polling() in an async context.
    await bot.run_polling()