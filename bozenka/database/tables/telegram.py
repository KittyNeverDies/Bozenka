import asyncio
from typing import Tuple, Any

from sqlalchemy import Column, Integer, VARCHAR, Boolean, Text, select, BigInteger, Row, inspect
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import sessionmaker
from bozenka.database.main import MainModel


class TelegramUsers(MainModel):
    """
    Telegram users table, contains:

    - Telegram user_id
    - Telegram chat_id
    - Is user banned status
    - Ban reason
    - Is user muted status
    - Mute reason
    """
    __tablename__ = 'users'
    user_id = Column(BigInteger, unique=False, nullable=False, primary_key=True)
    chat_id = Column(BigInteger, unique=False, nullable=False, primary_key=True)
    is_banned = Column(Boolean, nullable=True, unique=False)
    ban_reason = Column(Text, nullable=True, unique=False)
    is_muted = Column(Boolean, nullable=True, unique=False)
    mute_reason = Column(Text, nullable=True, unique=False)

    def __str__(self) -> str:
        return f"<User:{self.user_id}:{self.chat_id}>"


class TelegramChatSettings(MainModel):
    """
    Telegram of chat settings table, contains:

    - Telegram chat_id
    - Moderation setting
    - Pins and Topics setting
    - Gpt Conversation setting
    - Welcome & Goodbye messages setting
    - Hi command setting
    - Open AI token (P.S in future)
    """
    __tablename__ = 'chats_tg'
    chat_id = Column(BigInteger, unique=True, nullable=False, primary_key=True)
    # Admin features
    moderation = Column(Boolean, default=True, unique=False)
    topics = Column(Boolean, default=False, unique=False)
    pins = Column(Boolean, default=False, unique=False)
    welcome_messages = Column(Boolean, default=True, unique=False)
    hi_command = Column(Boolean, default=False, unique=False)
    invite_generator = Column(Boolean, default=True, unique=False)
    chat_info = Column(Boolean, default=True, unique=False)
    results_in_dm = Column(Boolean, default=True, unique=False)
    restrict_notification = Column(Boolean, default=True, unique=False)

    ai_working = Column(Boolean, default=False, unique=False)
    # openai_token = Column(Text)


async def get_chat_configuration(chat_id: int, session: async_sessionmaker):
    """
    Return settings with sessionmaker by chat_id
    :param chat_id: id of telegram chat
    :param session: sessionmaker from dispatcher
    :return:
    """
    async with session() as session:
        async with session.begin():
            (await session.execute(select(TelegramChatSettings).where(TelegramChatSettings.chat_id == chat_id)))
            return (await session.execute(select(TelegramChatSettings).where(TelegramChatSettings.chat_id == chat_id))).one_or_none()


async def get_chat_config_value(chat_id: int, session: async_sessionmaker, setting) -> bool:
    """
    Return setting by sessionmaker and chat_id
    :param chat_id: id of telegram chat
    :param session: sessionmaker from dispatcher
    :param setting: string setting what we need to get
    :return:
    """
    async with session() as session:
        async with session.begin():
            rows = (await session.execute(select(setting).where(TelegramChatSettings.chat_id == chat_id))).one_or_none()
            if rows:
                return rows[0]
            return False


async def is_chat_exist(chat_id: int, session: async_sessionmaker) -> bool:
    """
    Check if chat_id exist in database or not
    :param chat_id: id of telegram chat
    :param session: async sessionmaker
    :return: Bool, does chat_id exist or not
    """
    async with session() as session:
        async with session.begin():
            rows = (await session.execute(select(TelegramChatSettings).where(TelegramChatSettings.chat_id == chat_id))).one_or_none()
            if rows:
                return True
            return False


async def get_user_info(user_id: int, chat_id: int, session: async_sessionmaker) -> Row[tuple[Any, ...] | Any] | None:
    """
    Return user with sessionmaker by user_id and chat_id.
    :param user_id: id of telegram user
    :param chat_id: id of telegram chat
    :param session: sessionmaker from dispatcher
    :return:
    """
    async with session() as session:
        async with session.begin():
            return (await session.execute(select(TelegramUsers).where(TelegramUsers.user_id == user_id and TelegramUsers.chat_id == chat_id))).one_or_none()


