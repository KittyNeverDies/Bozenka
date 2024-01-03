from aiogram import types

from bozenka.instances.telegram.utils.callbacks_factory import CloseThread, OpenThread
from bozenka.instances.telegram.utils.keyboards import open_thread_keyboard, close_thread_keyboard, delete_keyboard
from bozenka.instances.telegram.utils.simpler import SolutionSimpler


async def inline_close_thread(call: types.CallbackQuery, callback_data: CloseThread) -> None:
    """
    Query, what close thread
    :param call:
    :param callback_data:
    :return:
    """

    if callback_data.user_id != call.from_user.id or not call.message.chat.is_forum:
        return
    config = await SolutionSimpler.close_topic(msg=call.message, call=call)
    await call.message.edit_text(
        config[0],
        reply_markup=close_thread_keyboard(user_id=call.from_user.id) if config[1] else
        delete_keyboard(admin_id=call.from_user.id)
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
    config = await SolutionSimpler.open_topic(msg=call.message, call=call)
    await call.message.edit_text(
        config[0],
        reply_markup=open_thread_keyboard(user_id=call.from_user.id) if config[1] else
        delete_keyboard(admin_id=call.from_user.id)
    )
