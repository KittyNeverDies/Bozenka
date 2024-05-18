from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bozenka.instances.telegram.utils.callbacks_factory import *


def delete_keyboard(admin_id: int) -> InlineKeyboardMarkup:
    """
    Basic keyboard for all messages from bot.
    By pressing this button, message from bot will get deleted.
    :param admin_id: User_id of user to work with this
    :return: None
    """
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Спасибо, удали сообщение ✅", callback_data=DeleteMenu(user_id_clicked=str(admin_id)).pack())
    ]])
    return kb
