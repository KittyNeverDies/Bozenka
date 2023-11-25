from aiogram.types import Message as Message
from bozenka.instances.telegram.utils.simpler import ru_cmds
from bozenka.instances.telegram.utils.keyboards import setup_keyboard


async def setup_cmd(msg: Message):
    """
    /setup handler
    :param msg:
    :return:
    """
    await msg.answer("Привет владелец чата 👋\n"
                     "Чтобы меня настроить, используй меню под данным сообщением",
                     reply_markup=setup_keyboard())


async def after_adding(msg: Message):
    """
    Send message after adding bozenka into group chat
    :param msg:
    :return:
    """
    await msg.answer("Здраствуйте администраторы чата 👋\n"
                     "Я - <b>бозенька</b>, мультифункциональный бот, разрабатываемый Bozo Developement\n"
                     "Выдайте мне <b>полные права администратора</b> для моей полной работы."
                     "Чтобы настроить функционал, используйте /setup или кнопку под сообщением")
