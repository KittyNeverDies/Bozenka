import os
import logging
import g4f
from aiogram import Dispatcher, Bot
from sqlalchemy.ext.asyncio import async_sessionmaker

from bozenka.telegram.cmds import register_handlers


async def launch_telegram_instance(session_maker: async_sessionmaker) -> None:
    """
    Launches telegram bot with token from enviroment
    :return:
    """
    logging.basicConfig(level=logging.INFO)
    logging.log(msg="Setting up logging!", level=logging.INFO)
    g4f.logging = True

    bot = Bot(token=os.getenv("tg_bot_token"), parse_mode="HTML")
    dp = Dispatcher(bot=bot, session_maker=session_maker)
    await dp.start_polling(on_startup=[register_handlers(dp)])
