import g4f
from g4f import Provider

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

desc = {
        # Admin features list
        "mods-features": "<b>Модерация чата</b>🕵️\nДанная настройка включает следущие комманды:" 
                         "\n/ban [время] [причина] - блокировка пользователя" 
                         "\n/unban - разблокировка пользователя\n" 
                         "/mute [время] [причина] - мут пользователя "
                         "(1h - один час, 1d - один день, 1m - одна минута, 1s - одна секунда)\n"
                         "/unmute - Размут пользователя\n Для того, "
                         "чтобы выполнить одну из комманд по отношению к пользователю, " 
                         "ответьте на сообщение пользователя и используйте команду\n"
                         "Для исполнения <b>требует соответсвующих прав от пользователя и их наличие у бота.</b>",
        "invite-features": "<b>Генератор приглашения в Чат ✉</b>\n"
                           "Разрешает использование комманды /invite в чате, для созданния приглашений.\n"
                           "Для исполнения <b>требует соответсвующих прав от пользователя и их наличие у бота.</b>",
        "unpin-features": "<b>Закреп</b>"
                          "\nДанная функция включает команды:"
                          "/pin - закрепляет сообщение"
                          "/unpin - открепляет сообщение"
                          "/unpin_all - открепляет все сообщения, которые видит бот"
                          "Для исполнения <b>требует соответсвующих прав от пользователя и их наличие у бота.</b>",
        # User features list
        "greetings-features": "<b>Приветсвенные сообщения 👋</b>"
                              "\nПриветсвенные сообщения новым и ушедшим пользователям.",
        "mute-info-features": "<b>Оповещение о муте 📬</b>"
                              "\nОповещает пользователя в личных сообщениях, что тот был:"
                              "\n- Замучен\n-Размучен\n-Забанен\n-Разбанен\n",
        "results-dm-features": "<b>Результаты команд в личных сообщениях📑</b>"
                               "\nРезультат использования команды будет отправлен не в чат, "
                               "в котором была произведена комманда, а в личные сообщения пользователя.",
        "topics-features": "<b>Работа с форумом</b>",
        # Testing features list
        "hi-features": "<b>Функция `Привет` </b>👋"
                       "\nБот будет отвечать на комманды "
                       "/hi, /hello, /privet и т.п., отвечая приветсвием на сообщение пользователя.",
        "ai-features": "<b>ИИ 🤖</b>"
                       "\nНаходится в разработке, планируется в будущем. Следите за обновлениями 😘",
        "photo-generator-features": "Генерация изображений 📸"
                                    "\nНаходится в разработке, планируется в будущем. Следите за обновлениями 😘",
}
