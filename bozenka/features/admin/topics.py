from aiogram import F
from aiogram.enums import ChatType
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from bozenka.database.tables.telegram import TelegramChatSettings
from bozenka.features.main import BasicFeature
from bozenka.instances.telegram.utils.callbacks_factory import CloseThread, OpenThread, DeleteMenu
from bozenka.instances.telegram.filters import UserHasPermissions, BotHasPermissions, IsSettingEnabled
from bozenka.instances.telegram.utils.delete import delete_keyboard
from bozenka.instances.telegram.utils.simpler import SolutionSimpler


# Close / Open thread commands related keyboards
def telegram_close_thread_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """
    Generate menu for /close command
    :param user_id: User_if of member, who closed thread
    :return: InlineKeyboardMarkup
    """
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Окрыть обсуждение 🛠️", callback_data=OpenThread(user_id=user_id).pack())],
        [InlineKeyboardButton(text="Спасибо ✅", callback_data=DeleteMenu(user_id_clicked=str(user_id)).pack())]
    ])
    return kb


def telegram_open_thread_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """
    Generate menu for /open command
    :param user_id: User_if of member, who opened thread
    :return: InlineKeyboardMarkup
    """
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Закрыть обсуждение 🛠️", callback_data=CloseThread(user_id=user_id).pack())],
        [InlineKeyboardButton(text="Спасибо ✅", callback_data=DeleteMenu(user_id_clicked=str(user_id)).pack())]
    ])
    return kb


