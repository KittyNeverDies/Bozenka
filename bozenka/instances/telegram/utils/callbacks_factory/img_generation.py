from aiogram.filters.callback_data import CallbackData


class ImageGenerationCategory(CallbackData, prefix="igc"):
    """
    Callback with information related to image
    """
    user_id: int
    category: str


