from dataclasses import dataclass
from typing import List, Any

import g4f
from g4f import Provider
from g4f.Provider import RetryProvider
from varname import nameof

from bozenka.database.tables.telegram import TelegramChatSettings


@dataclass
class BaseFeature:
    """
    Basic class of Feature.
    Have inside desription, name, callback name,
    """
    name: str
    description: str
    callback_name: str
    settings_name: str
    db_name: Any


@dataclass
class BaseCategory:
    """
    Basic class of Feature category
    Have inside category name, callbackname
    """
    name: str
    callback_name: str


# List of categories, avaible in bot
list_of_categories = [
    BaseCategory(name="Администраторы 👮‍♂", callback_name="Admins"),
    BaseCategory(name="Пользователи 👤", callback_name="Members"),
    BaseCategory(name="В разработке 👨‍💻", callback_name="Devs")
]

# List of features, avaible in bot
list_of_features = {
    "Admins": [
        BaseFeature(
            name="Закреп 📌",
            description="<b>Закреп</b>📌"
                        "\nДанная функция включает команды:"
                        "<pre>/pin - закрепляет сообщение\n"
                        "/unpin - открепляет сообщение\n"
                        "/unpin_all - открепляет все сообщения, которые видит бот</pre>\n"
                        "Для исполнения <b>требует соответсвующих прав от пользователя и их наличие у бота.</b>",
            callback_name="pins",
            settings_name="pins",
            db_name=TelegramChatSettings.pins
        ),
        BaseFeature(
            name="Модерация чата 🕵️",
            description="<b>Модерация чата</b>🕵️\nДанная настройка включает следущие комманды:"
                        "\n<pre>/ban [время блокировки] [причина блокировки] - блокировка пользователя"
                        "\n/unban - разблокировка пользователя\n"
                        "/mute [время мута] [причина мута] - мут пользователя\n"
                        "/unmute - Размут пользователя</pre>\n"
                        "Время обозначается как:"
                        "<pre>1h - один час, "
                        "1d - один день, "
                        "1m - одна минута, "
                        "1s - одна секунда</pre>\n"
                        "Для того, "
                        "чтобы выполнить одну из комманд по отношению к пользователю, "
                        "ответьте на сообщение пользователя и используйте команду\n"
                        "Для исполнения <b>требует соответсвующих прав от пользователя и их наличие у бота.</b>",
            callback_name="moderation",
            settings_name="moderation",
            db_name=TelegramChatSettings.moderation
        ),
        BaseFeature(
            name="Работа с Форумом 💬",
            description="<b>Работа с Форумом</b>💬\nДанная настройка включает следущие комманды:\n"
                        "<pre>/open - открывают тему форума\n"
                        "/close - закрывают тему форума\n"
                        "/open_general - открывают основную тему форума\n"
                        "/close_general - закрывает основную тему форума\n"
                        "/hide_general - прячет основную тему форума\n"
                        "/show_general - показывает основную тему форума</pre>\n"
                        "Для исполнения <b>требует соответсвующих прав от пользователя и их наличие у бота. Также должен быть"
                        "включен форум</b>",
            callback_name="topics",
            settings_name="topics",
            db_name=TelegramChatSettings.topics
        ),
        BaseFeature(
            name="Приглашения в Чат ✉",
            description="<b>Генератор приглашения в Чат ✉</b>\n"
                        "Разрешает использование комманды <code>/invite</code> в чате, для созданния приглашений.\n"
                        "Для исполнения <b>требует соответсвующих прав от пользователя и их наличие у бота.</b>",
            callback_name="invites",
            settings_name="invite_generator",
            db_name=TelegramChatSettings.invite_generator
        ),
        BaseFeature(
            name="Результаты в лс ✉",
            description="<b>Результаты в личных сообщениях ✉</b>\n"
                        "Отправляет все результаты команд модерации в личные сообщения пользователя\n"
                        "Никаких особых прав у бота не требует.",
            callback_name="results_in_dm",
            settings_name="results_in_dm",
            db_name=TelegramChatSettings.results_in_dm
        ),
        BaseFeature(
            name="Оповещение об ограничении 🗯",
            description="<b>Оповещение об ограничении 🗯</b>\n"
                        "Отправляет оповещение пользователю об его муте, бане\n"
                        "Никаких особых прав у бота не требует.",
            callback_name="restrict_notification",
            settings_name="restrict_notification",
            db_name=TelegramChatSettings.restrict_notification
        )
    ],
    "Members": [
        BaseFeature(
            name="Приветсвенные сообщения 👋",
            description="<b>Приветсвенные сообщения 👋</b>"
                        "\nПриветсвенные сообщения новым и ушедшим пользователям.",
            callback_name="welcome",
            settings_name="welcome_messages",
            db_name=TelegramChatSettings.welcome_messages
        ),
        BaseFeature(
            name="Оповещение о муте 📬",
            description="<b>Оповещение о муте 📬</b>"
                        "\nОповещает пользователя в личных сообщениях, что тот был: замучен, размучен, забанен, разбанен",
            callback_name="notify",
            settings_name="restrict_notification",
            db_name=TelegramChatSettings.restrict_notification
        )
    ],
    "Devs": [
        BaseFeature(
            name="Функция Привет 👋",
            description="<b>Функция `Привет` </b>👋"
                        "\nБот будет отвечать на комманды "
                        "/hi, /hello, /privet и т.п., отвечая приветсвием на сообщение пользователя.",
            callback_name="hi",
            settings_name="hi_command",
            db_name=TelegramChatSettings.hi_command
        ),
        BaseFeature(
            name="ИИ ЧатБот 🤖",
            description="<b>ИИ ЧатБот </b>🤖"
                        "\nЕсть поддержка:\n"
                        "- Моделей Gpt4All\n"
                        "- Провайдеров Gpt4Free и моделей\n"
                        "Для использования:\n"
                        "<pre>/conversations</pre>"
                        "\nНаходится в разработке, планируется в будущем. Следите за обновлениями 😘",
            callback_name="gtm",
            settings_name="gpt_conversations",
            db_name=TelegramChatSettings.text_generation
        ),
        BaseFeature(
            name="Генерация изображений 📸",
            description="<b>Генерация изображений </b>🤖"
                        "\nНаходится в разработке, планируется в будущем. Следите за обновлениями 😘",
            callback_name="gpm",
            settings_name="123",
            db_name=TelegramChatSettings.image_generation
        )
    ]

}


