import os
import logging
import g4f
from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand
from sqlalchemy.ext.asyncio import async_sessionmaker

from bozenka.instances.telegram.cmds import register_handlers
from bozenka.instances.telegram.utils.simpler import list_of_commands


async def launch_telegram_instance(session_maker: async_sessionmaker) -> None:
    """
    Launches telegram bot with token from enviroment
    :return:
    """
    logging.basicConfig(level=logging.INFO)
    logging.log(msg="Setting up logging!", level=logging.INFO)
    g4f.logging = True

    bot = Bot(token=os.getenv("tg_bot_token"), parse_mode="HTML")

    cmd_of_bot = []
    for command in list_of_commands:
        cmd_of_bot.append(BotCommand(command=command[0], description=command[1]))
    await bot.set_my_commands(cmd_of_bot)

    dp = Dispatcher()
    await dp.start_polling(bot, session_maker=session_maker, on_startup=[register_handlers(dp)])
