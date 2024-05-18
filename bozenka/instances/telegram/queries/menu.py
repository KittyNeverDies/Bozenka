import logging

from aiogram import types

from bozenka.instances.telegram.utils.callbacks_factory import DeleteMenu
from aiogram.enums import ChatMemberStatus

from bozenka.instances.telegram.utils.callbacks_factory.menu_controler import HideMenu


async def delete_callback_handler(call: types.CallbackQuery, callback_data: DeleteMenu) -> None:
    """
    Deletes messsage, after special callback
    :param call: CallbackQuery telegram object
    :param callback_data: DeleteMenu object
    :return: None
    """
    user_clicked = await call.message.chat.get_member(call.from_user.id)
    if call.from_user.id == callback_data.user_id_clicked or user_clicked.status == ChatMemberStatus.ADMINISTRATOR:
        await call.answer("Хорошо ✅")
        logging.log(msg=f"Deleted message with message_id={call.message.message_id}",
                    level=logging.INFO)
        await call.message.delete()


async def hide_menu_handler(call: types.CallbackQuery, callback_data: HideMenu):
    """
    Hide InlineKeyboard, after special callback
    :param call: CallbackQuery telegram object
    :param callback_data: HideMenu object
    :return: None
    """
    user_clicked = await call.message.chat.get_member(call.from_user.id)
    if call.from_user.id == callback_data.user_id_clicked or user_clicked.status == ChatMemberStatus.ADMINISTRATOR:
        await call.answer("Хорошо ✅")
        logging.log(msg=f"Hide inline keyboard message with message_id={call.message.message_id}",
                    level=logging.INFO)
        await call.message.edit_text(call.message.text, reply_markup=None)

