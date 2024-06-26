import logging
from typing import Any

from aiogram.filters import Filter
from aiogram.methods import GetChatMember
from aiogram.types import Message, ChatPermissions, CallbackQuery
from aiogram.enums import ChatMemberStatus, ChatType

from bozenka.instances.telegram.utils.delete import delete_keyboard


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
        print("True")

    def generate_perms_list(self, user) -> list[Any]:
        """
        Generates list of permissions for user.
        :param user: User telegram object
        :return: List
        """
        permission = []
        for rule in self.perms:
            if rule in self.permissions:
                try:
                    # Checking, does user have this permission
                    exec(f"permission.append(user.{rule})")
                except Exception as e:
                    logging.error(f"Error: {e}")
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

    async def __call__(self, msg: Message | CallbackQuery) -> bool:
        """
        Working after catching a call from aiogram
        :param msg: Message or CallbackQuery telegram object
        :param self: A self object of this class
        :return: None
        """
        if type(msg) is CallbackQuery:
            user = await msg.message.chat.get_member(msg.from_user.id)
        else:
            user = await msg.chat.get_member(msg.from_user.id)
        if ChatMemberStatus.CREATOR != user.status:
            await msg.answer("Ошибка ❌\n"
                             "У вас нет прав на использование этой комманды 🚫")
            print(user.status)
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

    async def __call__(self, msg: Message | CallbackQuery) -> bool:
        """
        Working after catching a call from aiogram
        :param msg: Message telegram object
        :param self: A self object of this class
        :return: None
        """
        if type(msg) is CallbackQuery:
            user = await msg.message.chat.get_member(msg.from_user.id)
            bot = await msg.message.chat.get_member(msg.message.chat.bot.id)
            msg: CallbackQuery
        else:
            user = await msg.chat.get_member(msg.from_user.id)
            bot = await msg.chat.get_member(msg.chat.bot.id)

        if msg.chat.type == ChatType.PRIVATE:
            return False

        if ChatMemberStatus.ADMINISTRATOR != user.status and ChatMemberStatus.CREATOR != user.status:
            if bot.status != ChatMemberStatus.ADMINISTRATOR:
                if type(msg) is Message:
                    await msg.reply("Ошибка ❌\n"
                                    "У вас нет прав на использование этой комманды. \n"
                                    "У меня нет прав для осуществления этой комманды",
                                    reply_markup=delete_keyboard())
                else:
                    await msg.answer(
                        "Ошибка ❌\n"
                        "У вас нет прав на осуществленния действия \n"
                        "У меня нет прав для осуществления действия",
                        show_alert=True
                    )
                return False
            else:
                if type(msg) is Message:
                    await msg.reply("Ошибка ❌\n"
                                    "У вас нет прав на использование этой комманды 🚫",
                                    reply_markup=delete_keyboard())
                else:
                    await msg.answer("Ошибка ❌\n"
                                     "У вас нет прав на это действие.", show_alert=True)
                return False

        if bot.status != ChatMemberStatus.ADMINISTRATOR:
            await msg.reply("Ошибка ❌\n"
                            "У меня нет прав для осуществления этой комманды 🚫",
                            reply_markup=delete_keyboard(msg.from_user.id))
            return False

        return ChatMemberStatus.ADMINISTRATOR == user.status or ChatMemberStatus.CREATOR == user.status
