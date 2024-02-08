import logging

from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import async_sessionmaker

from bozenka.database.tables.telegram import TelegramChatSettings
from bozenka.features import BasicFeature
from bozenka.instances.telegram.utils.callbacks_factory import PinMsg, UnpinMsg
from bozenka.instances.telegram.utils.keyboards import unpin_msg_keyboard, delete_keyboard, pin_msg_keyboard
from bozenka.instances.telegram.utils.simpler import SolutionSimpler


class Welcome(BasicFeature):
    """
    A class of pins related commands
    All staff related to it will be here
    """

    @staticmethod
    async def telegram_join_handler(msg: Message, session_maker: async_sessionmaker) -> None:
        """
        Message handler.
        Send welcome message, after adding new member to chat.
        Also works on adding bot to chat and sending welcome message.
        :param msg: Message telegram object
        :param session_maker: AsyncSessionmaker object
        :return: None
        """
        for new in msg.new_chat_members:
            if new.id != msg.bot.id:
                logging.log(msg=f"Saing welcome for user_id={new.id}, chat_id={msg.chat.id}",
                            level=logging.INFO)
                await msg.answer(
                    f"Пользователь {new.mention_html()} переехал в конфу, благодаря {msg.from_user.mention_html()}👋",
                )
                await msg.delete()
            else:
                logging.log(msg=f"Saing welcome to administrators for chat_id={msg.chat.id}",
                            level=logging.INFO)
                await msg.answer("Здраствуйте администраторы чата 👋\n"
                                 "Я - <b>бозенька</b>, мультифункциональный бот, разрабатываемый Bozo Developement\n"
                                 "Выдайте мне <b>полные права администратора</b> для моей полной работы.\n"
                                 "Чтобы настроить функционал, используйте /setup или кнопку под сообщением", )
                await SolutionSimpler.auto_settings(msg=msg, session=session_maker)

    @staticmethod
    async def telegram_leave_handler(msg: Message, bot: Bot) -> None:
        """
        Sens goodbye message, after deleting member from chat
        :param msg: Message telegram object
        :param bot: Aiogram bot object
        :return: Nothing
        """
        await msg.delete()
        if msg.from_user.id == bot.id:
            return
        logging.log(msg=f"Saing goodbye for user_id={msg.left_chat_member.id}, chat_id={msg.chat.id}",
                    level=logging.INFO)
        await msg.answer(
            f"Пользователь {msg.left_chat_member.mention_html()} съехал с конфы, благодаря {msg.from_user.mention_html()}👋"
        )

    def __init__(self):
        """
        All information about feature
        will be inside this function
        """
        super().__init__()
        self.cmd_description: str = "Your description of command"
        # Telegram feature settings
        self.telegram_setting = TelegramChatSettings.welcome_messages
        self.telegram_commands: dict[str: str] = {}
        self.telegram_setting_in_list = True
        self.telegram_setting_name = "Приветсвенные сообщения 👋"
        self.telegram_setting_description = "<b>Приветсвенные сообщения 👋</b>" \
                                            "\nПриветсвенные сообщения новым и ушедшим пользователям.",
        self.telegram_cmd_avaible = False  # Is a feature have a commands
        self.telegram_message_handlers = {

        }
        self.telegram_callback_handlers = {}
