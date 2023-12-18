from aiogram.enums import ChatType
from aiogram.types import Message as Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bozenka.instances.telegram.utils.keyboards import start_keyboard_builder, help_keyboard


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
        reply_markup=start_keyboard_builder.as_markup(one_time_keyboard=True, resize_keyboard=True)
    )


async def features_list(msg: Message):
    """
    Shows features list from reply keyboard
    :param msg:
    :return:
    """
    await msg.answer("Выберите категорию, по которой нужна помощь:",
                     reply_markup=help_keyboard())


async def about_devs(msg: Message):
    """
    Shows info about devs from reply keyboard
    :param msg:
    :return:
    """
    await msg.answer("Бозеьнка разработавается коммандой, состаящей из одного человека.\n"
                     "Исходный код находится под лицензией <b>GPL-3.0</b>. Исходный код проекта всегда будет открыт и доступен.\n"
                     "Исходный код проекта всегда можно найти тут: https://github.com/kittyneverdies/bozenka/")
    await msg.delete()


async def add_to_chat(msg: Message):
    """
    Sends link for adding bot into chat
    :param msg:
    :return:
    """
    # Getting bot
    me = await msg.bot.me()
    # Generating special keyboard
    kb = InlineKeyboardBuilder()
    kb.button(text="Добавить в чат", url="https://t.me/"
                                         f"{me.username}?"
                                         "startgroup&"
                                         "admin=promote_members+delete_messages+restrict_members+invite_users+pin_messages+manage_video_chats")
    # Answering
    await msg.answer("Чтобы добавить бозеньку в чат, нажмите на кнопку под сообщением:",
                     reply_markup=kb.as_markup())
    await msg.delete()
