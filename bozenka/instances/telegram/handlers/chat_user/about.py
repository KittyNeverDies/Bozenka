import logging

from aiogram.types import Message as Message
from bozenka.instances.telegram.utils.keyboards import about_keyboard


async def about(msg: Message):
    """
    Sending information about bot by command `/about`
    Will be deleted by its use
    :param msg:
    :return:
    """
    logging.log(msg=f"Sending about information for user_id={msg.from_user.id}",
                level=logging.INFO)
    await msg.answer("Кто я? 👁"
                     "\nЯ - многозадачный бот, разрабатываемый Bozo Developement и всё ещё нахожусь в разработке"
                     "\n(Ссылочки на нас внизу короче)☺️",
                     reply_markup=about_keyboard.as_markup())
