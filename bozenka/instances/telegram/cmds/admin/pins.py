from aiogram.types import Message as Message
from bozenka.instances.telegram.utils.keyboards import unpin_msg_keyboard, pin_msg_keyboard, delete_keyboard


async def pin(msg: Message):
    """
    /pin command function, pins replied command
    :param msg: Message telegram object
    :return:
    """
    await msg.chat.pin_message(message_id=msg.reply_to_message.message_id)
    await msg.answer("Удача ✅\n"
                     "Сообщение было закреплено 📌",
                     reply_markup=pin_msg_keyboard(msg_id=msg.reply_to_message.message_id, user_id=msg.from_user.id))


async def unpin(msg: Message):
    """
    /unpin command function, unpins replied command
    :param msg: Message telegram object
    :return:
    """
    await msg.chat.unpin_message(message_id=msg.reply_to_message.message_id)
    await msg.answer("Удача ✅\n"
                     "Сообщение было откреплено 📌",
                     reply_markup=unpin_msg_keyboard(msg_id=msg.reply_to_message.message_id, user_id=msg.from_user.id))


async def unpin_all(msg: Message):
    """
    /unpin_all command function, unpins all messages in chat
    :param msg: Message telegram object
    :return:
    """
    await msg.chat.unpin_all_messages()
    await msg.answer("Удача ✅\n"
                     "Все сообщения были откреплены 📌",
                     reply_markup=delete_keyboard(admin_id=msg.from_user.id))

