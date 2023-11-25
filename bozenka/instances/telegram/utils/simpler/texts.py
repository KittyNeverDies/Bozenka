from typing import List

import g4f
from g4f import Provider


class BaseFeature:
    """
    Basic class of Feature.
    Have inside desription, name, callback name,
    """
    def __init__(self, name: str, description: str, callback_name: str):
        self.name = name
        self.description = description
        self.callback_name = callback_name


gpt4free_providers = {
    "AItianhu": ["gpt-3.5-turbo", "gpt-4"],
    "Acytoo": ["gpt-3.5-turbo"],
    "AiService": ["gpt-3.5-turbo"],
    "Aichat": ["gpt-3.5-turbo"],
    "Ails": ["gpt-3.5-turbo"],
    "Bard": ["palm"],
    "Bing": ["gpt-4"],
    "ChatgptAi": ["gpt-4"],
    "ChatgptLogin": ["gpt-3.5-turbo"],
    "DeepAi": ["gpt-3.5-turbo"],
    "DfeHub": ["gpt-3.5-turbo"],
    "EasyChat": ["gpt-3.5-turbo"],
    "Forefront": ["gpt-3.5-turbo"],
    "GetGpt": ["gpt-3.5-turbo"],
    "H2o": ["falcon-40b", "falcon-7b", "llama-13b"],
    "Liaobots": ["gpt-3.5-turbo", "gpt-4"],
    "Lockchat": ["gpt-3.5-turbo", "gpt-4"],
    "Opchatgpts": ["gpt-3.5-turbo"],
    "Raycast": ["gpt-3.5-turbo", "gpt-4"],
    "Theb": ["gpt-3.5-turbo"],
    # Vercel, biggest part of list
    "Vercel": [
        "gpt-3.5-turbo",
        "claude-instant-v1",
        "claude-v1",
        "claude-v2",
        "command-light-nightly",
        "command-nightly",
        "gpt-neox-20b",
        "oasst-sft-1-pythia-12b",
        "oasst-sft-4-pythia-12b-epoch-3.5",
        "santacoder",
        "bloom",
        "flan-t5-xxl",
        "code-davinci-002",
        "gpt-3.5-turbo-16k",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0613",
        "text-ada-001",
        "text-babbage-001",
        "text-curie-001",
        "text-davinci-002",
        "text-davinci-003",
        "llama13b-v2-chat",
        "llama7b-v2-chat"
    ],
    "Wewordle": ["gpt-3.5-turbo"],
    "You": ["gpt-3.5-turbo"],
    "Yqcloud": ["gpt-3.5-turbo"]
}

