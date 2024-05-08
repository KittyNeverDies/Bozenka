import logging
import os

from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand
from sqlalchemy.ext.asyncio import async_sessionmaker

from bozenka.instances.basic_features_list import basic_features
from bozenka.instances.customizable_features_list import customizable_features
from bozenka.instances.telegram.queries import *
from bozenka.generative.generative_categories import register_all_categories


async def register_all_features(list_of_features: list, dispatcher: Dispatcher, bot: Bot) -> None:
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
            logging.log(msg=f"{feature}", level=logging.INFO)
            logging.log(msg=f"{message_handler}", level=logging.INFO)
            dispatcher.message.register(message_handler[0], *message_handler[1])

        for callback_query_handler in feature.telegram_callback_handlers:
            dispatcher.callback_query.register(callback_query_handler[0], *callback_query_handler[1])

    if not (commands := await bot.get_my_commands()):
        await bot.set_my_commands(cmd_list)
    else:
        for cmd in cmd_list:
            commands.append(cmd)
        await bot.set_my_commands(commands)


async def launch_telegram_instance(session_maker: async_sessionmaker) -> None:
    """
    Launch bozenka telegram instance with token from enviroment
    :param session_maker: AsyncSessionMaker SqlAlchemy object
    :return: None
    """
    logging.log(msg="-" * 50 + "TELEGRAM BOZENKA INSTANCE LAUNCH" + "-" * 50, level=logging.INFO)

    bot = Bot(token=os.getenv("tg_bot_token"), parse_mode="HTML")

    dp = Dispatcher()

    await bot.delete_my_commands()

    # Registering other handlers
    dp.callback_query.register(delete_callback_handler, DeleteMenu.filter())
    dp.callback_query.register(hide_menu_handler, HideMenu.filter())

    await dp.start_polling(bot,
                           session_maker=session_maker,     # Pass your async_sessionmaker here, you can do dependency injection
                           on_startup=[
                               await register_all_features(list_of_features=customizable_features, dispatcher=dp, bot=bot),
                               await register_all_features(list_of_features=basic_features, dispatcher=dp, bot=bot),
                               await register_all_categories(dp=dp, telegram_bot=bot),

                           ])
