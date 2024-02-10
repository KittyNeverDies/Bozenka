import logging

from aiogram import Bot, F
from aiogram.enums import ContentType
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

    # Telegram feature settings
    telegram_setting = TelegramChatSettings.welcome_messages
    telegram_commands: dict[str: str] = {}
    telegram_setting_in_list = True
    telegram_setting_name = "Приветсвенные сообщения 👋"
    telegram_setting_description = "<b>Приветсвенные сообщения 👋</b>" \
                                   "\nПриветсвенные сообщения новым и ушедшим пользователям.",
    telegram_cmd_avaible = False  # Is a feature have a commands
    telegram_message_handlers = [
        [telegram_leave_handler, [F.content_type == ContentType.LEFT_CHAT_MEMBER]],
        [telegram_join_handler, [F.content_type == ContentType.NEW_CHAT_MEMBERS]]
    ]
    telegram_callback_handlers = []
