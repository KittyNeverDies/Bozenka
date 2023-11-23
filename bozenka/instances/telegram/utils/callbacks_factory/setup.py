from aiogram.filters.callback_data import CallbackData


class SetupCategory(CallbackData, prefix="scategory"):
    """
    Callback data of setup categories
    """
    owner_id: int
    category_name: str


class SetupFeature(CallbackData, prefix="sfeature"):
    """
    Callback data of features category
    """
    owner_id: int
    feature_name: str
