from aiogram import types

from bozenka.instances.telegram.utils.callbacks_factory import PinMsg, UnpinMsg
from bozenka.instances.telegram.utils.keyboards import unpin_msg_keyboard, pin_msg_keyboard


async def inline_pin_msg(call: types.CallbackQuery, callback_data: PinMsg) -> None:
    """
    Query, what pins message
    :param call:
    :param callback_data:
    :return:
    """
    if callback_data.user_id == call.from_user.id:
        return

    await call.message.chat.pin_message(message_id=callback_data.msg_id)
    await call.message.edit_text("Удача ✅\n"
                                 "Сообщение было закреплено 📌",
                                 reply_markup=pin_msg_keyboard(user_id=call.from_user.id, msg_id=callback_data.msg_id))


async def inline_unpin_msg(call: types.CallbackQuery, callback_data: UnpinMsg) -> None:
    """
    Query, what unpins message
    :param call:
    :param callback_data:
    :return:
    """
    if callback_data.user_id == call.from_user.id:
        return

    await call.message.chat.pin_message(message_id=callback_data.msg_id)
    await call.message.edit_text("Удача ✅\n"
                                 "Сообщение было откреплено 📌",
                                 reply_markup=unpin_msg_keyboard(user_id=call.from_user.id, msg_id=callback_data.msg_id))
