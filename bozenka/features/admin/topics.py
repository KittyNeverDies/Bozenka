from aiogram import F
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from bozenka.database.tables.telegram import TelegramChatSettings
from bozenka.features import BasicFeature
from bozenka.instances.telegram.utils.callbacks_factory import CloseThread, OpenThread
from bozenka.instances.telegram.utils.filters import UserHasPermissions, BotHasPermissions
from bozenka.instances.telegram.utils.keyboards import delete_keyboard, close_thread_keyboard, open_thread_keyboard
from bozenka.instances.telegram.utils.simpler import SolutionSimpler


class Threads(BasicFeature):
    """
    A class of topics / threads related commands
    All staff related to it will be here
    """

    async def telegram_close_topic_cmd_handler(msg: Message) -> None:
        """
        /close command function. Closing thread
        :param msg: Message telegram object
        :return: Nothing
        """
        config = await SolutionSimpler.close_topic(msg=msg)
        await msg.answer(config[0],
                         reply_markup=close_thread_keyboard(user_id=msg.from_user.id)
                         if config[1] else delete_keyboard(msg.from_user.id))

    async def telegram_reopen_topic_cmd_handler(msg: Message) -> None:
        """
        /open command function. Opens thread
        :param msg: Message telegram object
        :return: Nothing
        """
        config = await SolutionSimpler.open_topic(msg=msg)
        await msg.answer(config[0],
                         reply_markup=open_thread_keyboard(user_id=msg.from_user.id)
                         if config[1] else delete_keyboard(msg.from_user.id))

    async def telegram_close_general_topic_cmd_handler(msg: Message) -> None:
        """
        /close_general command function. Closes general thread
        :param msg: Message telegram object
        :return: Nothing
        """
        config = await SolutionSimpler.close_general_topic(msg=msg)
        await msg.answer(config[0],
                         reply_markup=close_thread_keyboard(user_id=msg.from_user.id)
                         if config[1] else delete_keyboard(msg.from_user.id))

    async def telegram_reopen_general_topic_cmd(msg: Message) -> None:
        """
        /open_general command function. Opens general thread
        :param msg: Message telegram object
        :return: Nothing
        """
        config = await SolutionSimpler.open_general_topic(msg=msg)
        await msg.answer(config[0],
                         reply_markup=open_thread_keyboard(user_id=msg.from_user.id)
                         if config[1] else delete_keyboard(msg.from_user.id))

    async def telegram_hide_general_topic_cmd_handler(msg: Message) -> None:
        """
        /hide_general command function. Hides general thread
        :param msg: Message telegram object
        :return: Nothing
        """
        config = await SolutionSimpler.hide_general_topic(msg=msg)
        await msg.answer(config[0],
                         reply_markup=delete_keyboard(msg.from_user.id))

    async def telegram_unhide_general_topic_cmd(msg: Message) -> None:
        """
        /show_general command function. Shows back general thread.
        :param msg: Message telegram object
        :return: Nothing
        """
        config = await SolutionSimpler.show_general_topic(msg=msg)
        await msg.answer(config[0],
                         reply_markup=delete_keyboard(msg.from_user.id))

    async def telegram_close_thread_callback_handler(call: CallbackQuery, callback_data: CloseThread) -> None:
        """
        Query, what close thread
        :param call: CallbackQuery object
        :param callback_data: ClosetThread object
        :return: None
        """

        if callback_data.user_id != call.from_user.id or not call.message.chat.is_forum:
            return
        config = await SolutionSimpler.close_topic(msg=call.message, call=call)
        await call.message.edit_text(
            config[0],
            reply_markup=close_thread_keyboard(user_id=call.from_user.id) if config[1] else
            delete_keyboard(admin_id=call.from_user.id)
        )

    async def inline_open_thread(call: CallbackQuery, callback_data: OpenThread) -> None:
        """
        Query, what opens thread
        :param call: CallbackQuery object
        :param callback_data: OpenThread
        :return: None
        """

        if callback_data.user_id != call.from_user.id or not call.message.chat.is_forum:
            return
        config = await SolutionSimpler.open_topic(msg=call.message, call=call)
        await call.message.edit_text(
            config[0],
            reply_markup=open_thread_keyboard(user_id=call.from_user.id) if config[1] else
            delete_keyboard(admin_id=call.from_user.id)
        )

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
                                            ~(F.chat.type == ChatType.PRIVATE)]],
        [telegram_reopen_topic_cmd_handler, [Command(commands=["reopen_topic", "open_topic", "open"]),
                                             UserHasPermissions(["can_manage_topics"]),
                                             BotHasPermissions(["can_manage_topics"]), F.chat.is_forum,
                                             ~(F.chat.type == ChatType.PRIVATE)]],
        [telegram_close_general_topic_cmd_handler, [Command(commands=["close_general"]),
                                                    UserHasPermissions(["can_manage_topics"]),
                                                    BotHasPermissions(["can_manage_topics"]),
                                                    F.chat.is_forum]],
        [telegram_reopen_general_topic_cmd, [Command(commands=["reopen_general", "open_general"]),
                                             UserHasPermissions(["can_manage_topics"]),
                                             BotHasPermissions(["can_manage_topics"]), F.chat.is_forum,
                                             ~(F.chat.type == ChatType.PRIVATE)]],
        [telegram_hide_general_topic_cmd_handler, [Command(commands=["hide_general"]),
                                                   UserHasPermissions(["can_manage_topics"]),
                                                   BotHasPermissions(["can_manage_topics"]), F.chat.is_forum,
                                                   ~(F.chat.type == ChatType.PRIVATE)]],
        [telegram_unhide_general_topic_cmd, [Command(commands=["unhide_general", "show_general"]),
                                             UserHasPermissions(["can_manage_topics"]),
                                             BotHasPermissions(["can_manage_topics"]), F.chat.is_forum,
                                             ~(F.chat.type == ChatType.PRIVATE)]]
    ]
    telegram_callback_handlers = [
        [telegram_close_thread_callback_handler, [CloseThread.filter()]],
        [telegram_reopen_topic_cmd_handler, [OpenThread.filter()]]
    ]
