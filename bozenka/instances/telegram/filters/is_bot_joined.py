from aiogram.filters import Filter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import async_sessionmaker


class IsBotJoined(Filter):
    """
    Check, does bot joined the chat
    """

    def __init__(self, setting) -> None:
        self.setting = setting

    async def __call__(self, msg: Message) -> bool:
        """
        Working after bot joined the chat
        :param msg: Message telegram object
        :return: Is config enabled
        """
        for new in msg.new_chat_members:
            if new == msg.bot.id:
                return self.setting
        return not self.setting

