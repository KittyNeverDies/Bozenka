import logging

from aiogram import Dispatcher, Bot, F
from aiogram.filters import Command
from aiogram.types import BotCommand

from bozenka.generative.provider_categories import *
from .list_of_generative import basic_generatives

categories = [
    Text2TextCategory,
    Text2ImageCategory,
]

commands = [
    BotCommand(command=i.category_command, description=i.category_command_description) for i in categories
]


async def register_all_categories(dp: Dispatcher, telegram_bot: Bot) -> None:
    """
    Registers all handlers of generative categories
    Adds all commands suggestions to the bot.
    :param dp: Aiogram Dispatcher
    :param telegram_bot: Aiogram bot
    :return: None
    """
    logging.info("Registering basic generative handlers!")
    for generative in basic_generatives:
        for telegram_handler in generative.handlers_functions["telegram"]:
            dp.callback_query.register(telegram_handler[0], *telegram_handler[1])

    for category in categories:
        print(category.category_command)
        dp.message.register(category.telegram_menu, Command(category.category_command))
        dp.callback_query.register(category.telegram_start_menu, F.data == category.start_menu_callback_data)

    logging.info("Registered basic generative handlers, going to add commands suggestions ")
    cmds = commands
    for i in await telegram_bot.get_my_commands():
        cmds.append(i)
    await telegram_bot.set_my_commands(cmds)
    logging.info("Commands suggestions added!")
