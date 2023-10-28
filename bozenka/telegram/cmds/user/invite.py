import logging

from aiogram.types import Message
from bozenka.telegram.utils.keyboards import invite_keyboard
from bozenka.telegram.utils.simpler import ru_cmds


async def invite(msg: Message):
    """
    Generating invite to group by /invite command
    :param msg:
    :return:
    """
    logging.log(msg=f"Generating invite for user_id={msg.from_user.id}",
                level=logging.INFO)
    link = await msg.chat.create_invite_link()
    print(link.invite_link[0])
    await msg.answer(
        ru_cmds["invite_generation"].replace("user", msg.from_user.mention_html(ru_cmds["sir"])),
        reply_markup=invite_keyboard(link=str(link.invite_link), admin_id=msg.from_user.id, chat_name=msg.chat.full_name)
    )

