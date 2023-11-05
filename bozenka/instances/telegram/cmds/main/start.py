from aiogram.types import Message as Message

from bozenka.instances.telegram.utils.keyboards import start_keyboard


async def start_cmd(msg: Message):
    """
    /start command function
    :param msg:
    :return:
    """
    await msg.answer(
        'Привет, пользователь, я - Бозенька 👋\n' 
        'Я мультизадачный телеграм бот, разрабатываемый Bozo Developement\n' 
        f'Выберите, что будете делать, {msg.from_user.mention_html()}',
        reply_markup=start_keyboard.as_markup()
    )


async def features_list(msg: Message):
    """
    Shows features list from reply keyboard
    :param msg:
    :return:
    """
    await msg.answer("List will be soon")


async def about_devs(msg: Message):
    """
    Shows info about devs from reply keyboard
    :param msg:
    :return:
    """
    await msg.answer("Info about developers will be added soon")


async def add_to_chat(msg: Message):
    """
    Sends link for adding bot into chat
    :param msg:
    :return:
    """
    await msg.answer("Will be soon")

