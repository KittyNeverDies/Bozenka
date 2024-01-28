from aiogram.types import Message as Message
from sqlalchemy.ext.asyncio import async_sessionmaker

from bozenka.instances.telegram.utils.simpler import SolutionSimpler
from bozenka.instances.telegram.utils.keyboards import setup_keyboard


async def setup_cmd(msg: Message):
    """
    /setup handler
    :param msg:
    :param session:
    :return:
    """
    await msg.answer("Привет владелец чата 👋\n"
                     "Чтобы меня настроить, используй меню под данным сообщением",
                     reply_markup=setup_keyboard())


async def group_adding_handler(msg: Message, session_maker: async_sessionmaker):
    """
    Send message after adding bozenka into group chat
    :param msg:
    :param session_maker:
    :return:
    """
    await SolutionSimpler.auto_settings(msg=msg, session=session_maker)
    await msg.answer("Здраствуйте администраторы чата 👋\n"
                     "Я - <b>бозенька</b>, мультифункциональный бот, разрабатываемый Bozo Developement\n"
                     "Выдайте мне <b>полные права администратора</b> для моей полной работы, если не выдали."
                     "Чтобы настроить функционал, используйте /setup или кнопку под сообщением")
