import logging
import re
import time
from datetime import datetime
from typing import Any

from aiogram import types, Bot
from sqlalchemy import select, insert, Select, Insert, Update
from aiogram.filters import CommandObject
from aiogram.types import ChatPermissions
from aiogram.enums import ChatMemberStatus
from aiogram.types import ChatPermissions, ChatAdministratorRights
from sqlalchemy.ext.asyncio import async_sessionmaker


from bozenka.db import get_user, Users




def count_time(counted_time: str) -> int:
    """
    Counts unix time, for seconds, minutes, hours, days, weeks
    :param counted_time:
    :return:
    """
    mute_times = {"d": int(time.time()) + int(counted_time[0]) * 60 * 60 * 24,
                  "s": int(time.time()) + int(counted_time[0]),
                  "m": int(time.time()) + int(counted_time[0]) * 60,
                  "h": int(time.time()) + int(counted_time[0]) * 60 * 60,
                  "w": int(time.time()) + int(counted_time[0]) * 60 * 60 * 24 * 7}
    return mute_times[counted_time[1]]


def cmd_register(command_list: list[Any], bot: Bot) -> list[Any]:
    """
    Registrate commands for telegram automatic tips
    """
    pass


class SolutionSimpler:
    """
    Making feature 'result in your direct message' easy and cleaner to complete.
    Including logging and debugging.
    """
    @staticmethod
    async def ban_user(msg: types.Message, cmd: CommandObject, session: async_sessionmaker) -> dict[str, None | str | bool]:
        """
        Bans user, returns config, by config you can send special message.
        :param msg:
        :param cmd:
        :param session:
        :return:
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
                        .where(Users.user_id == msg.from_user.id and Users.chat_id == msg.chat.id)
                    )
        return config

    @staticmethod
    async def unban_user(msg: types.Message, session: async_sessionmaker) -> None:
        """
        Unbans user, returns nothing
        :param session:
        :param msg:
        :return:
        """
        await msg.chat.unban(msg.reply_to_message.from_user.id)
        logging.log(
            msg=f"Unbanned user @{msg.reply_to_message.from_user.full_name} id={msg.reply_to_message.from_user.id}",
            level=logging.INFO)
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
        :param msg:
        :param session:
        :return:
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
    async def mute_user(msg: types.Message, cmd: CommandObject, session: async_sessionmaker):
        """
        Mutes user, returns config, by config you can send special message.
        :param session:
        :param cmd:
        :param msg:
        :return:
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
        perms = ChatPermissions(can_send_messages=False)
        await msg.chat.restrict(msg.reply_to_message.from_user.id, until_date=config["mute_time"], permissions=perms)
        logging.log(
            msg=f"Muted user @{msg.reply_to_message.from_user.full_name} id={msg.reply_to_message.from_user.id}",
            level=logging.INFO)
        user = await get_user(user_id=msg.from_user.id, chat_id=msg.chat.id, session=session)
        if not user:
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
                        .where(Users.user_id == msg.from_user.id and Users.chat_id == msg.chat.id)
                    )
        return config

    @staticmethod
    async def unmute_user(msg: types.Message, session: async_sessionmaker):
        """
        Unmutes user, returns nothing
        :param session:
        :param msg:
        :return:
        """

        perms = ChatPermissions(can_send_messages=True)
        await msg.chat.restrict(msg.reply_to_message.from_user.id, permissions=perms)
        user = await get_user(user_id=msg.from_user.id, chat_id=msg.chat.id, session=session)
        logging.log(
            msg=f"Unmuted user @{msg.reply_to_message.from_user.full_name} id={msg.reply_to_message.from_user.id}",
            level=logging.INFO)
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
        :param msg:
        :return:
        """
        await msg.chat.pin_message(message_id=msg.reply_to_message.message_id)
        logging.log(
            msg=f"Pinned message id={msg.reply_to_message.message_id} chat_id={msg.chat.id}",
            level=logging.INFO)

    @staticmethod
    async def unpin_msg(msg: types.Message) -> None:
        """
        Unpins replied message, if it pinned, always returns nothing.
        :param msg:
        :return:
        """
        await msg.chat.unpin_message(message_id=msg.reply_to_message.message_id)
        logging.log(
            msg=f"Unpinned message id={msg.reply_to_message.message_id} chat_id={msg.chat.id}",
            level=logging.INFO)

    @staticmethod
    async def unpin_all_msg(msg: types.Message) -> None:
        """
        Unpins all pinned messages, returns nothing
        :param msg:
        :return:
        """
        logging.log(
            msg=f"Unpinned all messages chat_id={msg.chat.id}",
            level=logging.INFO)
        await msg.chat.unpin_all_messages()

    @staticmethod
    async def create_invite(msg: types.Message, cmd: CommandObject):
        """
        Creating invite, returning invite link
        :param msg:
        :param cmd:
        :return:
        """
        if cmd.args and re.match(r"^\d[wdysmh]", cmd.args):
            link = await msg.chat.create_invite_link()

        link = await msg.chat.create_invite_link()
        logging.log(
            msg=f"Created invite into chat by @{msg.from_user.full_name} chat_id={msg.chat.id}",
            level=logging.INFO)
        return link.invite_link