class Threads(BasicFeature):
    """
    A class of topics / threads related commands
    All staff related to it will be here
    """

    @staticmethod
    async def telegram_close_topic_cmd_handler(msg: Message) -> None:
        """
        /close command function. Closing thread
        :param msg: Message telegram object
        :return: Nothing
        """
        try:
            if msg.message_thread_id:
                await msg.bot.close_forum_topic(chat_id=msg.chat.id, message_thread_id=msg.message_thread_id)
                await msg.answer(
                    f"Удача ✅\n{msg.from_user.mention_html('Этот пользователь')} закрыл данное обсуждение.",
                    reply_markup=telegram_close_thread_keyboard(user_id=msg.from_user.id))
            else:
                await msg.bot.close_general_forum_topic(chat_id=msg.chat.id)
                await msg.answer(
                    f"Удача ✅\n{msg.from_user.mention_html('Этот пользователь')} закрыл основное обсуждение.",
                    reply_markup=telegram_close_thread_keyboard(user_id=msg.from_user.id))
        except TelegramBadRequest as ex:
            if ex.message == "Bad Request: TOPIC_NOT_MODIFIED":
                await msg.answer("Ошибка ❌\nДанное обсуждение уже закрыто.",
                                 reply_markup=telegram_open_thread_keyboard(user_id=msg.from_user.id))

    @staticmethod
    async def telegram_reopen_topic_cmd_handler(msg: Message) -> None:
        """
        /open command function. Opens thread
        :param msg: Message telegram object
        :return: Nothing
        """
        try:
            if msg.message_thread_id:
                await msg.bot.reopen_forum_topic(chat_id=msg.chat.id, message_thread_id=msg.message_thread_id)
                await msg.answer(
                    f"Удача ✅\n{msg.from_user.mention_html('Этот пользователь')} открыл данное обсуждение.",
                    reply_markup=telegram_open_thread_keyboard(user_id=msg.from_user.id))
            else:
                await msg.bot.reopen_general_forum_topic(chat_id=msg.chat.id)
                await msg.answer(
                    f"Удача ✅\n{msg.from_user.mention_html('Этот пользователь')} открыл основное обсуждение.",
                    reply_markup=telegram_open_thread_keyboard(user_id=msg.from_user.id))
        except TelegramBadRequest as ex:
            if ex.message == "Bad Request: TOPIC_NOT_MODIFIED":
                await msg.answer("Ошибка ❌\nДанное обсуждение уже открыто.",
                                 reply_markup=telegram_close_thread_keyboard(user_id=msg.from_user.id))

    @staticmethod
    async def telegram_close_general_topic_cmd_handler(msg: Message) -> None:
        """
        /close_general command function. Closes general thread
        :param msg: Message telegram object
        :return: Nothing
        """
        try:
            await msg.bot.close_general_forum_topic(chat_id=msg.chat.id)
            await msg.answer(f"Удача ✅\n{msg.from_user.mention_html('Этот пользователь')} закрыл основное обсуждение.",
                             reply_markup=telegram_close_thread_keyboard(user_id=msg.from_user.id))
        except TelegramBadRequest as ex:
            if ex.message == "Bad Request: TOPIC_NOT_MODIFIED":
                await msg.answer(f"Ошибка ❌\nДанное обсуждение уже закрыто.",
                                 reply_markup=telegram_close_thread_keyboard(user_id=msg.from_user.id))

    @staticmethod
    async def telegram_reopen_general_topic_cmd(msg: Message) -> None:
        """
        /open_general command function. Opens general thread
        :param msg: Message telegram object
        :return: Nothing
        """
        try:
            await msg.bot.reopen_general_forum_topic(chat_id=msg.chat.id)
            await msg.answer(f"Удача ✅\n{msg.from_user.mention_html('Этот пользователь')} открыл основное обсуждение",
                             reply_markup=telegram_open_thread_keyboard(user_id=msg.from_user.id))
        except TelegramBadRequest as ex:
            if ex.message == "Bad Request: TOPIC_NOT_MODIFIED":
                await msg.answer("Ошибка ❌\nДанное обсуждение уже открыто.",
                                 reply_markup=telegram_open_thread_keyboard(user_id=msg.from_user.id))

    @staticmethod
    async def telegram_hide_general_topic_cmd_handler(msg: Message) -> None:
        """
        /hide_general command function. Hides general thread
        :param msg: Message telegram object
        :return: Nothing
        """
        try:
            await msg.bot.hide_general_forum_topic(chat_id=msg.chat.id)
            await msg.answer(f"Удача ✅\n{msg.from_user.mention_html('Этот пользователь')} скрыл основное обсуждение",
                             reply_markup=delete_keyboard(admin_id=msg.from_user.id))
        except TelegramBadRequest as ex:
            if ex.message == "Bad Request: TOPIC_NOT_MODIFIED":
                await msg.answer(f"Ошибка ❌\nОсновное обсуждение уже скрыто.",
                                 reply_markup=delete_keyboard(admin_id=msg.from_user.id))

    @staticmethod
    async def telegram_unhide_general_topic_cmd(msg: Message) -> None:
        """
        /show_general command function. Shows back general thread.
        :param msg: Message telegram object
        :return: Nothing
        """
        try:
            await msg.bot.unhide_general_forum_topic(chat_id=msg.chat.id)
            await msg.answer(f"Удача ✅\n{msg.from_user.mention_html('Этот пользователь')} раскрыл основное обсуждение",
                             reply_markup=delete_keyboard(admin_id=msg.from_user.id))
        except TelegramBadRequest as ex:
            if ex.message == "Bad Request: TOPIC_NOT_MODIFIED":
                await msg.answer(f"Ошибка ❌\nДанное обсуждение уже публично.",
                                 reply_markup=delete_keyboard(admin_id=msg.from_user.id))

    @staticmethod
    async def telegram_close_thread_callback_handler(call: CallbackQuery, callback_data: CloseThread) -> None:
        """
        Query, what close thread
        :param call: CallbackQuery object
        :param callback_data: ClosetThread object
        :return: None
        """

        if callback_data.user_id != call.from_user.id or not call.message.chat.is_forum:
            return
        try:
            if call.message.message_thread_id:
                await call.bot.close_forum_topic(chat_id=call.message.chat.id,
                                                 message_thread_id=call.message.message_thread_id)
                await call.message.edit_text(
                    f"Удача ✅\n{call.from_user.mention_html('Этот пользователь')} закрыл данное обсуждение.",
                    reply_markup=telegram_close_thread_keyboard(user_id=call.from_user.id))
            else:
                await call.bot.close_general_forum_topic(chat_id=call.message.chat.id)
                await call.message.edit_text(
                    text=f"Удача ✅\n{call.from_user.mention_html('Этот пользователь')} закрыл основное обсуждение.",
                    reply_markup=telegram_close_thread_keyboard(user_id=call.from_user.id))
        except TelegramBadRequest as ex:
            if ex.message == "Bad Request: TOPIC_NOT_MODIFIED":
                await call.message.edit_text(f"Ошибка ❌\nДанное обсуждение уже закрыто",
                                             reply_markup=telegram_close_thread_keyboard(user_id=call.from_user.id))

    async def telegram_open_thread_callback_handler(call: CallbackQuery, callback_data: OpenThread) -> None:
        """
        Query, what opens thread
        :param call: CallbackQuery object
        :param callback_data: OpenThread
        :return: None
        """

        if callback_data.user_id != call.from_user.id or not call.message.chat.is_forum:
            return
        try:
            if call.message.message_thread_id:
                await call.bot.reopen_forum_topic(chat_id=call.message.chat.id,
                                                  message_thread_id=call.message.message_thread_id)
                await call.message.edit_text(
                    f"Удача ✅\n{call.from_user.mention_html('Этот пользователь')} открыл данное обсуждение.",
                    reply_markup=telegram_open_thread_keyboard(user_id=call.from_user.id))
            else:
                await call.bot.reopen_general_forum_topic(chat_id=call.message.chat.id)
                await call.message.edit_text(
                    f"Удача ✅\n{call.from_user.mention_html('Этот пользователь')} открыл основное обсуждение",
                    reply_markup=telegram_open_thread_keyboard(user_id=call.from_user.id))
        except TelegramBadRequest as ex:
            if ex.message == "Bad Request: TOPIC_NOT_MODIFIED":
                await call.message.edit_text(f"Ошибка ❌\nДанное обсуждение уже открыто.",
                                             reply_markup=telegram_open_thread_keyboard(user_id=call.from_user.id))
        """
        Telegram feature settings
        """
        # Telegram setting info

    telegram_setting_in_list = True
    telegram_setting_name = "Работа с Форумом 💬"
    telegram_setting_description = "<b>Работа с Форумом</b>💬\nДанная настройка включает следущие комманды:\n" \
                                   "<pre>/open - открывают тему форума\n" \
                                   "/close - закрывают тему форума\n" \
                                   "/open_general - открывают основную тему форума\n" \
                                   "/close_general - закрывает основную тему форума\n" \
                                   "/hide_general - прячет основную тему форума\n" \
                                   "/show_general - показывает основную тему форума</pre>\n" \
                                   "Для исполнения <b>требует соответсвующих прав от пользователя и их наличие у бота. Также должен быть" \
                                   "включен форум</b>"
    telegram_db_name = TelegramChatSettings.topics
    telegram_category = "admin"
    # Telegram commands
    telegram_commands: dict[str: str] = {
        'close': 'Close fast topic (not general) in chat',
        'open': 'Open fast topic (not general) in chat',
        'hide_general': 'Hide general topic in chat',
        'show_general': 'Show general topic in chat',
        "close_general": 'Closes general topic in chat',
        "open_general": 'Opens general topic in chat',
    }
    telegram_cmd_avaible = True  # Is a feature have a commands
    # All handlers
    telegram_message_handlers = [
        [telegram_close_topic_cmd_handler, [Command(commands=["close_topic", "close"]),
                                            UserHasPermissions(["can_manage_topics"]),
                                            BotHasPermissions(["can_manage_topics"]), F.chat.is_forum,
                                            ~(F.chat.type == ChatType.PRIVATE), IsSettingEnabled(telegram_db_name)]],
        [telegram_reopen_topic_cmd_handler, [Command(commands=["reopen_topic", "open_topic", "open"]),
                                             UserHasPermissions(["can_manage_topics"]),
                                             BotHasPermissions(["can_manage_topics"]), F.chat.is_forum,
                                             ~(F.chat.type == ChatType.PRIVATE), IsSettingEnabled(telegram_db_name)]],
        [telegram_close_general_topic_cmd_handler, [Command(commands=["close_general"]),
                                                    UserHasPermissions(["can_manage_topics"]),
                                                    BotHasPermissions(["can_manage_topics"]),
                                                    F.chat.is_forum], IsSettingEnabled(telegram_db_name)],
        [telegram_reopen_general_topic_cmd, [Command(commands=["reopen_general", "open_general"]),
                                             UserHasPermissions(["can_manage_topics"]),
                                             BotHasPermissions(["can_manage_topics"]), F.chat.is_forum,
                                             ~(F.chat.type == ChatType.PRIVATE), IsSettingEnabled(telegram_db_name)]],
        [telegram_hide_general_topic_cmd_handler, [Command(commands=["hide_general"]),
                                                   UserHasPermissions(["can_manage_topics"]),
                                                   BotHasPermissions(["can_manage_topics"]), F.chat.is_forum,
                                                   ~(F.chat.type == ChatType.PRIVATE),
                                                   IsSettingEnabled(telegram_db_name)]],
        [telegram_unhide_general_topic_cmd, [Command(commands=["unhide_general", "show_general"]),
                                             UserHasPermissions(["can_manage_topics"]),
                                             BotHasPermissions(["can_manage_topics"]), F.chat.is_forum,
                                             ~(F.chat.type == ChatType.PRIVATE), IsSettingEnabled(telegram_db_name)]]
    ]
    telegram_callback_handlers = [
        [telegram_close_thread_callback_handler, [CloseThread.filter()]],
        [telegram_open_thread_callback_handler, [OpenThread.filter()]]
    ]
