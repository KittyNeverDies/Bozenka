from aiogram import Bot
from aiogram.filters import CommandObject
from aiogram.types import Message as Message
from bozenka.instances.telegram.utils.keyboards import delete_keyboard, close_thread_keyboard, open_thread_keyboard
from bozenka.instances.telegram.utils.simpler import SolutionSimpler


async def close_topic(msg: Message, bot: Bot) -> None:
    """
    /close command function. Closing thread
    :param msg: Message telegram object
    :param bot: Object of telegram bot
    :return: Nothing
    """
    config = await SolutionSimpler.close_topic(msg=msg)
    await msg.answer(config[0],
                     reply_markup=close_thread_keyboard(user_id=msg.from_user.id)
                     if config[1] else delete_keyboard(msg.from_user.id))


async def reopen_topic(msg: Message, bot: Bot) -> None:
    """
    /open command function. Opens thread
    :param msg: Message telegram object
    :param bot: Object of telegram bot
    :return: Nothing
    """
    config = await SolutionSimpler.open_topic(msg=msg)
    await msg.answer(config[0],
                     reply_markup=open_thread_keyboard(user_id=msg.from_user.id)
                     if config[1] else delete_keyboard(msg.from_user.id))


async def close_general_topic(msg: Message, bot: Bot) -> None:
    """
    /close_general command function. Closes general thread
    :param msg: Message telegram object
    :param bot: Object of telegram bot
    :return: Nothing
    """
    config = await SolutionSimpler.close_general_topic(msg=msg)
    await msg.answer(config[0],
                     reply_markup=close_thread_keyboard(user_id=msg.from_user.id)
                     if config[1] else delete_keyboard(msg.from_user.id))


async def reopen_general_topic(msg: Message, bot: Bot) -> None:
    """
    /open_general command function. Opens general thread
    :param msg: Message telegram object
    :param bot: Object of telegram bot
    :return: Nothing
    """
    config = await SolutionSimpler.open_general_topic(msg=msg)
    await msg.answer(config[0],
                     reply_markup=open_thread_keyboard(user_id=msg.from_user.id)
                     if config[1] else delete_keyboard(msg.from_user.id))


async def hide_general_topic(msg: Message, bot: Bot) -> None:
    """
    /hide_general command function. Hides general thread
    :param msg: Message telegram object
    :param bot: Object of telegram bot
    :return: Nothing
    """
    config = await SolutionSimpler.hide_general_topic(msg=msg)
    await msg.answer(config[0],
                     reply_markup=delete_keyboard(msg.from_user.id))


async def unhide_general_topic(msg: Message, bot: Bot) -> None:
    """
    /show_general command function. Shows back general thread.
    :param msg: Message telegram object
    :param bot: Object of telegram bot
    :return: Nothing
    """
    config = await SolutionSimpler.show_general_topic(msg=msg)
    await msg.answer(config[0],
                     reply_markup=delete_keyboard(msg.from_user.id))


async def rename_topic(msg: Message, bot: Bot, command: CommandObject) -> None:
    """
    /rename command function. Rename thread to a new name
    :param msg: Message telegram object
    :param bot: Object of telegram bot
    :param command: Object of telegram command
    :return: Nothing
    """
    await msg.general_forum_topic_unhidden
    await bot.edit_forum_topic(name=command.text, chat_id=msg.chat.id, message_thread_id=msg.message_thread_id)
