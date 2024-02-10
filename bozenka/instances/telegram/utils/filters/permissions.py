from typing import Any

from aiogram.filters import Filter
from aiogram.methods import GetChatMember
from aiogram.types import Message, ChatPermissions
from aiogram.enums import ChatMemberStatus
from bozenka.instances.telegram.utils.simpler import ru_cmds


class UserHasPermissions(Filter):
    """
    Check, does user have permissions, what user need to work with bot.
    """
    # List of permissions avaible to users.
    # Basic permissions for administration and user
    permissions = [
        "can_manage_chat",
        "can_delete_messages",
        "can_manage_video_chats",
        "can_restrict_members",
        "can_promote_members",
        "can_change_info",
        "can_invite_users",
        "can_post_messages",
        "can_edit_messages",
        "can_pin_messages",
        "can_manage_topics",
        "can_send_messages",
        "can_send_audios",
        "can_send_documents",
        "can_send_photos",
        "can_send_videos",
        "can_send_video_notes",
        "can_send_voice_notes",
        "can_send_polls",
        "can_send_other_messages",
        "can_add_web_page_previews",
    ]

    def __init__(self, perms: list[Any]) -> None:
        self.perms = perms

    @staticmethod
    async def check_permissions(permission, msg: Message) -> bool:
        """
        Checking permissions, included to user.
        :return:
        """
        if permission.count(False) > 0 or permission.count(None) > 0:
            await msg.answer("Ошибка ❌\n"
                             "У вас нет прав на использование этой комманды 🚫")
            return False
        return True

    def generate_perms_list(self, user) -> list[Any]:
        """
        Generates list of permissions for user.
        :param user: User telegram object
        :return: List
        """
        permission = []
        for rule in self.perms:
            if rule in self.permissions:
                exec(f"permission.append(user.{rule})")
        return permission

    async def __call__(self, msg: Message) -> bool:
        """
        Working after catching a call from aiogram
        :param msg: Message telegram object
        :param self: A self object of this class
        :return: None
        """
        user = await msg.chat.get_member(msg.from_user.id)
        if user.status != ChatMemberStatus.CREATOR:
            permission = self.generate_perms_list(user)
        else:
            permission = None

        return True if user.status == ChatMemberStatus.CREATOR else self.check_permissions(permission, msg)


class BotHasPermissions(UserHasPermissions):
    """
    Check, does bot have permissions, what user need to work with bot.
    """

    async def __call__(self, msg: Message, *args, **kwargs) -> bool:
        """
        Working after catching a call from aiogram
        :param msg: Message telegram object
        :param self: A self object of this class
        :return: None
        """
        bot = await msg.chat.get_member(msg.chat.bot.id)
        permission = self.generate_perms_list(bot)
        return await self.check_permissions(permission, msg)


class IsOwner(Filter):
    """
    Checks, is memeber is owner of this chat
    """

    def __init__(self, is_admin: bool) -> None:
        """
        Basic init class
        :param is_admin: Is admin status
        :return: Nothing
        """
        self.is_admin = is_admin

    async def __call__(self, msg: Message) -> bool:
        """
        Working after catching a call from aiogram
        :param msg: Message telegram object
        :param self: A self object of this class
        :return: None
        """
        user = await msg.chat.get_member(msg.from_user.id)
        if ChatMemberStatus.CREATOR != user.status:
            await msg.answer(ru_cmds["no-perms"])
        return ChatMemberStatus.CREATOR == user.status


class IsAdminFilter(Filter):
    """
    Checks, is member of chat is admin and
    does bot have administration rights
    """

    def __init__(self, is_user_admin: bool, is_bot_admin: bool) -> None:
        """
        Basic init class

        """
        self.is_user_admin = is_user_admin
        self.is_bot_admin = is_bot_admin

    async def __call__(self, msg: Message) -> bool:
        """
        Working after catching a call from aiogram
        :param msg: Message telegram object
        :param self: A self object of this class
        :return: None
        """
        user = await msg.chat.get_member(msg.from_user.id)
        bot = await msg.chat.get_member(msg.bot.id)
        if ChatMemberStatus.ADMINISTRATOR != user.status and ChatMemberStatus.CREATOR != user.status:
            if bot.status != ChatMemberStatus.ADMINISTRATOR:
                await msg.reply("Ошибка ❌\n"
                                "У вас нет прав на использование этой комманды. У меня нет прав на использование  🚫")
            else:
                await msg.reply("Ошибка ❌\n"
                                "У вас нет прав на использование этой комманды 🚫")
            return False
        if ChatMemberStatus.CREATOR == user.status:
            return True
        return ChatMemberStatus.ADMINISTRATOR == user.status or ChatMemberStatus.CREATOR == user.status