def generate_list_of_features(category: str) -> list[BaseFeature]:
    """
    Generates list of features avaible at some category
    made for future auto translate
    :param category:
    :return:
    """
    return list_of_features[category]


ru_cmds = {
    # /info command translation
    "info": "Информация об чате с названием nameofchathere"
            "descr\n"
            "Является chattype isforum requiredinvite\n"
            "Скрытые участники ishiddenmembers, isprotected",
    "chat_types": {"group": "группой", "supergroup": "cупер группой"},
    "forum_type": {True: "и форумом,", False: ", не является форумом,", None: ", не является форумом,"},
    "required_invite": {True: "требуется одобрение заявки на вступление", False: "заявка не требуется.",
                        None: "заявка не требуется."},
    "hidden_members": {True: "присуствуют", False: "отсуствуют", None: "отсуствуют"},
    "isprotected": {True: "пересылать сообщения из группы можно.", False: "пересылать сообщения из группы нельзя.",
                    None: "пересылать сообщения из группы можно."},
    # /hi command translation
    "hi": "Привет, user 👋",
    "user": "пользователь",
    # /invite command translation
    "invite_generation": "<em> Держите ваше приглашение в чат, user 👋</em>",
    "sir": "сэр",
    # Ban cases
    "ban_1": "Удача ✅\n"
             "Пользователь banned был заблокирован пользователем admin.\n"
             "По причине ban_reason, до даты ban_time",
    "ban_2": "Удача ✅\n"
             "Пользователь banned был заблокирован пользователем admin.\n"
             "По причине ban_reason.",
    "ban_3": "Удача ✅\n"
             "Пользователь banned был заблокирован пользователем admin.",
    "ban_4": "Удача ✅\n"
             "Пользователь banned был заблокирован пользователем admin, до даты ban_time.\n",
    "ban_success": "Успешно заблокирован ✅",
    # Unban cases
    "unban_1": "Удача ✅\n"
               "Пользователь unbanned был разблокирован пользователем admin.\n"
               "По причине reason.",
    "unban_2": "Удача ✅\n"
               "Пользователь unbanned был разблокирован пользователем admin.",
    "unban_3": "Ошибка ❌\n"
               "Этот пользователь не находится в бане.",
    "unban_success": "Успешно разблокирован ✅",
    # Work with topic
    "topic_closed": "Удача ✅\n"
                    "Пользователь user закрыл данное обсуждение.",
    "open_topic": "Удача ✅\n"
                  "Пользователь user открыл данное обсуждение.",
    "close_general": "Удача ✅\n"
                     "Пользователь user закрыл основное обсуждение",
    "open_general": "Удача ✅\n"
                    "Пользователь user открыл основное обсуждение",
    "hide_general": "Удача ✅\n"
                    "Пользователь user скрыл основное обсуждение",
    "show_general": "Удача ✅\n"
                    f"Пользователь user раскрыл основное обсуждение",
    "topic_renamed": "Удача ✅\n"
                     f"Пользователь user переименовал обсуждение <pre>originalthreadname</pre>",
    # GPT cases
    "generate_answer": "Пожалуйста подождите, ответ генерируется ⏰",
    "select_provider": "Выберите пожалуйста одного из провайдеров 👨‍💻",
    "select_provider_message": "Выберите пожалуйста одного из провайдеров 👨‍💻",
    "help_notification": "Это текущая странница 📃",
    "select_provider_page": "Пожалуйста, выберите одного из провайдеров 👨‍💻\n"
                            "Ваша текущая страница это pagecount📄",
    "moved_page": "Перенесли на страницу pagecount📄",
    "finish_gpt4all_message": "Удача ✅\n"
                              "Вы теперь можете спокойно вести диалог 🤖\n"
                              "Чтобы прекратить общение, используйте /cancel",
    "finish_gptfree_message": "Удача ✅\n"
                              "Вы теперь можете спокойно вести диалог 🤖\n"
                              "Вы выбрали модель <pre>modelname</pre>👾, от провайдера <pre>providername</pre>👨‍💻\n"
                              "Чтобы прекратить общение, используйте /cancel ",
    "finish_gpt": "Вы теперь можете спокойно вести диалог 🤖",
    "select_model_message": "Выберите пожалуйста модель ИИ 👾",
    "select_model": "Выберите пожалуйста модель ИИ 👾",
    # No Permission translation
    "no_perms": "Ошибка ❌"
                "У вас нет прав на использование этой комманды 🚫",
    # After adding bot into group message text
    "after_adding": "Здраствуйте администраторы чата 👋\n"
                    "Я - <b>бозенька</b>, мультифункциональный бот, разрабатываемый Bozo Developement\n"
                    "Выдайте мне <b>полные права администратора</b> для моей полной работы."
                    "Чтобы настроить функционал, используйте /setup или кнопку под сообщением",
    # Success
    "success": "Удача ✅"

}

list_of_commands = {
    # Main commands
    ("start", "Command to start work with bozenka the bot"),
    ('setup', 'Command to setup bozenka features in chat'),
    # Moderation commands
    ("ban", "Command to ban user in chat"),
    ('unban', 'Command to unban user in chat'),
    ('mute', 'Command to mute user in chat'),
    ('unmute', 'Command to unmute user in chat'),
    # Work with pins
    ('pin', 'Pin fast any message in chat'),
    ('unpin', 'Unpin fast any message in chat'),
    # Close / open topics
    ('close', 'Close fast topic (not general) in chat'),
    ('open', 'Open fast topic (not general) in chat'),
    ('hide_general', 'Hide general topic in chat'),
    ('show_general', 'Show general topic in chat'),
    ("close_general", 'Closes general topic in chat'),
    ("open_general", 'Opens general topic in chat'),
    # AI related
    ('conversation', 'Starts conversation with text generative ai'),
    ('imagine', 'Starts conversation with image generative ai'),
    # Basic features
    ('invite', 'Generates invite into current chat'),
    ('about', 'Sends information about bozenka'),
    ('hi', 'Sends test welcome message'),
    ('info', 'Get information about chat')
}

translations = {
    "ru": ru_cmds,
}
