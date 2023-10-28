__all__ = ["about", "invite", "welcome", ""]

from aiogram.enums import ContentType
from aiogram.filters import Command
from aiogram import Router, F

from bozenka.telegram.cmds.user.about import about
from bozenka.telegram.cmds.user.invite import invite
from bozenka.telegram.cmds.user.info import chat_info
from bozenka.telegram.cmds.user.welcome import *


def register_user_cmd(router: Router) -> None:
    """
    Registers all commands related to users, and can be used by them.
    Some of them require access to some perms for bot.
    :param router:
    :return:
    """
    logging.log(msg="Registering user commands", level=logging.INFO)
    router.message.register(invite, Command(commands=["invite"]))
    router.message.register(about, Command(commands=["about"]))
    router.message.register(leave, F.content_type == ContentType.LEFT_CHAT_MEMBER)
    router.message.register(join, F.content_type == ContentType.NEW_CHAT_MEMBERS)
    router.message.register(chat_info, Command(commands=["info"]))
