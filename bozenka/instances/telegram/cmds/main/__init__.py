__all__ = ["setup", "start"]

import logging

from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.filters import Command

from bozenka.instances.telegram.cmds.main.setup import after_adding, setup_cmd


def register_main_cmd(router: Router) -> None:
    """
    Registers all commands related to basic commands or main commands in bot.
    Don't require any special perms for bot in group.
    :param router:
    :return:
    """
    logging.log(msg="Registering main related commands", level=logging.INFO)
    # Start command handler
    # router.message.register(start_cmd, CommandStart)
    router.message.register(setup_cmd, Command(commands=["setup"]))
    # After adding to chat handler
    router.message.register(after_adding, F.content_type == ContentType.SUPERGROUP_CHAT_CREATED)
    router.message.register(after_adding, F.content_type == ContentType.GROUP_CHAT_CREATED)
