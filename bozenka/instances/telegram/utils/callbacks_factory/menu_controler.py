from aiogram.filters.callback_data import CallbackData


class DeleteMenu(CallbackData, prefix="delete"):
    """
       Callback with information to delete message
    """
    user_id_clicked: int


class HideMenu(CallbackData, prefix="hide"):
    """
        Callback with information to hide message
    """
    user_id_clicked: int
