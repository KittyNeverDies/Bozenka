from aiogram.filters import Filter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import async_sessionmaker
from varname.helpers import exec_code

from bozenka.database.tables.telegram import get_settings


class ChatSettingFilter(Filter):
    """
    Check, does chat have enabled features
    """

    def __init__(self, settings: str) -> None:
        self.settings = settings

    async def __call__(self, msg: Message, session: async_sessionmaker) -> bool:
        chat_setting = await get_settings(chat_id=msg.chat.id, session=session)
        exec_code(f'return chat_setting.{self.settings}')
        return True

