from aiogram.types import *

from bozenka.instances.telegram.utils.callbacks_factory import *
from bozenka.instances.telegram.utils.keyboards import *
from bozenka.instances.telegram.utils.simpler import list_of_features


async def inline_help_features(call: CallbackQuery, callback_data: HelpCategory):
    """
    Query, what shows list of  features to get support.
    :param call:
    :param callback_data:
    :return:
    """
    await call.message.edit_text("Выберите функцию, по которой нужна помощь",
                                 reply_markup=help_category_keyboard(category=callback_data.category_name))


async def inline_back_help_features(call: CallbackQuery, callback_data: HelpBackCategory):
    """
    Query, what shows list of  features to get support.
    :param call:
    :param callback_data:
    :return:
    """
    await call.message.edit_text("Выберите функцию, по которой нужна помощь",
                                 reply_markup=help_category_keyboard(category=callback_data.back_to_category))


async def inline_back_help_categories(call: CallbackQuery, callback_data: HelpBack):
    """
    Query, what shows list of  features to get support back.
    :param call:
    :param callback_data:
    :return:
    """
    await call.message.edit_text("Выберите категорию, по которой нужна помощь:",
                                 reply_markup=help_keyboard())


async def inline_help_feature(call: CallbackQuery, callback_data: HelpFeature):
    """
    Query, what shows list of  features to get support.
    :param call:
    :param callback_data:
    :return:
    """
    await call.message.edit_text(list_of_features[callback_data.feature_category][callback_data.feature_index].description,
                                 reply_markup=help_feature_keyboard(category=callback_data.feature_category))