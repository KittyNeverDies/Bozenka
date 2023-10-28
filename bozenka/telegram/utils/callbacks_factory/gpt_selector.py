from aiogram.filters.callback_data import CallbackData


class Gpt4FreeProvider(CallbackData, prefix="provider"):
    """
        Callback with information related to selected provider
    """
    user_id: int
    provider: str


class GptCategory(CallbackData, prefix="gpt"):
    """
       Callback with information to show content, related to gpt category
    """
    user_id: int
    category: str


class Gpt4freeResult(CallbackData, prefix="endselect"):
    """
        Callback with information of selected g4f content
    """
    user_id: int
    provider: str
    model: str


class Gpt4FreePage(CallbackData, prefix="gptpage"):
    """
        Callback with information to show next page of providers
    """
    user_id: int
    page: int


class Gpt4All(CallbackData, prefix="gpt4all"):
    """
        Callback with information to show GPT4All content
    """
    user_id: int
