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


class SetupAction(CallbackData, prefix="sa"):
    """
    Callback with information to do with a feature
    """
    action: str
    category_name: str
    feature_index: int


class SetupEditFeature(CallbackData, prefix="sef"):
    """
    Callback data with information to edit status of bozenka enabled feature
    """
    enable: bool
    feature_index: int
    feature_category: str


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
    category_name: str
