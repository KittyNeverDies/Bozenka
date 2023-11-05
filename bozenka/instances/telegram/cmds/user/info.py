import logging

from aiogram.types import Message
from bozenka.instances.telegram.utils.simpler import ru_cmds
from bozenka.instances.telegram.utils.keyboards import delete_keyboard


async def chat_info(msg: Message):
    """
    Shows information about chat by command `/info`
    :param msg:
    :return:
    """
    logging.log(msg=f"Sending information about chat user_id={msg.from_user.id}",
                level=logging.INFO)
    chat = await msg.bot.get_chat(msg.chat.id)
    await msg.answer(ru_cmds["info"].replace
                     ("nameofchathere", "<code>" + chat.title + "</code>").replace
                     ("chattype", ru_cmds["chat_types"][chat.type]).replace
                     ("isforum", ru_cmds["forum_type"][chat.is_forum]).replace
                     ("requiredinvite", ru_cmds["required_invite"][chat.join_by_request]).replace
                     ("ishiddenmembers", ru_cmds["hidden_members"][chat.has_hidden_members]).
                     replace("isprotected", ru_cmds["isprotected"][chat.has_protected_content]).
                     replace("descr", "\n" + chat.description), reply_markup=delete_keyboard(admin_id=msg.from_user.id))
