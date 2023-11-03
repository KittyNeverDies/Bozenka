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
    await msg.answer("Удача ✅\n"
                     f"Пользователь {msg.from_user.mention_html()} закрыл данное обсуждение.",
                     reply_markup=delete_keyboard(msg.from_user.id))


async def reopen_topic(msg: Message, bot: Bot) -> None:
    """
    /open command function. Opens thread
    :param msg:
    :param bot:
    :return:
    """
    await bot.reopen_forum_topic(chat_id=msg.chat.id, message_thread_id=msg.message_thread_id)
    await msg.answer("Удача ✅\n"
                     f"Пользователь {msg.from_user.mention_html()} открыл данное обсуждение.",
                     reply_markup=delete_keyboard(msg.from_user.id))


async def close_general_topic(msg: Message, bot: Bot):
    """
    /close_general command function. Closes general thread
    :param msg:
    :param bot:
    :return:
    """
    await bot.close_general_forum_topic(chat_id=msg.chat.id)
    await msg.answer("Удача ✅\n"
                     f"Пользователь {msg.from_user.mention_html()} закрыл основное обсуждение",
                     reply_markup=delete_keyboard(msg.from_user.id))


async def reopen_general_topic(msg: Message, bot: Bot):
    """
    /open_general command function. Opens general thread
    :param msg:
    :param bot:
    :return:
    """
    await bot.reopen_general_forum_topic(chat_id=msg.chat.id)
    await msg.answer("Удача ✅\n"
                     f"Пользователь {msg.from_user.mention_html()} открыл основное обсуждение",
                     reply_markup=delete_keyboard(msg.from_user.id))


async def hide_general_topic(msg: Message, bot: Bot):
    """
    /hide_general command function. Hides general thread
    :param msg: Message telegram object
    :param bot: Object of telegram bot
    :return:
    """
    await bot.hide_general_forum_topic(chat_id=msg.chat.id)
    await msg.answer("Удача ✅\n"
                     f"Пользователь {msg.from_user.mention_html()} скрыл основное обсуждение",
                     reply_markup=delete_keyboard(msg.from_user.id))


async def unhide_general_topic(msg: Message, bot: Bot):
    """
    /show_general command function. Shows back general thread.
    :param msg: Message telegram object
    :param bot: Object of telegram bot
    :return:
    """
    await bot.unhide_general_forum_topic(chat_id=msg.chat.id)
    await msg.answer("Удача ✅\n"
                     f"Пользователь {msg.from_user.mention_html()} раскрыл основное обсуждение",
                     reply_markup=delete_keyboard(msg.from_user.id))


async def rename_topic(msg: Message, bot: Bot, command: CommandObject):
    """
    /rename command function. Rename thread to a new name
    :param msg: Message telegram object
    :param bot: Object of telegram bot
    :param command: Object of telegram command
    :return:
    """
    await msg.general_forum_topic_unhidden
    await bot.edit_forum_topic(name=command.text, chat_id=msg.chat.id, message_thread_id=msg.message_thread_id)
