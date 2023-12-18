from aiogram.types import Message

from bozenka.instances.telegram.utils.keyboards import delete_keyboard


async def help_ban(msg: Message):
    """
    Shows help message for /ban
    :param msg:
    """
    await msg.answer("Использование:\n"
                     "<pre>/ban [время блокировки] [причина блокировки]</pre>\n"
                     "Ответьте на сообщение, чтобы заблокировать пользователя",
                     reply_markup=delete_keyboard(msg.from_user.id))


async def help_unban(msg: Message):
    """
    Shows help message for /unban
    :param msg:
    """
    await msg.answer("Использование:\n"
                     "<pre>/unban</pre>\n"
                     "Ответьте на сообщение, чтобы разблокировать пользователя",
                     reply_markup=delete_keyboard(msg.from_user.id))


async def help_mute(msg: Message):
    """
    Shows help message for /mute
    :param msg:
    """
    await msg.answer("Использование:\n"
                     "<pre>/mute [время мута] [причина мута]</pre>\n"
                     "Ответьте на сообщение, чтобы замутить пользователя",
                     reply_markup=delete_keyboard(msg.from_user.id))


async def help_unmute(msg: Message):
    """
    Shows help message for /unmute
    :param msg:
    """
    await msg.answer("Использование:\n"
                     "<pre>/unmute</pre>\n"
                     "Ответьте на сообщение, чтобы замутить пользователя",
                     reply_markup=delete_keyboard(msg.from_user.id))


async def help_pin(msg: Message):
    """
    Shows help message for /mute
    :param msg:
    """
    await msg.answer("Использование:\n"
                     "<pre>/pin</pre>\n"
                     "Ответьте на сообщение, чтобы закрепить сообщение",
                     reply_markup=delete_keyboard(msg.from_user.id))


async def help_unpin(msg: Message):
    """
    Shows help message for /mute
    :param msg:
    """
    await msg.answer("Использование:\n"
                     "<pre>/unpin</pre>\n"
                     "Ответьте на сообщение, чтобы открепить сообщение",
                     reply_markup=delete_keyboard(msg.from_user.id))

