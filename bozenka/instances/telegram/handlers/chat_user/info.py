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
    # Related texts
    texts = {
        "chat_types": {"group": "группой", "supergroup": "cупер группой"},
        "forum_type": {True: "форумом,", False: ", не является форумом,", None: ", не является форумом,"},
        "required_invite": {True: "требуется одобрение заявки на вступление", False: "заявка не требуется.",
                            None: "заявка не требуется."},
        "hidden_members": {True: "присуствуют", False: "отсуствуют", None: "отсуствуют"},
        "isprotected": {True: "пересылать сообщения из группы можно.", False: "пересылать сообщения из группы нельзя.",
                        None: "пересылать сообщения из группы можно."},
    }

    await msg.answer(f"{chat.title}\n"
                     f"{chat.description}\n\n"
                     f"Является {texts['chat_types'][chat.type]} {texts['forum_type'][chat.is_forum]} {texts['required_invite'][chat.join_by_request]}\n"
                     f"Скрытые пользователи {texts['hidden_members'][chat.has_hidden_members]}, {texts['isprotected'][chat.has_protected_content]}",
                     reply_markup=delete_keyboard(admin_id=msg.from_user.id))