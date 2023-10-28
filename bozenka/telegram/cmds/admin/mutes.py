from aiogram.filters import CommandObject
from aiogram.types import Message as Message
from aiogram.enums import ChatMemberStatus
from sqlalchemy.ext.asyncio import async_sessionmaker
from bozenka.telegram.utils.keyboards import mute_keyboard, unmute_keyboard
from bozenka.telegram.utils.simpler import SolutionSimpler


async def mute(msg: Message, command: CommandObject, session_maker: async_sessionmaker):
    """
    Handler of command /mute
    Restricts member from using chat
    :param msg: Message telegram object
    :param command: Object of telegram command
    :param session_maker: Session maker object of SqlAlchemy
    :return:
    """
    restricting = await msg.chat.get_member(msg.reply_to_message.from_user.id)
    if restricting.status == ChatMemberStatus.LEFT or restricting.status == ChatMemberStatus.KICKED:
        return
    config = await SolutionSimpler.mute_user(msg, command, session_maker)
    if config["mute_time"] and config["reason"] != "":
        await msg.answer("Удача ✅\n"
                         f"Пользователь {msg.from_user.mention_html()} запретил писать "
                         f"сообщения пользователю {msg.reply_to_message.from_user.mention_html()}.\n"
                         f"По причине {config['reason']}, до даты {config['mute_time']}",
                         reply_markup=mute_keyboard(msg.from_user.id, restricting.user.id))
    elif config["mute_reason"] != "":
        await msg.answer("Удача ✅\n"
                         f"Пользователь {msg.from_user.mention_html()} запретил писать "
                         f"сообщения пользователю {msg.reply_to_message.from_user.mention_html()}.\n"
                         f"По причине {config['reason']}",
                         reply_markup=mute_keyboard(msg.from_user.id, restricting.user.id))
    elif config["mute_time"]:
        await msg.answer("Удача ✅\n"
                         f"Пользователь {msg.from_user.mention_html()} запретил писать "
                         f"сообщения пользователю {msg.reply_to_message.from_user.mention_html()}.\n"
                         f"До даты {config['mute_time']}",
                         reply_markup=mute_keyboard(msg.from_user.id, restricting.user.id))
    else:
        await msg.answer("Удача ✅\n"
                         f"Пользователь {msg.from_user.mention_html()} запретил писать "
                         f"сообщения пользователю {msg.reply_to_message.from_user.mention_html()}.\n",
                         reply_markup=mute_keyboard(msg.from_user.id, restricting.user.id))


async def unmute(msg: Message, session_maker: async_sessionmaker):
    """
    Handler of command /unmute
    Gives access member to send messages into chat
    :param msg: Message telegram object
    :param command: Object of telegram command
    :param session_maker: Session maker object of SqlAlchemy
    :return:
    """
    await SolutionSimpler.unmute_user(msg, session_maker)
    await msg.answer("Удача ✅"
                     f"Пользователь {msg.from_user.mention_html()} разрешил писать "
                     f"сообщения пользователю {msg.reply_to_message.from_user.mention_html()}",
                     reply_markup=unmute_keyboard(msg.from_user.id, msg.reply_to_message.from_user.id))
