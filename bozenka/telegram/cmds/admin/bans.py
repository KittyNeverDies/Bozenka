from aiogram.filters import CommandObject
from aiogram.types import Message
from aiogram.enums import ChatMemberStatus
from sqlalchemy.ext.asyncio import async_sessionmaker

from bozenka.telegram.utils.keyboards import ban_keyboard, delete_keyboard

from bozenka.telegram.utils.simpler import SolutionSimpler, ru_cmds


async def ban(msg: Message, command: CommandObject, session_maker: async_sessionmaker):
    """
    /ban command function, supports time and reasons.
    :param msg: Message telegram object
    :param command: Object of telegram command
    :param session_maker: Session maker object of SqlAlchemy
    :return:
    """
    banned_user = await msg.chat.get_member(msg.reply_to_message.from_user.id)
    if banned_user.status == ChatMemberStatus.KICKED:
        await msg.answer(ru_cmds["ban_6"], reply_markup=delete_keyboard(msg.from_user.id))
        return
    config = await SolutionSimpler.ban_user(msg, command, session_maker)
    if config["reason"] and config["ban_time"]:
        await msg.answer(ru_cmds["ban_1"].replace
                         ("banned", msg.reply_to_message.from_user.mention_html()).replace
                         ("admin", msg.from_user.mention_html()).replace
                         ("ban_reason", config["reason"]).replace("ban_time", config["ban_time"]),
                         reply_markup=ban_keyboard(msg.from_user.id, msg.reply_to_message.from_user.id))
    elif config["reason"]:
        await msg.answer(
            ru_cmds["ban_2"].replace
            ("banned", msg.reply_to_message.from_user.mention_html()).replace
            ("admin", msg.from_user.mention_html()).replace
            ("ban_reason", config["reason"]),
            reply_markup=ban_keyboard(admin_id=msg.from_user.id, ban_id=msg.reply_to_message.from_user.id)
        )
    elif config["ban_time"]:
        await msg.answer(
            ru_cmds["ban_4"].replace
            ("banned", msg.reply_to_message.from_user.mention_html()).replace
            ("admin", msg.from_user.mention_html()).replace("ban_time", config["ban_time"]),
            reply_markup=ban_keyboard(admin_id=msg.from_user.id, ban_id=msg.reply_to_message.from_user.id)
        )
    else:
        await msg.answer(
            ru_cmds["ban_3"].replace
            ("banned", msg.reply_to_message.from_user.mention_html()).replace
            ("admin", msg.from_user.mention_html()),
            reply_markup=ban_keyboard(msg.from_user.id, msg.reply_to_message.from_user.id)
        )


async def unban(msg: Message, command: CommandObject, session_maker: async_sessionmaker):
    """
    /unban command function
    :param msg: Message telegram object
    :param command: Object of telegram command
    :param session_maker: Session maker object of SqlAlchemy
    """
    await SolutionSimpler.unban_user(msg, command, session_maker)
    unbanned_user = await msg.chat.get_member(msg.reply_to_message.from_user.id)
    if unbanned_user.is_member and unbanned_user.status != ChatMemberStatus.KICKED:
        await msg.answer(
            ru_cmds["unban_3"],
            reply_markup=delete_keyboard(admin_id=msg.from_user.id)
        )
    elif not command.text:
        await msg.answer(
            ru_cmds["unban_1"]
            .replace("unbanned", msg.reply_to_message.from_user.mention_html())
            .replace("admin", msg.from_user.mention_html()),
            reply_markup=ban_keyboard(admin_id=msg.from_user.id, ban_id=msg.reply_to_message.from_user.id)
        )
    else:
        await msg.answer(
            ru_cmds["unban_2"]
            .replace("unbanned", msg.reply_to_message.from_user.mention_html())
            .replace("admin", msg.from_user.mention_html())
            .replace("reason", CommandObject.text),
            reply_markup=ban_keyboard(admin_id=msg.from_user.id, ban_id=msg.reply_to_message.from_user.id)
        )


async def status(msg: Message, session_maker: async_sessionmaker):
    """
    /status command function
    Checks is user banned and muted
    :param msg:
    :param command:
    :param session_maker:
    :return:
    """
    config = await SolutionSimpler.get_status(msg, session_maker)
    msg_text = ""
    if config["is_banned"]:
        msg_text += "Находится в бане"
        if config["ban_reason"]:
            msg_text += f"по причине <code>{config['ban_reason']}</code>"
        msg_text += "🔨\n"
    if config["is_muted"]:
        msg_text += "Находится в муте"
        if config["mute_reason"]:
            msg_text += f"по причине <code>{config['mute_reason']}</code>"
        msg_text += "🤐\n"
    await msg.answer(msg_text, reply_markup=delete_keyboard(msg.from_user.id))