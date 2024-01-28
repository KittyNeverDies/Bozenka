from aiogram.types import Message as Message
from bozenka.instances.telegram.utils.keyboards import unpin_msg_keyboard, pin_msg_keyboard, delete_keyboard
from bozenka.instances.telegram.utils.simpler import SolutionSimpler


async def pin(msg: Message) -> None:
    """
    /pin command function, pins replied command
    :param msg: Message telegram object
    :return: Nothing
    """
    await SolutionSimpler.pin_msg(msg)
    await msg.answer("Удача ✅\n"
                     "Сообщение было закреплено 📌",
                     reply_markup=pin_msg_keyboard(msg_id=msg.reply_to_message.message_id, user_id=msg.from_user.id))


async def unpin(msg: Message) -> None:
    """
    /unpin command function, unpins replied command
    :param msg: Message telegram object
    :return: Nothing
    """
    await SolutionSimpler.unpin_msg(msg)
    await msg.answer("Удача ✅\n"
                     "Сообщение было откреплено 📌",
                     reply_markup=unpin_msg_keyboard(msg_id=msg.reply_to_message.message_id, user_id=msg.from_user.id))


async def unpin_all(msg: Message) -> None:
    """
    /unpin_all command function, unpins all messages in chat
    :param msg: Message telegram object
    :return: Nothing
    """
    await SolutionSimpler.unpin_all_messages(msg)
    await msg.answer("Удача ✅\n"
                     "Все сообщения были откреплены 📌",
                     reply_markup=delete_keyboard(admin_id=msg.from_user.id))

