from aiogram import F, Bot
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bozenka.features import BasicFeature
from bozenka.instances.telegram.utils.callbacks_factory import HelpCategory, HelpBackCategory, HelpFeature, HelpBack, \
    PinMsg, UnpinMsg, CloseThread, OpenThread
from bozenka.instances.telegram.utils.keyboards import help_category_keyboard, help_keyboard, \
    help_feature_keyboard, gpt_categories_keyboard, unpin_msg_keyboard, delete_keyboard, pin_msg_keyboard, \
    close_thread_keyboard, open_thread_keyboard
from bozenka.instances.telegram.utils.simpler import list_of_features, SolutionSimpler
from bozenka.instances.version import build, is_updated


class Threads(BasicFeature):
    """
    A class of topics / threads related commands
    All staff related to it will be here
    """

    @staticmethod
    async def telegram_close_topic_cmd_handler(msg: Message, bot: Bot) -> None:
        """
        /close command function. Closing thread
        :param msg: Message telegram object
        :param bot: Object of telegram bot
        :return: Nothing
        """
        config = await SolutionSimpler.close_topic(msg=msg)
        await msg.answer(config[0],
                         reply_markup=close_thread_keyboard(user_id=msg.from_user.id)
                         if config[1] else delete_keyboard(msg.from_user.id))

    @staticmethod
    async def telegram_reopen_topic_cmd_handler(msg: Message, bot: Bot) -> None:
        """
        /open command function. Opens thread
        :param msg: Message telegram object
        :param bot: Object of telegram bot
        :return: Nothing
        """
        config = await SolutionSimpler.open_topic(msg=msg)
        await msg.answer(config[0],
                         reply_markup=open_thread_keyboard(user_id=msg.from_user.id)
                         if config[1] else delete_keyboard(msg.from_user.id))

    @staticmethod
    async def telegram_close_general_topic_cmd_handler(msg: Message, bot: Bot) -> None:
        """
        /close_general command function. Closes general thread
        :param msg: Message telegram object
        :param bot: Object of telegram bot
        :return: Nothing
        """
        config = await SolutionSimpler.close_general_topic(msg=msg)
        await msg.answer(config[0],
                         reply_markup=close_thread_keyboard(user_id=msg.from_user.id)
                         if config[1] else delete_keyboard(msg.from_user.id))

    @staticmethod
    async def telegram_reopen_general_topic_cmd(msg: Message, bot: Bot) -> None:
        """
        /open_general command function. Opens general thread
        :param msg: Message telegram object
        :param bot: Object of telegram bot
        :return: Nothing
        """
        config = await SolutionSimpler.open_general_topic(msg=msg)
        await msg.answer(config[0],
                         reply_markup=open_thread_keyboard(user_id=msg.from_user.id)
                         if config[1] else delete_keyboard(msg.from_user.id))

    @staticmethod
    async def telegram_hide_general_topic_cmd_handler(msg: Message, bot: Bot) -> None:
        """
        /hide_general command function. Hides general thread
        :param msg: Message telegram object
        :param bot: Object of telegram bot
        :return: Nothing
        """
        config = await SolutionSimpler.hide_general_topic(msg=msg)
        await msg.answer(config[0],
                         reply_markup=delete_keyboard(msg.from_user.id))

    @staticmethod
    async def telegram_unhide_general_topic_cmd(msg: Message, bot: Bot) -> None:
        """
        /show_general command function. Shows back general thread.
        :param msg: Message telegram object
        :param bot: Object of telegram bot
        :return: Nothing
        """
        config = await SolutionSimpler.show_general_topic(msg=msg)
        await msg.answer(config[0],
                         reply_markup=delete_keyboard(msg.from_user.id))

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
        config = await SolutionSimpler.close_topic(msg=call.message, call=call)
        await call.message.edit_text(
            config[0],
            reply_markup=close_thread_keyboard(user_id=call.from_user.id) if config[1] else
            delete_keyboard(admin_id=call.from_user.id)
        )

    @staticmethod
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

    def __init__(self):
        """
        All information about feature
        will be inside this function
        """
        super().__init__()
        self.cmd_description: str = "Your description of command"
        # Telegram feature settings
        self.telegram_setting = None
        self.telegram_commands: list[str | None] = ["start"]
        self.telegram_cmd_avaible = True  # Is a feature have a commands
        self.telegram_callback_factory = None
        self.telegram_message_handlers = {

        }
        self.telegram_callback_handlers = {

        }
