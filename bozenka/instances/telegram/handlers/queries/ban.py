import logging

from aiogram import types
from sqlalchemy.ext.asyncio import async_sessionmaker

from bozenka.instances.telegram.utils.callbacks_factory import BanData, UnbanData
from aiogram.enums import ChatMemberStatus

from bozenka.instances.telegram.utils.keyboards import ban_keyboard, unban_keyboard
from bozenka.instances.telegram.utils.simpler import SolutionSimpler


async def inline_ban(call: types.CallbackQuery, callback_data: BanData, session_maker: async_sessionmaker) -> None:
    """
    Query, what bannes users after callback
    :param call: CallBackQuery telegram object
    :param callback_data: BanData object
    :param session_maker: AsyncSessionmaker object
    :return:
    """
    clicked_user = await call.message.chat.get_member(call.from_user.id)
    banned_user = await call.message.chat.get_member(int(callback_data.user_id_ban))

    if call.from_user.id != callback_data.user_id_clicked \
            and clicked_user.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
        return
    await SolutionSimpler.inline_ban_user(call=call, data=callback_data, session=session_maker)

    if not banned_user.is_member and banned_user.status == ChatMemberStatus.KICKED:
        await call.answer("Уже заблокирован ✅")
    else:
        await call.answer("Успешно заблокирован ✅")

    await call.message.edit_text(
            "Удача ✅\n"
            f"{banned_user.user.mention_html('Этот пользователь')} был заблокирован {call.from_user.mention_html('этим пользователем')}.",
            reply_markup=ban_keyboard(admin_id=call.from_user.id, ban_id=banned_user.user.id)
    )
    logging.log(msg=f"Banned user @{banned_user.user.full_name} user_id=f{banned_user.user.id}", level=logging.INFO)


async def inline_unban(call: types.CallbackQuery, callback_data: UnbanData, session_maker: async_sessionmaker) -> None:
    """
    Query, what unbannes users after callback
     :param call: CallBackQuery telegram object
    :param callback_data: UnbanData object
    :param session_maker: AsyncSessionmaker object
    :return:
    """
    clicked_user = await call.message.chat.get_member(call.from_user.id)
    unbanned_user = await call.message.chat.get_member(int(callback_data.user_id_unban))
    if call.from_user.id != callback_data.user_id_clicked \
            and clicked_user.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
        return

    await SolutionSimpler.inline_unban_user(call=call, data=callback_data, session=session_maker)

    if unbanned_user.is_member and unbanned_user.status != ChatMemberStatus.KICKED:
        await call.answer("Уже разблокирован ✅")
    else:
        await call.answer("Успешно разблокирован ✅")
    await call.message.edit_text(
            "Удача ✅\n"
            f"{unbanned_user.user.mention_html('Этот пользователь')} был разблокирован {call.from_user.mention_html('этим пользователем')}.",
            reply_markup=unban_keyboard(admin_id=call.from_user.id, ban_id=unbanned_user.user.id)
        )
    logging.log(msg=f"Unbanned user @{unbanned_user.user.full_name} user_id=f{unbanned_user.user.id}", level=logging.INFO)
