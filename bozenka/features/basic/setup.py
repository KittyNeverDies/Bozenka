from aiogram import F
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy import Update
from sqlalchemy.ext.asyncio import async_sessionmaker

from bozenka.database.tables.telegram import get_chat_config_value, TelegramChatSettings
from bozenka.features import BasicFeature
from bozenka.instances.telegram.utils.callbacks_factory import SetupAction, SetupFeature, SetupCategory
from bozenka.instances.telegram.utils.filters import IsOwner
from bozenka.instances.telegram.utils.keyboards import setup_keyboard, setup_category_keyboard, setup_feature_keyboard
from bozenka.instances.telegram.utils.simpler import list_of_features


class Setup(BasicFeature):
    """
    A class of /setup command
    All staff related to it will be here
    """

    async def telegram_setup_cmd_handler(msg: Message) -> None:
        """
        /setup telegram handler
        :param msg: Telegram message object
        :return: Nothing
        """
        await msg.answer("Привет владелец чата 👋\n"
                         "Настрой меня - бота так, как тебе удобно, и я буду помогать тебе в чате с определенными функциями.\n"
                         "Используй меню настроек ниже, чтобы указать, какие функции, которые я умею, должен выполнять.",
                         reply_markup=setup_keyboard())

    async def telegram_setup_categories_handler(call: CallbackQuery, callback_data: SetupCategory | SetupAction):
        """
        Query, what shows list of  features to enable.
        :param call:
        :param callback_data:
        :return:
        """
        await call.message.edit_text("Выберите настройку, которую хотите изменить",
                                     reply_markup=setup_category_keyboard(category=callback_data.category_name))

    async def telegram_setup_edit_feature_handler(call: CallbackQuery, callback_data: SetupFeature, session_maker: async_sessionmaker):
        """
        Query, what shows  menu to enable / disable feature
        :param call:
        :param callback_data:
        :param session_maker:
        :return:
        """
        is_enabled = await get_chat_config_value(
            chat_id=call.message.chat.id,
            session=session_maker,
            setting=list_of_features[callback_data.feature_category][callback_data.feature_index]
        )

        await call.message.edit_text(
            list_of_features[callback_data.feature_category][callback_data.feature_index].description,
            reply_markup=await setup_feature_keyboard(category=callback_data.feature_category,
                                                      index=callback_data.feature_index,
                                                      is_enabled=is_enabled))

    async def telegram_features_edit_handler(call: CallbackQuery, callback_data: SetupAction, session_maker: async_sessionmaker):
        """
        Query, what shows  menu to enable / disable feature
        after editing
        :param call:
        :param callback_data:
        :param session_maker:
        :return:
        """
        async with session_maker() as session:
            async with session.begin():
                await session.execute(Update(TelegramChatSettings)
                                      .values(
                    {list_of_features[callback_data.category_name][callback_data.feature_index].settings_name: callback_data.action == "enable"})
                                      .where(TelegramChatSettings.chat_id == call.message.chat.id))
        await call.message.edit_text(
            list_of_features[callback_data.category_name][callback_data.feature_index].description,
            reply_markup=await setup_feature_keyboard(category=callback_data.category_name,
                                                      index=callback_data.afeature_index,
                                                      is_enabled=callback_data.action == "enable"))

    """
    Telegram feature settings
    """
    # Telegram feature settings
    telegram_setting_in_list = False
    telegram_commands = {"setup": 'Command to setup bozenka features in chat'}
    telegram_cmd_avaible = True
    telegram_category = None
    telegram_message_handlers = [
            [telegram_setup_cmd_handler, [Command(commands=["setup"]), ~(F.chat.type == ChatType.PRIVATE), IsOwner(True)]]
        ]
    telegram_callback_handlers = [
            [telegram_features_edit_handler, [SetupAction.filter(F.action == "disable"), IsOwner(True)]],
            [telegram_features_edit_handler, [SetupAction.filter(F.action == "enable"), IsOwner(True)]],
            [telegram_setup_edit_feature_handler, [SetupFeature.filter(), IsOwner(True)]],
            [telegram_setup_categories_handler, [SetupAction.filter(F.action == "back"), IsOwner(True)]]
    ]
