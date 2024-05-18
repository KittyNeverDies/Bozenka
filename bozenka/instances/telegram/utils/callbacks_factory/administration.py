from aiogram.filters.callback_data import CallbackData


# Ban / Unban
class BanData(CallbackData, prefix="ban"):
    """
        Callback with information to ban user
        and handle clicking on button ban
    """
    user_id_ban: int
    user_id_clicked: int


class UnbanData(CallbackData, prefix="unban"):
    """
       Callback with information to unban user
       and handle clicking on button unban
    """
    user_id_unban: int
    user_id_clicked: int


# Mute / Unmute
class MuteData(CallbackData, prefix="mute"):
    """
       Callback with information to mute user
       and handle clicking on button unmute
    """
    user_id_mute: int
    user_id_clicked: int


class UnmuteData(CallbackData, prefix="unmute"):
    """
       Callback with information to unmute user
    """
    user_id_unmute: int
    user_id_clicked: int


# Close / Open thread
class CloseThread(CallbackData, prefix="ct"):
    """
        Callback with information to close thread
    """
    user_id: int


class OpenThread(CallbackData, prefix="ot"):
    """
        Callback with information to open thread
    """
    user_id: int


# Pin / Unpin thread
class PinMsg(CallbackData, prefix='p'):
    """
        Callback with information to pin message
    """
    user_id: int
    msg_id: int


class UnpinMsg(CallbackData, prefix='up'):
    """
        Callback with infromation to unpin message
    """
    user_id: int
    msg_id: int


# Link revoke
class RevokeCallbackData(CallbackData, prefix="mute"):
    """
        Callback with information to revoke invite link
    """
    admin_id: int
    link: str

