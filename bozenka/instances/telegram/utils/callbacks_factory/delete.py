from aiogram.filters.callback_data import CallbackData


class DeleteCallbackData(CallbackData, prefix="delete"):
    """
       Callback with information to delete message
    """
    user_id_clicked: int
