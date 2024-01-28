import logging

from aiogram import types

from bozenka.instances.telegram.utils.callbacks_factory import RevokeCallbackData
from aiogram.enums import ChatMemberStatus

from bozenka.instances.telegram.utils.simpler import ru_cmds


async def inline_revoke(call: types.CallbackQuery, callback_data: RevokeCallbackData):
    """
    Revokes invite link
    :param call:
    :param callback_data:
    :return:
    """
    user_clicked = await call.message.chat.get_member(call.from_user.id)
    if callback_data.admin_id == call.from_user.id or user_clicked.status == ChatMemberStatus.ADMINISTRATOR or user_clicked.status == ChatMemberStatus.CREATOR:
        logging.log(msg=f"Revoking link for user_id={call.from_user.id}",
                    level=logging.INFO)
        await call.message.chat.revoke_invite_link(invite_link="https://" + str(callback_data.link))
        await call.answer("Удача ✅")
        await call.message.delete()
