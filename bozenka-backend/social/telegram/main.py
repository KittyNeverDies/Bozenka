import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties



async def launch_telegram_bot_instance(features: dict[str: list]) -> None:
    """
    Launches telegram bot instance for bozenka platform
    :param features: List of features, that instance should have to register
    :return: Nothing
    """

    # Dispatcher from aiogram, look into their documentation for more information
    dp = Dispatcher()

    # Handler registration mapping
    handler_mapping = {
        'message': dp.message,
        'callback_query': dp.callback_query,
        'channel_post': dp.channel_post,
        'edited_channel_post': dp.edited_channel_post,
        'poll': dp.poll,
        'chat_join_request': dp.chat_join_request,
        'chat_boost': dp.chat_boost,
    }

    @dp.message()
    async def echo_handler(message) -> None:
        """
        Handler will forward receive a message back to the sender
        By default, message handler will handle all message types (like a text, photo, sticker etc.)
        """
        try:
            # Send a copy of the received message
            await message.send_copy(chat_id=message.chat.id)
        except TypeError:
            # But not all the types is supported to be copied so need to handle it
            await message.answer("Nice try!")

    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=os.getenv("TELEGRAM_TOKEN"), default=DefaultBotProperties())

    # Initializing all handlers, written for telegram
    # Register handlers from all features
    for feature_list in features.values():
        for feature in feature_list:
            # Skip if telegram platform not available
            if 'telegram' not in feature.platforms_available:
                continue

            # Get telegram handlers
            telegram_handlers = feature.platforms_available['telegram']['handlers']

            # Register each handler type
            for event_type, handlers in telegram_handlers.items():
                if not handlers:  # Skip empty handler lists
                    continue

                register_method = handler_mapping.get(event_type)
                if register_method:
                    for handler_config in handlers:
                        handler_func, filters = handler_config
                        register_method.register(
                            callback=handler_func,
                            *filters
                        )


    # And the run events dispatching
    await dp.start_polling(bot)
