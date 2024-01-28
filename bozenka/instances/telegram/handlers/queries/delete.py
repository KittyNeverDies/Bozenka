import logging

from aiogram import types

from bozenka.instances.telegram.utils.callbacks_factory import DeleteCallbackData
from aiogram.enums import ChatMemberStatus


async def inline_delete(call: types.CallbackQuery, callback_data: DeleteCallbackData) -> None:
    """
    Deletes messsage, after special callback
    :param call:
    :param callback_data:
    :return:
    """
    user_clicked = await call.message.chat.get_member(call.from_user.id)
    if call.from_user.id == callback_data.user_id_clicked or user_clicked.status == ChatMemberStatus.ADMINISTRATOR:
        await call.answer("Хорошо ✅")
        logging.log(msg=f"Deleted message with message_id={call.message.message_id}",
                    level=logging.INFO)
        await call.message.delete()
