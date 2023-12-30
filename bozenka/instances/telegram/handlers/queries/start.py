from aiogram.types import *

from bozenka.instances.telegram.utils.callbacks_factory import *
from bozenka.instances.telegram.utils.keyboards import *
from bozenka.instances.telegram.utils.simpler import list_of_features


async def inline_start(call: CallbackQuery):
    """
    Query, what shows back menu of /start
    :param call:
    :return:
    """
    await call.message.edit_text(
        'Привет, пользователь, я - Бозенька 👋\n'
        'Я мультизадачный телеграм (в будущем кросс-платформенный) бот с открытым исходным кодом, разрабатываемый <b>Bozo Developement</b>\n'
        f'Выберите, что будете делать, {call.from_user.mention_html(name="пользователь")}.',
        reply_markup=start_keyboard()
    )


async def inline_start_chatbot(call: CallbackQuery):
    """
    Query, what shows list of Categories, avaible to use as chatbot
    :param call:
    :return:
    """
    await call.message.edit_text("Пожалуста, выберите сервиc / библиотеку, через которую вы будете общаться",
                                 reply_markup=gpt_categories_keyboard
                                 (user_id=call.from_user.id))


async def inline_help(call: CallbackQuery):
    """
    Query, what shows information about bozenka and it's development
    :param call:
    :return:
    """
    kb = InlineKeyboardMarkup(inline_keyboard=[[

    ]])
    await call.message.edit_text("Выберите категорию, по которой нужна помощь:",
                                 reply_markup=help_keyboard())


async def inline_about_developers(call: CallbackQuery):
    """
    Query, what shows information about bozenka and it's development
    :param call:
    :return:
    """
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Вернуться 🔙", callback_data="back")
    ]])
    await call.message.edit_text("Бозенька - это мультифункциональный (в будущем кроссплатформенный бот)."
                                 "Он умеет работать с группами и готовыми нейронными сетями\n"
                                 "Бозеьнка разработавается коммандой, состаящей из одного человека, сам проект был изначально для развития моих навыков в Python\n"
                                 "Исходный код находится под лицензией <b>GPL-3.0</b>. Исходный код проекта всегда будет открыт и доступен.\n"
                                 "Исходный код проекта всегда можно найти по этой ссылке: https://github.com/kittyneverdies/bozenka/\n"
                                 "Исходный код бота для телеграма можно найти по этой ссылке: https://github.com/kittyneverdies/bozenka/branch/telegram",
                                 reply_markup=kb)


async def inline_add_to_chat(call: CallbackQuery):
    """
    Query, what shows a link to add bozenka into user chat
    :param call:
    :return:
    """
    # Getting bot
    me = await call.message.bot.me()
    # Generating special keyboard
    kb = InlineKeyboardBuilder()
    kb.button(text="Добавить в чат", url="https://t.me/"
                                         f"{me.username}?"
                                         "startgroup&"
                                         "admin=promote_members+delete_messages+restrict_members+invite_users+pin_messages+manage_video_chats")
    kb.row(InlineKeyboardButton(text="Вернуться 🔙", callback_data="back"))
    # Answering
    await call.message.edit_text("Чтобы добавить бозеньку в чат, нажмите на кнопку под сообщением:",
                                 reply_markup=kb.as_markup())


async def inline_help_features(call: CallbackQuery, callback_data: HelpCategory):
    """
    Query, what shows list of  features to get support.
    :param call:
    :param callback_data:
    :return:
    """
    await call.message.edit_text("Выберите функцию, по которой нужна помощь",
                                 reply_markup=help_category_keyboard(category=callback_data.category_name))


async def inline_back_help_features(call: CallbackQuery, callback_data: HelpBackCategory):
    """
    Query, what shows list of  features to get support.
    :param call:
    :param callback_data:
    :return:
    """
    await call.message.edit_text("Выберите функцию, по которой нужна помощь",
                                 reply_markup=help_category_keyboard(category=callback_data.back_to_category))


async def inline_back_help_categories(call: CallbackQuery, callback_data: HelpBack):
    """
    Query, what shows list of  features to get support back.
    :param call:
    :param callback_data:
    :return:
    """
    await call.message.edit_text("Выберите категорию, по которой нужна помощь:",
                                 reply_markup=help_keyboard())


async def inline_help_feature(call: CallbackQuery, callback_data: HelpFeature):
    """
    Query, what shows list of  features to get support.
    :param call:
    :param callback_data:
    :return:
    """
    await call.message.edit_text(
        list_of_features[callback_data.feature_category][callback_data.feature_index].description,
        reply_markup=help_feature_keyboard(category=callback_data.feature_category))
