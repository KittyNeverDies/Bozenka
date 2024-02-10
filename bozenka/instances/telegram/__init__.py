import os
import logging
import g4f
from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand
from sqlalchemy.ext.asyncio import async_sessionmaker

from bozenka.features import BasicFeature
from bozenka.features.features_list import features_list
from bozenka.features.admin import *
from bozenka.features.basic import *
from bozenka.features.user import *
from bozenka.instances.telegram.handlers import register_handlers
from bozenka.instances.telegram.utils.simpler import list_of_commands


async def register_all_features(list_of_features: list[BasicFeature], dispatcher: Dispatcher, bot: Bot) -> None:
    """
    Registers all features / handlers avaible in bozenka
    :param list_of_features: List of features
    :param dispatcher: Dispatcher aiogram class
    :param bot: Bot aiogram class
    :return: None
    """
    cmd_list = []
    for feature in list_of_features:

        if feature.telegram_cmd_avaible:
            for command, description in feature.telegram_commands.items():
                cmd_list.append(BotCommand(command=command, description=description))

        for message_handler in feature.telegram_message_handlers:
            dispatcher.message.register(message_handler[0], *message_handler[1])

        for callback_query_handler in feature.telegram_callback_handlers:
            dispatcher.callback_query.register(callback_query_handler[0], *callback_query_handler[1])

    await bot.set_my_commands(cmd_list)


async def launch_telegram_instance(session_maker: async_sessionmaker) -> None:
    """
    Launches telegram bot with token from enviroment
    :param session_maker:
    :return:
    """
    logging.log(msg="-" * 50 + "TELEGRAM INSTANCE LAUNCH" + "-" * 50, level=logging.INFO)

    bot = Bot(token=os.getenv("tg_bot_token"), parse_mode="HTML")

    dp = Dispatcher()

    await register_all_features(list_of_features=features_list, dispatcher=dp, bot=bot)
    await dp.start_polling(bot, session_maker=session_maker, on_startup=[])
