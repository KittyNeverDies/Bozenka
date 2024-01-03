from aiogram.enums import ChatType
from aiogram.types import Message as Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bozenka.instances.telegram.utils.keyboards import help_keyboard, start_keyboard


async def start_cmd(msg: Message):
    """
    /start command function
    :param msg:
    :return:
    """
    await msg.answer(
        'Привет, пользователь, я - Бозенька 👋\n' 
        'Я мультизадачный телеграм (в будущем кросс-платформенный) бот с открытым исходным кодом, разрабатываемый <b>Bozo Developement</b>\n' 
        f'Выберите, что будете делать, {msg.from_user.mention_html(name="пользователь")}.',
        reply_markup=start_keyboard()
    )
