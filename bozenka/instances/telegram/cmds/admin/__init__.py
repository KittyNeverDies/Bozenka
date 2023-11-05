__all__ = ["bans", "mutes", "pins", "topics"]

import logging

from aiogram import Router, F
from aiogram.filters import Command

from bozenka.instances.telegram.cmds.admin.mutes import mute
from bozenka.instances.telegram.cmds.admin.pins import pin, unpin, unpin_all
from bozenka.instances.telegram.cmds.admin.topics import *
from bozenka.instances.telegram.cmds.admin.bans import ban
from bozenka.instances.telegram.utils.filters import (
    IsAdminFilter,
    UserHasPermissions
)


def register_admin_cmd(router: Router) -> None:
    """
    Registers all commands related to administrators in group.
    All commands there require access to some group perms.
    :param router:
    :return:
    """
    logging.log(msg="Registering administrator commands", level=logging.INFO)
    router.message.register(ban, Command(commands="ban"),
                            IsAdminFilter(True), F.reply_to_message.text)
    router.message.register(pin, Command(commands="pin"), UserHasPermissions(["can_pin_messages"]), F.reply_to_message.text)
    router.message.register(unpin, Command(commands="unpin"), UserHasPermissions(["can_pin_messages"]), F.reply_to_message.text)
    router.message.register(unpin_all, Command(commands="unpin_all"), IsAdminFilter(True), F.reply_to_message.text)
    router.message.register(reopen_topic, Command(commands=["reopen_topic", "open_topic", "open"]),
                            UserHasPermissions(["can_pin_messages"]), F.chat.is_forum)
    router.message.register(close_topic, Command(commands=["close_topic", "close"]),
                            UserHasPermissions(["can_pin_messages"]), F.chat.is_forum)
    router.message.register(mute, Command(commands=["mute", "re"]), UserHasPermissions(["can_restrict_members"]))
    router.message.register(close_general_topic, Command(commands=["close_general"]),
                            UserHasPermissions(["can_pin_messages"]), F.chat.is_forum)
    router.message.register(reopen_general_topic, Command(commands=["reopen_general", "open_general"]),
                            UserHasPermissions(["can_pin_messages"]), F.chat.is_forum)
    router.message.register(hide_general_topic, Command(commands=["hide_general"]),
                            UserHasPermissions(["can_pin_messages"]), F.chat.is_forum)
    router.message.register(unhide_general_topic, Command(commands=["unhide_general", "show_general"]),
                            UserHasPermissions(["can_pin_messages"]), F.chat.is_forum)

