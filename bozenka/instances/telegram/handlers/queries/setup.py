from aiogram.types import CallbackQuery, Message
from sqlalchemy import select, Update
from sqlalchemy.ext.asyncio import async_sessionmaker

from bozenka.database.tables.telegram import ChatSettings
from bozenka.instances.telegram.utils.callbacks_factory import SetupCategory, SetupFeature, SetupAction
from bozenka.instances.telegram.utils.keyboards import setup_category_keyboard, setup_feature_keyboard
from bozenka.instances.telegram.utils.simpler import list_of_features


async def inline_setup_category(call: CallbackQuery, callback_data: SetupCategory):
    """
    Query, what shows list of  features to enable.
    :param call:
    :param callback_data:
    :return:
    """
    await call.message.edit_text("Выберите настройку, которую хотите изменить",
                                 reply_markup=setup_category_keyboard(category=callback_data.category_name))


async def inline_setup_category_back(call: CallbackQuery, callback_data: SetupAction):
    """
    Query, what shows list of  features to enable.
    :param call:
    :param callback_data:
    :return:
    """
    await call.message.edit_text("Выберите настройку, которую хотите изменить",
                                 reply_markup=setup_category_keyboard(category=callback_data.feature_category))


async def inline_edit_feature(call: CallbackQuery, callback_data: SetupFeature, session_maker: async_sessionmaker):
    """
    Query, what shows  menu to enable / disable feature
    :param call:
    :param callback_data:
    :param session_maker:
    :return:
    """
    await call.message.edit_text(
        list_of_features[callback_data.feature_category][callback_data.feature_index].description,
        reply_markup=await setup_feature_keyboard(category=callback_data.feature_category,
                                                  index=callback_data.feature_index,
                                                  session=session_maker, msg=call.message))


async def inline_feature_edited(call: CallbackQuery, callback_data: SetupAction, session_maker: async_sessionmaker):
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
            await session.execute(Update(ChatSettings)
                                  .values({list_of_features[callback_data.feature_category][callback_data.feature_index].settings_name: callback_data.action == "enable"})
                                  .where(ChatSettings.chat_id == call.message.chat.id))
    await call.message.edit_text(
        list_of_features[callback_data.feature_category][callback_data.feature_index].description,
        reply_markup=await setup_feature_keyboard(category=callback_data.feature_category,
                                                  index=callback_data.feature_index,
                                                  session=session, msg=call.message))
