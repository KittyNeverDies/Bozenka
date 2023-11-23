from aiogram import types

from bozenka.instances.telegram.utils.callbacks_factory import CloseThread, OpenThread
from bozenka.instances.telegram.utils.keyboards import open_thread_keyboard, close_thread_keyboard


async def inline_close_thread(call: types.CallbackQuery, callback_data: CloseThread) -> None:
    """
    Query, what close thread
    :param call:
    :param callback_data:
    :return:
    """

    if callback_data.user_id != call.from_user.id or not call.message.chat.is_forum:
        return

    await call.message.bot.close_forum_topic(chat_id=call.message.chat.id,
                                             message_thread_id=call.message.message_thread_id)
    await call.message.edit_text(
        "Удача ✅\n"
        f"Пользователь {call.from_user.mention_html()} закрыл основное обсуждение",
        reply_markup=open_thread_keyboard(user_id=call.from_user.id)
    )


async def inline_open_thread(call: types.CallbackQuery, callback_data: OpenThread) -> None:
    """
    Query, what opens thread
    :param call:
    :param callback_data:
    :return:
    """

    if callback_data.user_id != call.from_user.id or not call.message.chat.is_forum:
        return

    await call.message.bot.close_forum_topic(chat_id=call.message.chat.id,
                                             message_thread_id=call.message.message_thread_id)

    await call.message.edit_text(
        "Удача ✅\n"
        f"Пользователь {call.from_user.mention_html()} открыл основное обсуждение",
        reply_markup=close_thread_keyboard(user_id=call.from_user.id)
    )
