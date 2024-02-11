from aiogram import F
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bozenka.features.main import BasicFeature
from bozenka.instances.customizable_features_list import categorized_customizable_features, text_transcription
from bozenka.instances.telegram.utils.callbacks_factory import HelpCategory, HelpBackCategory, HelpFeature, HelpBack
from bozenka.features.user.text_generation import gpt_categories_keyboard
from bozenka.instances.current_version import build, is_updated

telegram_main_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Добавить в ваш групповой чат 🔌", callback_data="addtochat")],
            [InlineKeyboardButton(text="Информация об функционале бота 🔨", callback_data="functional")],
            [InlineKeyboardButton(text="Об данном проекте ℹ️", callback_data="aboutdevs")],
            [InlineKeyboardButton(text="О данном запущенном экзепляре ℹ️", callback_data="aboutbot")],
            [InlineKeyboardButton(text="Начать диалог с текстовым ИИ 🤖", callback_data="dialogai")],
            [InlineKeyboardButton(text="Начать генерацию изображений 🖼", callback_data="dialogimage")],
        ]
    )


# Help related keyboards
def main_help_keyboard() -> InlineKeyboardMarkup:
    """
    Generate keyboard for /help command
    :return: InlineKeyboardMarkup
    """
    kb = InlineKeyboardBuilder()
    for category in categorized_customizable_features:
        kb.row(InlineKeyboardButton(text=text_transcription[category],
                                    callback_data=HelpCategory(category_name=category).pack()))

    return kb.as_markup()


def help_category_keyboard(category: str) -> InlineKeyboardMarkup:
    """
    Generate keyboard for one of categories
    :param category: Category name
    :return: InlineKeyboardMarkup
    """
    kb = InlineKeyboardBuilder()
    for setting in categorized_customizable_features[category]:
        kb.row(InlineKeyboardButton(text=setting.telegram_setting_name,
                                    callback_data=HelpFeature(
                                        feature_index=categorized_customizable_features[category].index(setting),
                                        feature_category=category
                                    ).pack()))
    kb.row(InlineKeyboardButton(text="🔙 Назад к списку категорий",
                                callback_data=HelpBack(back_to="category").pack()))
    return kb.as_markup()


def help_feature_keyboard(category: str) -> InlineKeyboardMarkup:
    """
    Just button for function of /help
    :param category: Category name
    :return: InlineKeyboardMarkup
    """
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад к списку функций",
                              callback_data=HelpBackCategory(category_name=category).pack())]
    ])
    return kb


class Start(BasicFeature):
    """
    A class of /start command
    All staff related to it will be here
    """

    #   There starting a help category of handlers
    #   It's related to one of menus
    #   Showing information about features, will be remade later :D

    @staticmethod
    async def back_help_categories_handler(call: CallbackQuery, callback_data: HelpBack) -> None:
        """
        Query, what shows list of  features to get support back.
        :param call: CallbackQuery object
        :param callback_data: Helpback class
        :return: None
        """
        await call.message.edit_text("Выберите категорию, по которой нужна помощь:",
                                     reply_markup=main_help_keyboard())
        await call.answer()

    @staticmethod
    async def help_features_handler(call: CallbackQuery, callback_data: HelpCategory | HelpBackCategory) -> None:
        """
        Handler of CallbackQuery, what shows list of  features to get support.
        :param call: CallbackQuery object
        :param callback_data: HelpCategory or HelpBack class
        :return: None
        """
        await call.message.edit_text("Выберите функцию, по которой нужна помощь",
                                     reply_markup=help_category_keyboard(category=callback_data.category_name))
        await call.answer()

    @staticmethod
    async def feature_info_handler(call: CallbackQuery, callback_data: HelpFeature) -> None:
        """
        Handler of CallbackQuery, what shows information about bozenka feature
        :param call: CallbackQuery ojbect
        :param callback_data: HelpFeature object
        :return: None
        """
        await call.message.edit_text(
            categorized_customizable_features[callback_data.feature_category][callback_data.feature_index]. telegram_setting_description,
            reply_markup=help_feature_keyboard(category=callback_data.feature_category))
        await call.answer()

    @staticmethod
    async def help_menu_handler(call: CallbackQuery) -> None:
        """
        Handler of CallbackQuery, what shows menu of help
        :param call: CallbackQuery object
        :return: None
        """
        await call.message.edit_text("Выберите категорию функций, по которой вам нужна помощь 🤖",
                                     reply_markup=main_help_keyboard())
        await call.answer()

    @staticmethod
    async def add_to_menu_handler(call: CallbackQuery) -> None:
        """
        Handler of CallbackQuery, what shows a link to add bozenka into user group chat
        :param call: CallbackQuery object
        :return: None
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
        await call.answer()

    @staticmethod
    async def about_instance_callback_handler(call: CallbackQuery) -> None:
        """
        Handler of CallbackQuery, what shows information about current running instance
        :param call: CallbackQuery object
        :return: Nothing
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
        await call.answer()

    @staticmethod
    async def about_developers_handler(call: CallbackQuery) -> None:
        """
        Handler of CallbackQuery, what shows information about bozenka & it's development
        :param call: CallbackQuery object
        :return: Nothing
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

    @staticmethod
    async def start_dialog_handler(call: CallbackQuery) -> None:
        """
        Handler of CallbackQuery, what shows list of Categories, avaible to use as chatbot
        :param call: CallbackQuery object
        :return: Nothing
        """
        await call.message.edit_text("Пожалуста, выберите сервиc / библиотеку, через которую вы будете общаться",
                                     reply_markup=gpt_categories_keyboard
                                     (user_id=call.from_user.id))

    @staticmethod
    async def start_callback_handler(call: CallbackQuery) -> None:
        """
        /start command function handler. Just back it by clicking on button.
        Shows menu and basic information about bozenka
        :param call: Message telegram object
        :return: Nothing
        """
        await call.message.edit_text("""
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
    """, reply_markup=telegram_main_menu, disable_web_page_preview=True)

    @staticmethod
    async def start_cmd_handler(msg: Message) -> None:
        """
        /start command function handler
        Shows menu and basic information about bozenka
        :param msg: Message telegram object
        :return: Nothing
        """
        await msg.answer("""
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
    """, reply_markup=telegram_main_menu, disable_web_page_preview=True)

    """
    Telegram feature settings
    """
    # Telegram feature settings
    telegram_setting_in_list = False
    telegram_category = None
    telegram_commands: dict[str: str] = {"start": "Command to start work with bozenka the bot"}
    telegram_cmd_avaible = True  # Is a feature have a commands
    telegram_message_handlers = [
            [start_cmd_handler, [Command(commands=["start"]), F.chat.type == ChatType.PRIVATE]],
        ]
    telegram_callback_handlers = [
            # Start menu
            [start_dialog_handler, [F.data == "dialogai"]],
            [add_to_menu_handler, [F.data == "addtochat"]],
            [about_developers_handler, [F.data == "aboutdevs"]],
            [about_instance_callback_handler, [F.data == "aboutbot"]],
            [start_callback_handler, [F.data == "back"]],
            # Help menu
            [help_menu_handler, [F.data == "functional"]],
            [feature_info_handler, [HelpFeature.filter()]],
            [help_features_handler, [HelpBackCategory.filter()]],
            [help_features_handler, [HelpCategory.filter()]],
            [help_menu_handler, [HelpBack.filter(F.back_to == "category")]]
        ]
