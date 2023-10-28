from aiogram import Bot
from aiogram.filters import CommandObject
from aiogram.types import Message as Message
from bozenka.telegram.utils.keyboards import delete_keyboard
from bozenka.telegram.utils.simpler import ru_cmds


async def close_topic(msg: Message, bot: Bot) -> None:
    """
    /close command function. Closing thread
    :param msg: Message telegram object
    :param bot: Object of telegram bot
    :return:
    """
    await bot.close_forum_topic(chat_id=msg.chat.id, message_thread_id=msg.message_thread_id)
    await msg.answer(ru_cmds["topic_closed"].replace("user", msg.from_user.mention_html()),
                     reply_markup=delete_keyboard(msg.from_user.id))


async def reopen_topic(msg: Message, bot: Bot) -> None:
    """
    /open command function. Opens thread
    :param msg:
    :param bot:
    :return:
    """
    await bot.reopen_forum_topic(chat_id=msg.chat.id, message_thread_id=msg.message_thread_id)
    await msg.answer(ru_cmds["open_topic"].replace("user", msg.from_user.mention_html()),
                     reply_markup=delete_keyboard(msg.from_user.id))


async def close_general_topic(msg: Message, bot: Bot):
    """
    /close_general command function. Closes general thread
    :param msg:
    :param bot:
    :return:
    """
    await bot.close_general_forum_topic(chat_id=msg.chat.id)
    await msg.answer(ru_cmds["close_general"].replace("user", msg.from_user.mention_html()),
                     reply_markup=delete_keyboard(msg.from_user.id))


async def reopen_general_topic(msg: Message, bot: Bot):
    """
    /open_general command function. Opens general thread
    :param msg:
    :param bot:
    :return:
    """
    await bot.reopen_general_forum_topic(chat_id=msg.chat.id)
    await msg.answer(ru_cmds["open_general"].replace("user", msg.from_user.mention_html()),
                     reply_markup=delete_keyboard(msg.from_user.id))


async def hide_general_topic(msg: Message, bot: Bot):
    """
    /hide_general command function. Hides general thread
    :param msg: Message telegram object
    :param bot: Object of telegram bot
    :return:
    """
    await bot.hide_general_forum_topic(chat_id=msg.chat.id)
    await msg.answer(ru_cmds["hide_general"].replace("user", msg.from_user.mention_html()),
                     reply_markup=delete_keyboard(msg.from_user.id))


async def unhide_general_topic(msg: Message, bot: Bot):
    """
    /show_general command function. Shows back general thread.
    :param msg: Message telegram object
    :param bot: Object of telegram bot
    :return:
    """
    await bot.unhide_general_forum_topic(chat_id=msg.chat.id)
    await msg.answer(ru_cmds["show_general"].replace("user", msg.from_user.mention_html()),
                     reply_markup=delete_keyboard(msg.from_user.id))


async def rename_topic(msg: Message, bot: Bot, command: CommandObject):
    await msg.general_forum_topic_unhidden
    await bot.edit_forum_topic(name=command.text, chat_id=msg.chat.id, message_thread_id=msg.message_thread_id)

