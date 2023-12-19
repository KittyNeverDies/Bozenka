__all__ = ["bans", "mutes", "pins", "topics"]

import logging

from aiogram import Router, F
from aiogram.filters import Command

from bozenka.instances.telegram.handlers.chat_admin.help import *
from bozenka.instances.telegram.handlers.chat_admin.mutes import mute, unmute
from bozenka.instances.telegram.handlers.chat_admin.pins import pin, unpin, unpin_all
from bozenka.instances.telegram.handlers.chat_admin.topics import *
from bozenka.instances.telegram.handlers.chat_admin.bans import ban, unban
from bozenka.instances.telegram.utils.filters import *


def register_admin_cmd(router: Router) -> None:
    """
    Registers all commands related to administrators in group.
    All commands there require access to some group perms.
    :param router:
    :return:
    """
    logging.log(msg="Registering administrator commands", level=logging.INFO)
    # Helpig handlers
    router.message.register(help_ban, Command(commands=["ban"]))
    router.message.register(help_unban, Command(commands=["unban"]))
    router.message.register(help_mute, Command(commands=["mute"]))
    router.message.register(help_unmute, Command(commands=["mute"]))
    router.message.register(help_pin, Command(commands=["pin"]))
    router.message.register(help_unpin, Command(commands=["unpin"]))
    # Ban / Unban commands handler
    router.message.register(ban, Command(commands="ban"),
                            IsAdminFilter(True))
    router.message.register(ban, Command(commands="ban"),
                            IsAdminFilter(True), F.reply_to_message.text)
    router.message.register(unban, Command(commands="unban"),
                            IsAdminFilter(True), F.reply_to_message.text)
    # Mute / Unmute commands handler
    router.message.register(mute, Command(commands=["mute", "re"]), UserHasPermissions(["can_restrict_members"]),
                            BotHasPermissions(["can_restrict_members"]))
    router.message.register(unmute, Command(commands=["unmute"]), UserHasPermissions(["can_restrict_members"]),
                            BotHasPermissions(["can_restrict_members"]))
    # Pin / Unpin / Unpinall commands handler
    router.message.register(pin, Command(commands="pin"), UserHasPermissions(["can_pin_messages"]),
                            BotHasPermissions(["can_pin_messages"]), F.reply_to_message.text)
    router.message.register(unpin, Command(commands="unpin"), UserHasPermissions(["can_pin_messages"]),
                            BotHasPermissions(["can_pin_messages"]), F.reply_to_message.text)
    router.message.register(unpin_all, Command(commands="unpin_all"), IsAdminFilter(True),
                            BotHasPermissions(["can_pin_messages"]), F.reply_to_message.text)
    # Topic managment handlers
    router.message.register(reopen_topic, Command(commands=["reopen_topic", "open_topic", "open"]),
                            UserHasPermissions(["can_manage_topics"]),
                            BotHasPermissions(["can_manage_topics"]), F.chat.is_forum)
    router.message.register(close_topic, Command(commands=["close_topic", "close"]),
                            UserHasPermissions(["can_manage_topics"]),
                            BotHasPermissions(["can_manage_topics"]), F.chat.is_forum)
    router.message.register(close_general_topic, Command(commands=["close_general"]),
                            UserHasPermissions(["can_manage_topics"]),
                            BotHasPermissions(["can_manage_topics"]), F.chat.is_forum)
    router.message.register(reopen_general_topic, Command(commands=["reopen_general", "open_general"]),
                            UserHasPermissions(["can_manage_topics"]),
                            BotHasPermissions(["can_manage_topics"]), F.chat.is_forum)
    router.message.register(hide_general_topic, Command(commands=["hide_general"]),
                            UserHasPermissions(["can_manage_topics"]),
                            BotHasPermissions(["can_manage_topics"]), F.chat.is_forum)
    router.message.register(unhide_general_topic, Command(commands=["unhide_general", "show_general"]),
                            UserHasPermissions(["can_manage_topics"]),
                            BotHasPermissions(["can_manage_topics"]), F.chat.is_forum)

