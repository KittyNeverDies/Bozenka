import git

from aiogram.types import *

from bozenka.instances.telegram.utils.callbacks_factory import *
from bozenka.instances.telegram.utils.keyboards import *
from bozenka.instances.telegram.utils.simpler import list_of_features
from bozenka.instances.version import is_updated, build


async def inline_start(call: CallbackQuery):
    """
    Query, what shows back menu of /start
    :param call:
    :return:
    """
    await call.message.edit_text(
        """
        Привет 👋
Я - бозенька, бот с открытым исходным кодом, который поможет тебе в различных задачах. 

Вот что ты можешь сделать с помощью меню:
• Добавить в чат: добавляет меня в групповой чат, чтобы я мог выполнять свои функции внутри него.
• Функционал: показывает список доступных функций и команд, которые я могу выполнить.
• О разработчиках: предоставляет информацию о команде разработчиков, которые создали и поддерживают этого бота.
• О запущенном экземпляре: выводит информацию о текущей версии и состоянии запущенного экземпляра бота.
• Начать диалог с ИИ: позволяет начать диалог с искусственным интеллектом, который может отвечать на вопросы и предоставлять информацию.
• Генерация изображений: позволяет сгенерировать изображения на основе заданных параметров и промта

Вот нужные ссылки обо мне:
• <a href='https://t.me/bozodevelopment'>Канал с новостями об разработке</a>
• <a href='https://github.com/kittyneverdies/bozenka/'>Исходный код на Github</a>

Чтобы воспользоваться какой-либо функцией, просто нажми на соответствующую кнопку ниже. 
Если у тебя возникнут вопросы или проблемы, не стесняйся обратиться к команде разработчиков или написать в обсуждении телеграм канала. 
Удачного использования!
        """,
        reply_markup=start_keyboard(),
        disable_web_page_preview=True
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
    await call.message.edit_text("""
Бозенька - это мультифункциональный (в будущем кроссплатформенный) бот.\n
Он умеет работать с групповыми чатами и готовыми нейронными сетями для генерации текста и изображений.
Бозенька разрабатывается коммандой, которая состоит на данный момент из одного человека.\n
Исходный код проекта\n
Исходный код находится под лицензией GPL-3.0, исходный код проекта можно посмотреть всегда <a href="https://github.com/kittyneverdies/bozenka/">здесь</a>
Канал с новостями разработки находится <a href="https://t.me/bozodevelopment">здесь</a>
    """, reply_markup=kb, disable_web_page_preview=True)


async def inline_about_instance(call: CallbackQuery):
    """
    Query, what shows information about runned instance
    :param call:
    :return:
    """
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Вернуться 🔙", callback_data="back")
    ]])
    me = await call.message.bot.get_me()
    update_status = {False: "требуется обновление бота 🔼",
                     True: "обновление не требуется, последняя версия ✅"}
    await call.message.edit_text(
        f"Информация об данном запущенном экземпляре бозеньки:\n"
        f"Аккаунт бота: {me.mention_html()}\n"
        f"Запущенная версия бота <code>{build}</code>\n",
        f"Нужно ли обновление: {update_status[is_updated]}",
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
    kb.button(text="Добавить в ваш груповой чат 🔌",
              url="https://t.me/"
                  f"{me.username}?"
                  "startgroup&"
                  "admin=promote_members+delete_messages+restrict_members+invite_users+pin_messages+manage_video_chats")
    kb.row(InlineKeyboardButton(text="Вернуться 🔙", callback_data="back"))

    # Answering
    await call.message.edit_text("Чтобы добавить бозеньку в ваш групповой чат, нажмите на кнопку под сообщением:",
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
