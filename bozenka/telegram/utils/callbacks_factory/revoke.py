from aiogram.filters.callback_data import CallbackData


class RevokeCallbackData(CallbackData, prefix="mute"):
    admin_id: int
    link: str