list_of_features = {
    "Admins": [
        BaseFeature(
            name="Закреп 📌",
            description="<b>Закреп</b>📌"
                        "\nДанная функция включает команды:"
                        "/pin - закрепляет сообщение"
                        "/unpin - открепляет сообщение"
                        "/unpin_all - открепляет все сообщения, которые видит бот"
                        "Для исполнения <b>требует соответсвующих прав от пользователя и их наличие у бота.</b>",
            callback_name="pins"
        ),
        BaseFeature(
            name="Модерация чата 🕵️",
            description="<b>Модерация чата</b>🕵️\nДанная настройка включает следущие комманды:"
                        "\n/ban [время блокировки] [причина блокировки] - блокировка пользователя"
                        "\n/unban - разблокировка пользователя\n"
                        "/mute [время мута] [причина мута] - мут пользователя "
                        "/unmute - Размут пользователя\n"
                        "Время обозначается как:"
                        "1h - один час, "
                        "1d - один день, "
                        "1m - одна минута, "
                        "1s - одна секунда\n"
                        "Для того, "
                        "чтобы выполнить одну из комманд по отношению к пользователю, "
                        "ответьте на сообщение пользователя и используйте команду\n"
                        "Для исполнения <b>требует соответсвующих прав от пользователя и их наличие у бота.</b>",
            callback_name="moderation"
        ),
        BaseFeature(
            name="Работа с Форумом 💬",
            description="<b>Работа с Форумом</b>💬\nДанная настройка включает следущие комманды:\n"
                        "/open - открывают тему форума\n"
                        "/close - закрывают тему форума\n"
                        "/open_general - открывают основную тему форума\n"
                        "/close_general - закрывает основную тему форума\n"
                        "/hide_general - прячет основную тему форума\n"
                        "/show_general - показывает основную тему форума\n"
                        "Для исполнения <b>требует соответсвующих прав от пользователя и их наличие у бота. Также должен быть"
                        "включен форум</b>",
            callback_name="topics"
        ),
        BaseFeature(
            name="Приглашения в Чат ✉",
            description="<b>Генератор приглашения в Чат ✉</b>\n"
                        "Разрешает использование комманды /invite в чате, для созданния приглашений.\n"
                        "Для исполнения <b>требует соответсвующих прав от пользователя и их наличие у бота.</b>",
            callback_name="invites"
        )
    ],
    "Members": [
        BaseFeature(
            name="Приветсвенные сообщения 👋",
            description="<b>Приветсвенные сообщения 👋</b>"
                        "\nПриветсвенные сообщения новым и ушедшим пользователям.",
            callback_name="welcome"
        ),
        BaseFeature(
            name="Оповещение о муте 📬",
            description="<b>Оповещение о муте 📬</b>"
                        "\nОповещает пользователя в личных сообщениях, что тот был: замучен, размучен, забанен, разбанен",
            callback_name="notify",
        )
    ],
    "Devs": [
        BaseFeature(
            name="Функция Привет 👋",
            description="<b>Функция `Привет` </b>👋"
                        "\nБот будет отвечать на комманды "
                        "/hi, /hello, /privet и т.п., отвечая приветсвием на сообщение пользователя.",
            callback_name="hi"
        ),
        BaseFeature(
            name="ИИ ЧатБот 🤖",
            description="<b>ИИ ЧатБот </b>🤖"
                        "Есть поддержка провайдеров из Gpt4Free\n"
                        "Есть поддержка моделей Gpt4All"
                        "\nНаходится в разработке, планируется в будущем. Следите за обновлениями 😘",
            callback_name="gtm"
        ),
        BaseFeature(
            name="Генерация изображений 📸",
            description="<b>Генерация изображений </b>🤖"
                        "\nНаходится в разработке, планируется в будущем. Следите за обновлениями 😘",
            callback_name="gpm"
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


def generate_gpt4free_providers():
    """
    Generates list of g4f providers
    :return:
    """
    provider = {}
    for prov in g4f.Provider.__all__:
        if prov != "BaseProvider":
            exec(f"provider['{prov}']=g4f.Provider.{prov}")
    result = {}
    for check in provider:
        if provider[check].working:
            result[check] = provider[check]
    return result


gpt_categories = [
    "Gpt4Free",
    "Gpt4All",
    "StableLM",
    "H20Gpt",
    "RWKV"
]
en_cmds = {}

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
    "ban_5": "Ошибка ❌\n"
             "Этот пользователь уже находится в бане.",
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
    ("start", "Command to start work with bozenka the bot"),
    ('setup', 'Command to setup bozenka work in chat'),
    ("ban", "Command to ban user in chat"),
    ('unban', 'Command to unban user in chat'),
    ('mute', 'Command to mute user in chat'),
    ('unmute', 'Command to unmute user in chat'),
    ('pin', 'Pin fast any message in chat'),
    ('unpin', 'Unpin fast any message in chat'),
    ('close', 'Close fast topic (not general) in chat'),
    ('open', 'Open fast topic (not general) in chat'),
    ('hide_general', 'Hide general topic in chat'),
    ('show_general', 'Show general topic in chat'),
    ("close_general", 'Closes general topic in chat'),
    ("open_general", 'Opens general topic in chat'),
    ('conversation', 'Starts conversation with gpt'),
    ('invite', 'Generates invite into this chat'),
    ('about', 'Sends information about bozenka'),
    ('hi', 'Sends welcome message')
}

translations = {
    "ru": ru_cmds,
    "en": en_cmds
}
