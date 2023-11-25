from aiogram.types import *

from bozenka.instances.telegram.utils.callbacks_factory import SetupCategory, SetupFeature
from bozenka.instances.telegram.utils.keyboards import setup_category_keyboard
from bozenka.instances.telegram.utils.simpler import list_of_features


async def inline_setup_features(call: CallbackQuery, callback_data: SetupCategory):
    """
    Query, what shows list of  features to enable.
    :param call:
    :param callback_data:
    :return:
    """
    await call.message.edit_text("Выберите настройку, которую хотите изменить",
                                 reply_markup=setup_category_keyboard(category=callback_data.category_name))


async def inline_setup_features_back(call: CallbackQuery, callback_data: SetupCategory):
    """
    Query, what shows list of  features to enable.
    :param call:
    :param callback_data:
    :return:
    """
    await call.message.edit_text("Выберите настройку, которую хотите изменить",
                                 reply_markup=setup_category_keyboard(category=callback_data.category_name))



async def inline_feature(call: CallbackQuery, callback_data: SetupFeature):
    """
    Query, what shows  menu to enable / disable feature
    :param call:
    :param callback_data:
    :return:
    """
    await call.message.edit_text(list_of_features[callback_data.feature_category][callback_data.feature_index].description)

