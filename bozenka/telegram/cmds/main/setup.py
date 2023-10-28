from aiogram.types import Message as Message
from bozenka.telegram.utils.simpler import ru_cmds
from bozenka.telegram.utils.keyboards import setup_keyboard


async def setup_cmd(msg: Message):
    """
    /setup handler
    :param msg:
    :return:
    """
    await msg.answer("Привет владелец чата 👋\n"
                     "Чтобы меня настроить, используй меню под данным сообщением", reply_markup=setup_keyboard(msg.from_user.id))


async def after_adding(msg: Message):
    """
    Send message after adding bozenka into group chat
    :param msg:
    :return:
    """
    await msg.answer(ru_cmds["after_adding"])
