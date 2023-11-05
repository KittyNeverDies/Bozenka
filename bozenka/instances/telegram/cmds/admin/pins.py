from aiogram.types import Message as Message


async def pin(msg: Message):
    """
    /pin command function, pins replied command
    :param msg: Message telegram object
    :return:
    """
    await msg.chat.pin_message(message_id=msg.reply_to_message.message_id)


async def unpin(msg: Message):
    """
    /unpin command function, unpins replied command
    :param msg: Message telegram object
    :return:
    """
    await msg.chat.unpin_message(message_id=msg.reply_to_message.message_id)


async def unpin_all(msg: Message):
    """
    /unpin_all command function, unpins all messages in chat
    :param msg: Message telegram object
    :return:
    """
    await msg.chat.unpin_all_messages()

