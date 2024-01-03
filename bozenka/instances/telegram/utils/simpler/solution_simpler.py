import logging
import re
import time
from datetime import datetime
from typing import Any, Optional

from aiogram import types
from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramRetryAfter, TelegramNotFound, TelegramBadRequest
from aiogram.filters import CommandObject
from aiogram.types import ChatPermissions, CallbackQuery
from sqlalchemy import Update
from sqlalchemy.ext.asyncio import async_sessionmaker

from bozenka.database import get_user, Users
from bozenka.database.tables.telegram import get_settings, ChatSettings


def count_time(counted_time: str) -> int:
    """
    Counts unix time, for seconds, minutes, hours, days, weeks
    :param counted_time: Time, needs to be converted
    :return:
    """
    mute_times = {"d": int(time.time()) + int(counted_time[0]) * 60 * 60 * 24,
                  "s": int(time.time()) + int(counted_time[0]),
                  "m": int(time.time()) + int(counted_time[0]) * 60,
                  "h": int(time.time()) + int(counted_time[0]) * 60 * 60,
                  "w": int(time.time()) + int(counted_time[0]) * 60 * 60 * 24 * 7}
    return mute_times[counted_time[1]]


class SolutionSimpler:
    """
    Making feature 'result in your direct message' easy and cleaner to complete.
    Including logging and debugging.
    """

    @staticmethod
    async def ban_user(msg: types.Message, cmd: CommandObject, session: async_sessionmaker) -> dict[str, None | str | bool]:
        """
        Bans user or user, returns config, by config you can send special message.
        Support multibans & antiflood telegram protection
        :param msg: Message telegram object
        :param cmd: Object of telegram command
        :param session: Session maker object of SqlAlchemy
        :return: Config
        """
        config = {
            "revert_msg": None,
            "ban_time": None,
            "reason": ""
        }
        if cmd.args:
            data = re.split(" ", cmd.args, 2)
            for item in data:
                if re.match(r"^n\w", item) and not config["revert_msg"]:
                    config["revert_msg"] = False
                elif re.match(r"^ye\w", item) and not config["revert_msg"]:
                    config["revert_msg"] = True
                elif re.match(r"^\d[wdysmh]", item) and not config["ban_time"]:
                    config["ban_time"] = datetime.utcfromtimestamp(count_time(item)).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    config["reason"] += item + " "
        try:
            user = msg.reply_to_message.from_user
            await msg.chat.ban(user.id, config["ban_time"], config["revert_msg"])
            logging.log(
                msg=f"Banned user @{msg.reply_to_message.from_user.full_name} id={msg.reply_to_message.from_user.id}",
                level=logging.INFO)
            if not await get_user(user_id=user.id, chat_id=msg.chat.id, session=session):
                new_user = Users(
                    user_id=user.id,
                    chat_id=msg.chat.id,
                    is_banned=True,
                    ban_reason=None if config["reason"] == "" else config["reason"],
                    is_muted=None,
                    mute_reason=None
                )
                async with session() as session:
                    async with session.begin():
                        await session.merge(new_user)
            else:
                async with session() as session:
                    async with session.begin():
                        await session.execute(
                            Update(Users)
                            .values(is_banned=True, ban_reason=None if config["reason"] == "" else config["reason"])
                            .where(Users.user_id == msg.from_user.id and Users.chat_id == msg.chat.id))

        except TelegramRetryAfter as ex:
            time.sleep(ex.retry_after)

            await msg.chat.ban(msg.reply_to_message.from_user.id, config["ban_time"], config["revert_msg"])
            logging.log(
                msg=f"Banned user @{msg.reply_to_message.from_user.full_name} id={msg.reply_to_message.from_user.id}",
                level=logging.INFO)
            user = await get_user(user_id=msg.from_user.id, chat_id=msg.chat.id, session=session)
            if not user:
                new_user = Users(
                    user_id=msg.from_user.id,
                    chat_id=msg.chat.id,
                    is_banned=True,
                    ban_reason=None if config["reason"] == "" else config["reason"],
                    is_muted=None,
                    mute_reason=None
                )
                async with session() as session:
                    async with session.begin():
                        await session.merge(new_user)
            else:
                async with session() as session:
                    async with session.begin():
                        await session.execute(
                            Update(Users)
                            .values(is_banned=True, ban_reason=None if config["reason"] == "" else config["reason"])
                            .where(Users.user_id == msg.from_user.id and Users.chat_id == msg.chat.id))

        except TelegramNotFound:
            logging.log(
                msg=f"Can't ban user, something was not avaible or got disabled",
                level=logging.INFO)
        return config

    @staticmethod
    async def unban_user(msg: types.Message, session: async_sessionmaker) -> None:
        """
        Unbans user by reply, returns nothing
        :param msg: Message telegram object
        :param session: Session maker object of SqlAlchemy
        :return: Nothing
        """
        await msg.chat.unban(msg.reply_to_message.from_user.id)
        logging.log(
            msg=f"Unbanned user @{msg.reply_to_message.from_user.full_name} id={msg.reply_to_message.from_user.id}",
            level=logging.INFO)
        if await get_user(user_id=msg.from_user.id, chat_id=msg.chat.id, session=session):
            async with session() as session:
                async with session.begin():
                    await session.execute(
                        Update(Users)
                        .values(is_banned=False, ban_reason=None)
                        .where(Users.user_id == msg.from_user.id and Users.chat_id == msg.chat.id)
                    )

    @staticmethod
    async def get_status(msg: types.Message, session: async_sessionmaker) -> dict[str, bool | None | Any]:
        """
        Get status of user, is it muted or banned.
        :param msg: Message telegram object
        :param session: Session maker object of SqlAlchemy
        :return: Config
        """
        config = {
            "is_banned": None,
            "ban_reason": None,
            "is_muted": None,
            "mute_reason": None,
        }
        user_tg = await msg.chat.get_member(msg.from_user.id)
        user_db = await get_user(user_id=msg.from_user.id, chat_id=msg.chat.id, session=session)
        config["is_banned"] = True if user_tg.status == ChatMemberStatus.KICKED else False
        config["ban_reason"] = user_db.ban_reason if user_db.ban_reason else None
        config["is_muted"] = True if not user_tg.can_send_messages else False
        config["mute_reason"] = user_db.mute_reason if user_db.mute_reason else None
        return config

    @staticmethod
    async def mute_user(msg: types.Message, cmd: CommandObject, session: async_sessionmaker) -> dict[str, None | str | bool]:
        """
        Mutes user, returns config, by config you can send special message.
        :param msg: Message telegram object
        :param cmd: Object of telegram command
        :param session: Session maker object of SqlAlchemy
        :return: Config or Nothing
        """
        config = {
            "mute_time": None,
            "reason": ""
        }
        if cmd.args:
            data = re.split(" ", cmd.args, 2)
            for item in data:
                if re.match(r"^\d[wdysmh]", item) and not config["mute_time"]:
                    config["mute_time"] = datetime.utcfromtimestamp(count_time(item)).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    config["reason"] += item + " "
        try:
            perms = ChatPermissions(can_send_messages=False)
            await msg.chat.restrict(msg.reply_to_message.from_user.id, until_date=config["mute_time"], permissions=perms)
            logging.log(
                msg=f"Muted user @{msg.reply_to_message.from_user.full_name} id={msg.reply_to_message.from_user.id}",
                level=logging.INFO)
            if not await get_user(user_id=msg.from_user.id, chat_id=msg.chat.id, session=session):
                new_user = Users(
                    user_id=msg.from_user.id,
                    chat_id=msg.chat.id,
                    is_banned=None,
                    ban_reason=None,
                    is_muted=True,
                    mute_reason=None if config["reason"] == "" else config["reason"]
                )
                async with session() as session:
                    async with session.begin():
                        await session.merge(new_user)
            else:
                async with session() as session:
                    async with session.begin():
                        await session.execute(
                            Update(Users)
                            .values(is_muted=True, mute_reason=None if config["reason"] == "" else config["reason"])
                            .where(Users.user_id == msg.from_user.id and Users.chat_id == msg.chat.id))
        except TelegramRetryAfter as ex:
            time.sleep(ex.retry_after)
            perms = ChatPermissions(can_send_messages=False)
            await msg.chat.restrict(msg.reply_to_message.from_user.id, until_date=config["mute_time"],
                                    permissions=perms)
            logging.log(
                msg=f"Muted user @{msg.reply_to_message.from_user.full_name} id={msg.reply_to_message.from_user.id}",
                level=logging.INFO)
            if not await get_user(user_id=msg.from_user.id, chat_id=msg.chat.id, session=session):
                new_user = Users(
                    user_id=msg.from_user.id,
                    chat_id=msg.chat.id,
                    is_banned=None,
                    ban_reason=None,
                    is_muted=True,
                    mute_reason=None if config["reason"] == "" else config["reason"]
                )
                async with session() as session:
                    async with session.begin():
                        await session.merge(new_user)
            else:
                async with session() as session:
                    async with session.begin():
                        await session.execute(
                            Update(Users)
                            .values(is_muted=True, mute_reason=None if config["reason"] == "" else config["reason"])
                            .where(Users.user_id == msg.from_user.id and Users.chat_id == msg.chat.id))
        return config

    @staticmethod
    async def unmute_user(msg: types.Message, session: async_sessionmaker):
        """
        Unmutes user, returns nothing
        :param msg: Message telegram object
        :param session: Session maker object of SqlAlchemy
        :return: Nothing
        """

        perms = ChatPermissions(can_send_messages=True)
        await msg.chat.restrict(msg.reply_to_message.from_user.id, permissions=perms)
        logging.log(
            msg=f"Unmuted user @{msg.reply_to_message.from_user.full_name} id={msg.reply_to_message.from_user.id}",
            level=logging.INFO)
        if await get_user(user_id=msg.from_user.id, chat_id=msg.chat.id, session=session):
            async with session() as session:
                async with session.begin():
                    await session.execute(
                        Update(Users)
                        .values(is_muted=False, mute_reason=None, )
                        .where(Users.user_id == msg.from_user.id and Users.chat_id == msg.chat.id)
                    )

    @staticmethod
    async def pin_msg(msg: types.Message) -> None:
        """
        Pins replied message, returns nothing
        :param msg: Message telegram object
        :return: Nothing
        """
        await msg.chat.pin_message(message_id=msg.reply_to_message.message_id)
        logging.log(
            msg=f"Pinned message id={msg.reply_to_message.message_id} chat_id={msg.chat.id}",
            level=logging.INFO)

    @staticmethod
    async def unpin_msg(msg: types.Message) -> None:
        """
        Unpins replied message, if it pinned, always returns nothing.
        :param msg: Message telegram object
        :return: Nothing
        """
        await msg.chat.unpin_message(message_id=msg.reply_to_message.message_id)
        logging.log(
            msg=f"Unpinned message id={msg.reply_to_message.message_id} chat_id={msg.chat.id}",
            level=logging.INFO)

    @staticmethod
    async def unpin_all_messages(msg: types.Message) -> None:
        """
        Unpins all pinned messages, returns nothing
        :param msg: Message telegram object
        :return: Nothing
        """
        logging.log(
            msg=f"Unpinned all messages chat_id={msg.chat.id}",
            level=logging.INFO)
        await msg.chat.unpin_all_messages()

    @staticmethod
    async def create_invite(msg: types.Message, cmd: CommandObject) -> str:
        """
        Creating invite, returning invite link
        :param msg: Message telegram object
        :param cmd: Object of telegram command
        :return: Generated invite link
        """
        if cmd.args and re.match(r"^\d[wdysmh]", cmd.args):
            link = await msg.chat.create_invite_link()

        link = await msg.chat.create_invite_link()
        logging.log(
            msg=f"Created invite into chat by @{msg.from_user.full_name} chat_id={msg.chat.id}",
            level=logging.INFO)
        return link.invite_link

    @staticmethod
    async def auto_settings(msg: types.Message, session: async_sessionmaker) -> None:
        """
        Creating settings related to chat automaticly
        after adding
        :param msg: Message telegram object
        :param session: Object of telegram command
        :return: Nothing
        """
        chat_data = await get_settings(msg.chat.id, session)
        print(chat_data)
        if not chat_data:
            new_chat_data = ChatSettings(chat_id=msg.chat.id)
            async with session() as session:
                async with session.begin():
                    await session.merge(new_chat_data)

    @staticmethod
    async def close_topic(msg: types.Message, call: Optional[CallbackQuery] = None) -> list[str, bool]:
        """
        Closing topic of chat automaticly
        :param msg: Message telegram object
        :param call: CallbackQuery telegram object
        :return: Nothing
        """
        try:
            if not call:
                if msg.message_thread_id:
                    await msg.bot.close_forum_topic(chat_id=msg.chat.id, message_thread_id=msg.message_thread_id)
                    return [f"Удача ✅\nПользователь {msg.from_user.mention_html()} закрыл данное обсуждение.",
                            True]
                else:
                    await msg.bot.close_general_forum_topic(chat_id=msg.chat.id)
                    return [f"Удача ✅\nПользователь {msg.from_user.mention_html()} закрыл основное обсуждение.",
                            True]
            else:
                if msg.message_thread_id:
                    await msg.bot.close_forum_topic(chat_id=msg.chat.id, message_thread_id=msg.message_thread_id)
                    return [f"Удача ✅\nПользователь {call.from_user.mention_html()} закрыл данное обсуждение.",
                            True]
                else:
                    await msg.bot.close_general_forum_topic(chat_id=msg.chat.id)
                    return [f"Удача ✅\nПользователь {call.from_user.mention_html()} закрыл основное обсуждение.",
                            True]
        except TelegramBadRequest as ex:
            if ex.message == "Bad Request: TOPIC_NOT_MODIFIED":
                return [f"Ошибка ❌\nДанное обсуждение уже закрыто.",
                        False]

    @staticmethod
    async def open_topic(msg: types.Message, call: Optional[CallbackQuery] = None) -> list[str, bool]:
        """
        Opening topic of chat automaticly
        :param msg: Message telegram object
        :param call: CallbackQuery telegram object
        :return: Nothing
        """
        try:

            if not call:
                if msg.message_thread_id:
                    await msg.bot.reopen_forum_topic(chat_id=msg.chat.id, message_thread_id=msg.message_thread_id)
                    return [f"Удача ✅\nПользователь {msg.from_user.mention_html()} открыл данное обсуждение.",
                            True]
                else:
                    await msg.bot.reopen_general_forum_topic(chat_id=msg.chat.id)
                    return [f"Удача ✅\nПользователь {msg.from_user.mention_html()} открыл основное обсуждение",
                            True]
            else:
                if msg.message_thread_id:
                    await msg.bot.reopen_forum_topic(chat_id=msg.chat.id, message_thread_id=msg.message_thread_id)
                    return [f"Удача ✅\nПользователь {call.from_user.mention_html()} открыл данное обсуждение.",
                            True]
                else:
                    await msg.bot.reopen_general_forum_topic(chat_id=msg.chat.id)
                    return [f"Удача ✅\nПользователь {call.from_user.mention_html()} открыл основное обсуждение",
                            True]
        except TelegramBadRequest as ex:
            if ex.message == "Bad Request: TOPIC_NOT_MODIFIED":
                return [f"Ошибка ❌\nДанное обсуждение уже открыто.",
                        False]

    @staticmethod
    async def open_general_topic(msg: types.Message) -> list[str, bool]:
        """
        Opening general topic of chat automaticly
        :param msg: Message telegram object
        :return: Nothing
        """
        try:
            await msg.bot.reopen_general_forum_topic(chat_id=msg.chat.id)
            return [f"Удача ✅\nПользователь {msg.from_user.mention_html()} открыл основное обсуждение", True]
        except TelegramBadRequest as ex:
            if ex.message == "Bad Request: TOPIC_NOT_MODIFIED":
                return [f"Ошибка ❌\nДанное обсуждение уже открыто.", False]

    @staticmethod
    async def close_general_topic(msg: types.Message) -> list[str, bool]:
        """
        Closing general topic of chat automaticly
        :param msg: Message telegram object
        :return: Nothing
        """
        try:
            await msg.bot.close_general_forum_topic(chat_id=msg.chat.id)
            return [f"Удача ✅\nПользователь {msg.from_user.mention_html()} закрыл основное обсуждение", True]
        except TelegramBadRequest as ex:
            if ex.message == "Bad Request: TOPIC_NOT_MODIFIED":
                return [f"Ошибка ❌\nДанное обсуждение уже закрыто.", False]

    @staticmethod
    async def show_general_topic(msg: types.Message) -> list[str, bool]:
        """
        Showing general topic of chat automaticly
        :param msg: Message telegram object
        :return: Nothing
        """
        try:
            await msg.bot.unhide_general_forum_topic(chat_id=msg.chat.id)
            return [f"Удача ✅\nПользователь {msg.from_user.mention_html()} раскрыл основное обсуждение", True]
        except TelegramBadRequest as ex:
            if ex.message == "Bad Request: TOPIC_NOT_MODIFIED":
                return [f"Ошибка ❌\nДанное обсуждение уже публично.", False]

    @staticmethod
    async def hide_general_topic(msg: types.Message) -> list[str, bool]:
        """
        Hiding topic of chat automaticly
        :param msg: Message telegram object
        :return: Nothing
        """
        try:
            await msg.bot.hide_general_forum_topic(chat_id=msg.chat.id)
            return [f"Удача ✅\nПользователь {msg.from_user.mention_html()} скрыл основное обсуждение", True]
        except TelegramBadRequest as ex:
            if ex.message == "Bad Request: TOPIC_NOT_MODIFIED":
                return [f"Ошибка ❌\nДанное обсуждение уже публично.", False]