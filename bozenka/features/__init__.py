from typing import Callable

from aiogram.filters import CommandObject
from aiogram.types import InlineKeyboardMarkup, Message, CallbackQuery
from sqlalchemy.ext.asyncio import async_sessionmaker

from bozenka.database.tables.telegram import TelegramChatSettings


class LineralFeature:
    """
    A classic class of lineral (basic)
    feature of bozenka. IN FUTURE!
    """

    cmd_description: str = "Your description of command"

    @NotImplemented
    async def generate_telegram_inline_keyboard(self) -> InlineKeyboardMarkup:
        """
        Generates a special telegram keyboard (menu)
        :return: Inline Keyboard
        """
        pass

    @NotImplemented
    async def telegram_command_handler(self, msg: Message, cmd: CommandObject, session_maker: async_sessionmaker) -> None:
        """
        A special telegram handler for command (if exist)
        :param msg: Telegram message object
        :param cmd: Aiogram command object
        :param session_maker: Async session maker object of SQLAlchemy
        :return: Nothing
        """
        pass

    @NotImplemented
    async def telegram_callback_handler(self, call: CallbackQuery, callback_data, session_maker: async_sessionmaker) -> None:
        """
        A special telegram handler for command (if exist)
        :param call: Telegram callbackquery object
        :param callback_data: A custom callback data created by callback factory
        :param session_maker: Async session maker object of SQLAlchemy
        :return: Nothing
        """
        pass

    def __init__(self):
        """
        All information about feature
        will be inside this function
        """
        self.cmd_description: str = "Your description of command"
        # Telegram feature settings
        self.telegram_setting = TelegramChatSettings.text_generation
        self.telegram_commands: list[str | None] = ["test"]
        self.telegram_cmd_avaible = True    # Is a feature have a commands
        self.telegram_callback_factory = None
