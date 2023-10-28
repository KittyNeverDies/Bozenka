from aiogram.filters.callback_data import CallbackData


class BanData(CallbackData, prefix="ban"):
    """
        Callback with information to ban user
    """
    user_id_ban: int
    user_id_clicked: int



class UnbanData(CallbackData, prefix="unban"):
    """
       Callback with information to unban user
    """
    user_id_unban: int
    user_id_clicked: int


class MuteData(CallbackData, prefix="mute"):
    """
       Callback with information to mute user
    """
    user_id_mute: int
    user_id_clicked: int


class UnmuteData(CallbackData, prefix="unmute"):
    """
       Callback with information to unmute user
    """
    user_id_unmute: int
    user_id_clicked: int
