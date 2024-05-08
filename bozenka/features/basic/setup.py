from aiogram import F
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import Update
from sqlalchemy.ext.asyncio import async_sessionmaker

from bozenka.database.tables.telegram import get_chat_config_value, TelegramChatSettings, is_chat_exist
from bozenka.features.main import BasicFeature
from bozenka.instances.customizable_features_list import categorized_customizable_features, text_transcription
from bozenka.instances.telegram.utils.callbacks_factory import SetupAction, SetupFeature, SetupCategory
from bozenka.instances.telegram.filters import IsOwner


# Setup related keyboards
def setup_keyboard() -> InlineKeyboardMarkup:
    """
    Generate keyboard for /setup command
    :return:
    """
    kb = InlineKeyboardBuilder()

    for category in categorized_customizable_features:
        kb.row(InlineKeyboardButton(text=text_transcription[category],
                                    callback_data=SetupCategory(category_name=category).pack()))

    return kb.as_markup()


def setup_category_keyboard(category: str) -> InlineKeyboardMarkup:
    """
    Generate keyboard for one of categories
    :param category:
    :return:
    """
    kb = InlineKeyboardBuilder()
    for setting in categorized_customizable_features[category]:
        kb.row(InlineKeyboardButton(text=setting.telegram_setting_name,
                                    callback_data=SetupFeature(
                                        feature_index=categorized_customizable_features[category].index(setting),
                                        feature_category=category
                                    ).pack()))
    return kb.as_markup()


async def setup_feature_keyboard(category: str, index: int, is_enabled: bool) -> InlineKeyboardMarkup:
    """
    Generate keyboard for enabling or disabling
    on of features
    :param is_enabled:
    :param category:
    :param index:

    :return:
    """

    from aiogram.types import InlineKeyboardButton
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Выключить ❌", callback_data=SetupAction(action="disable",
                                                                           category_name=category,
                                                                           feature_index=index).pack())
        if is_enabled else
        InlineKeyboardButton(text="Включить ✅", callback_data=SetupAction(action="enable",
                                                                          category_name=category,
                                                                          feature_index=index).pack())
    ], [
        InlineKeyboardButton(text="Вернуться 🔙", callback_data=SetupAction(action="back",
                                                                           category_name=category,
                                                                           feature_index=index).pack())]])
    return kb


class Setup(BasicFeature):
    """
    A class of /setup command
    All staff related to it will be here
    """

    async def telegram_setup_cmd_handler(msg: Message, session_maker: async_sessionmaker) -> None:
        """
        /setup telegram handler
        :param msg: Telegram message object
        :return: Nothing
        """
        await msg.answer("Привет владелец чата 👋\n\n"
                         "Настрой меня - бота так, как тебе удобно, и я буду помогать тебе в чате с определенными функциями.\n"
                         "Используй меню настроек ниже, чтобы указать, какие функции, которые я умею, должен выполнять.",
                         reply_markup=setup_keyboard())

        if not (await is_chat_exist(chat_id=msg.chat.id, session=session_maker)):
            new_user = TelegramChatSettings(chat_id=msg.chat.id)
            async with session_maker() as session:
                async with session.begin():
                    await session.merge(new_user)

    async def telegram_setup_categories_handler(call: CallbackQuery, callback_data: SetupCategory | SetupAction) -> None:
        """
        Query, what shows list of  features to enable.
        :param call: CallbackQuery class
        :param callback_data: SetupCategory or SetupAction
        :return: None
        """
        await call.message.edit_text(f"{text_transcription[callback_data.category_name]}\n\n"
                                     f"Выберите функцию, которые вы хотите настроить в данной категории у бота.",
                                     reply_markup=setup_category_keyboard(category=callback_data.category_name))

    async def telegram_setup_edit_feature_handler(call: CallbackQuery, callback_data: SetupFeature, session_maker: async_sessionmaker) -> None:
        """
        Query, what shows  menu to enable / disable feature
        :param call: CallbackQuery class
        :param callback_data: SetupFeature class
        :param session_maker: AsyncSessionMaker SqlAlchemy object
        :return: None
        """
        is_enabled = await get_chat_config_value(
            chat_id=call.message.chat.id,
            session=session_maker,
            setting=categorized_customizable_features[callback_data.feature_category][callback_data.feature_index].telegram_db_name
        )

        await call.message.edit_text(
            categorized_customizable_features[callback_data.feature_category][callback_data.feature_index].telegram_setting_description,
            reply_markup=await setup_feature_keyboard(category=callback_data.feature_category,
                                                      index=callback_data.feature_index,
                                                      is_enabled=is_enabled))

    async def telegram_features_edit_handler(call: CallbackQuery, callback_data: SetupAction, session_maker: async_sessionmaker) -> None:
        """
        Query, what shows  menu to enable / disable feature
        after editing
        :param call: CallbackQuery class
        :param callback_data: SetupAction class
        :param session_maker: AsyncSessionMaker SqlAlchemy object
        :return: None
        """
        async with session_maker() as session:
            async with session.begin():
                await session.execute(Update(TelegramChatSettings)
                                      .values(
                    {categorized_customizable_features[callback_data.category_name][callback_data.feature_index].telegram_db_name: callback_data.action == "enable"})
                                      .where(TelegramChatSettings.chat_id == call.message.chat.id))
        await call.message.edit_text(
             categorized_customizable_features[callback_data.category_name][callback_data.feature_index].telegram_setting_description,
            reply_markup=await setup_feature_keyboard(category=callback_data.category_name,
                                                      index=callback_data.feature_index,
                                                      is_enabled=callback_data.action == "enable"))

    """
    Telegram feature settings
    """
    # Telegram feature settings
    telegram_setting_in_list = False
    telegram_commands = {"setup": 'Command to setup bot and edit features in chat'}
    telegram_cmd_avaible = True
    telegram_category = None
    telegram_message_handlers = [
            [telegram_setup_cmd_handler, [Command(commands=["setup"]), ~(F.chat.type == ChatType.PRIVATE), IsOwner(True)]]
        ]
    telegram_callback_handlers = [
            [telegram_features_edit_handler, [SetupAction.filter(F.action == "disable"), IsOwner(True)]],
            [telegram_features_edit_handler, [SetupAction.filter(F.action == "enable"), IsOwner(True)]],
            [telegram_setup_edit_feature_handler, [SetupFeature.filter(), IsOwner(True)]],
            [telegram_setup_categories_handler, [SetupAction.filter(F.action == "back"), IsOwner(True)]],
            [telegram_setup_categories_handler, [SetupCategory.filter(), IsOwner(True)]]
    ]
