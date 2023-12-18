import logging

from aiogram import types

from bozenka.instances.telegram.utils.callbacks_factory import BanData, UnbanData
from aiogram.enums import ChatMemberStatus

from bozenka.instances.telegram.utils.keyboards import ban_keyboard, unban_keyboard


async def inline_ban(call: types.CallbackQuery, callback_data: BanData) -> None:
    """
    Query, what bannes users after callback
    :param call:
    :param callback_data:
    :return:
    """
    clicked_user = await call.message.chat.get_member(call.from_user.id)
    banned_user = await call.message.chat.get_member(int(callback_data.user_id_ban))
    if not banned_user.is_member and banned_user.status == ChatMemberStatus.KICKED:
        return
    elif call.from_user.id == callback_data.user_id_clicked or clicked_user.status == ChatMemberStatus.ADMINISTRATOR:
        await call.answer("Успешно заблокирован ✅")
        await call.message.edit_text(
            "Удача ✅\n"
            f"Пользователь {banned_user.user.mention_html()} был заблокирован пользователем {call.from_user.mention_html()}.",
            reply_markup=ban_keyboard(admin_id=call.from_user.id, ban_id=banned_user.user.id)
        )
        logging.log(msg=f"Banned user @{banned_user.user.full_name} user_id=f{banned_user.user.id}", level=logging.INFO)


async def inline_unban(call: types.CallbackQuery, callback_data: UnbanData) -> None:
    """
    Query, what unbannes users after callback
    :param call:
    :param callback_data:
    :return:
    """
    clicked_user = await call.message.chat.get_member(call.from_user.id)
    unbanned_user = await call.message.chat.get_member(int(callback_data.user_id_unban))
    if unbanned_user.is_member and unbanned_user.status != ChatMemberStatus.KICKED:
        return
    if call.from_user.id == callback_data.user_id_clicked or clicked_user.status == ChatMemberStatus.ADMINISTRATOR:
        await call.answer("Успешно разблокирован ✅")
        await call.message.edit_text(
            "Удача ✅\n"
            f"Пользователь {unbanned_user.user.mention_html()} был разблокирован пользователем {call.from_user.mention_html()}.",
            reply_markup=unban_keyboard(admin_id=call.from_user.id, ban_id=unbanned_user.user.id)
        )
        logging.log(msg=f"Unbanned user @{unbanned_user.user.full_name} user_id=f{unbanned_user.user.id}", level=logging.INFO)
