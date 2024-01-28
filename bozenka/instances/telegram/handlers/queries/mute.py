import logging

from aiogram import types
from sqlalchemy.ext.asyncio import async_sessionmaker

from bozenka.instances.telegram.utils.callbacks_factory import UnmuteData, MuteData
from aiogram.enums import ChatMemberStatus

from bozenka.instances.telegram.utils.keyboards import ban_keyboard, unban_keyboard, mute_keyboard, unmute_keyboard
from bozenka.instances.telegram.utils.simpler import SolutionSimpler


async def inline_mute(call: types.CallbackQuery, callback_data: MuteData, session_maker: async_sessionmaker) -> None:
    """
    Query, what mutes users after callback
    :param call: CallBackQuery telegram object
    :param callback_data: BanData object
    :param session_maker: AsyncSessionmaker object
    :return:
    """
    clicked_user = await call.message.chat.get_member(call.from_user.id)
    muted_user = await call.message.chat.get_member(int(callback_data.user_id_mute))

    if call.from_user.id != callback_data.user_id_clicked \
            and clicked_user.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
        return
    await SolutionSimpler.inline_mute_user(call=call, data=callback_data, session=session_maker)

    if not muted_user.can_send_messages and muted_user.status == ChatMemberStatus.RESTRICTED:
        await call.answer("Уже замучен ✅")
    else:
        await call.answer("Успешно замучен ✅")

    await call.message.edit_text(
            "Удача ✅\n"
            f"{muted_user.user.mention_html('Этот пользователь')} был замучен {call.from_user.mention_html('этим пользователем')}.",
            reply_markup=mute_keyboard(admin_id=call.from_user.id, mute_id=callback_data.user_id_mute)
    )
    logging.log(msg=f"Banned user @{muted_user.user.full_name} user_id=f{muted_user.user.id}", level=logging.INFO)


async def inline_unmute(call: types.CallbackQuery, callback_data: UnmuteData, session_maker: async_sessionmaker) -> None:
    """
    Query, what unbannes users after callback
    :param call: CallBackQuery telegram object
    :param callback_data: UnbanData object
    :param session_maker: AsyncSessionmaker object
    :return:
    """
    clicked_user = await call.message.chat.get_member(call.from_user.id)
    unmuted_user = await call.message.chat.get_member(int(callback_data.user_id_unmute))
    if call.from_user.id != callback_data.user_id_clicked \
            and clicked_user.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
        return

    await SolutionSimpler.inline_unmute_user(call=call, data=callback_data, session=session_maker)

    if unmuted_user.can_send_messages or unmuted_user.status == ChatMemberStatus.RESTRICTED:
        await call.answer("Уже размучен ✅")
    else:
        await call.answer("Успешно размучен ✅")
    await call.message.edit_text(
            "Удача ✅\n"
            f"{unmuted_user.user.mention_html('Этот пользователь')} был размучен {call.from_user.mention_html('этим пользователем')}.",
            reply_markup=unmute_keyboard(admin_id=call.from_user.id, unmute_id=unmuted_user.user.id)
        )
    logging.log(msg=f"Unbanned user @{unmuted_user.user.full_name} user_id=f{unmuted_user.user.id}", level=logging.INFO)
