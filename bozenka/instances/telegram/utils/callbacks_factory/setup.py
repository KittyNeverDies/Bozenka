from aiogram.filters.callback_data import CallbackData


class SetupCategory(CallbackData, prefix="sc"):
    """
    Callback data of setup categories
    """
    category_name: str


class SetupFeature(CallbackData, prefix="sf"):
    """
    Callback data of features category
    """
    feature_index: int
    feature_category: str


class SetupBack(CallbackData, prefix="sb"):
    """
    Callback data with information to back to some menu
    """
    back_to: str


class SetupEditFeature(CallbackData, prefix="sef"):
    """
    Callback data with information to edit status of bozenka enabled feature
    """
    enable: bool
    feature_index: int
    feature_category: str
