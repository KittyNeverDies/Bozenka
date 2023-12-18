from aiogram.filters.callback_data import CallbackData


class HelpCategory(CallbackData, prefix="hc"):
    """
    Callback data of help categories
    """
    category_name: str


class HelpFeature(CallbackData, prefix="hf"):
    """
    Callback data of features category
    """
    feature_index: int
    feature_category: str


class HelpBack(CallbackData, prefix="hb"):
    """
    Callback data to back to categories in help menu
    """
    back_to: str


class HelpBackCategory(CallbackData, prefix="hbc"):
    """
    Callback data to back to list of features in one
    of categories in menu
    """
    back_to_category: str


class BackStart(CallbackData, prefix="start"):
    """
    Callback data to back to /start
    """
    pass
