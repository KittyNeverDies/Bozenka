
import logging

from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.filters import Command, CommandStart

from bozenka.instances.telegram.handlers.main.setup import *
from bozenka.instances.telegram.handlers.main.start import *


def register_main_cmd(router: Router) -> None:
    """
    Registers all commands related to basic commands or main commands in bot.
    Don't require any special perms for bot in group.
    :param router:
    :return:
    """
    logging.log(msg="Registering main related commands", level=logging.INFO)

    # Start command handler
    """
    router.message.register(start_cmd, Command(commands=["start"]), F.chat.type == ChatType.PRIVATE)
    """

    router.message.register(start_cmd, *[Command(commands=["start"]), F.chat.type == ChatType.PRIVATE])

    # Registering command /setup
    router.message.register(setup_cmd, Command(commands=["setup"]), ~(F.chat.type == ChatType.PRIVATE))

    # After adding to chat handler
    router.message.register(group_adding_handler, F.content_type == ContentType.SUPERGROUP_CHAT_CREATED)
    router.message.register(group_adding_handler, F.content_type == ContentType.GROUP_CHAT_CREATED)
