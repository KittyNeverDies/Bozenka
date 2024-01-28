from aiogram.filters import Filter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import async_sessionmaker

from bozenka.database.tables.telegram import get_chat_configuration, get_chat_config_value
from bozenka.instances.telegram.utils.simpler import list_of_features


class IsSettingEnabled(Filter):
    """
    Check, does chat have enabled required feature
    """

    def __init__(self, setting: str) -> None:
        self.setting = setting

    async def __call__(self, msg: Message, session_maker: async_sessionmaker) -> bool:
        setting_object = None
        for key in list_of_features.items():
            for feature in list_of_features[key]:
                if feature.setting_name == self.setting:
                    setting_object = feature
                else:
                    continue

        return await get_chat_config_value(chat_id=msg.chat.id, session=session_maker, setting=setting_object)

