from aiogram.filters import Filter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import async_sessionmaker

from bozenka.database.tables.telegram import get_chat_configuration, get_chat_config_value


class IsSettingEnabled(Filter):
    """
    Check, does chat have enabled required feature
    """

    def __init__(self, setting) -> None:
        self.setting = setting

    async def __call__(self, msg: Message, session_maker: async_sessionmaker) -> bool:
        """
        Working after calling this filter
        :param msg: Message telegram boject
        :param session_maker: AsyncSessionMaker SqlAlchemy object
        :return: Is config enabled
        """

        return await get_chat_config_value(chat_id=msg.chat.id, session=session_maker, setting=self.setting)

