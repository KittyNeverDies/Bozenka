from aiogram.filters.callback_data import CallbackData


class Gpt4FreeProvider(CallbackData, prefix="g4fp"):
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


class Gpt4FreeModelPage(CallbackData, prefix="g4mp"):
    """
        Callback with information to show new page
    """
    user_id: int
    page: int
    provider: str


class Gpt4freeResult(CallbackData, prefix="g4fe"):
    """
        Callback with information of selected g4f content
    """
    user_id: int
    provider: str
    model: str


class Gpt4FreeProviderPage(CallbackData, prefix="g4pp"):
    """
        Callback with information to show next page of providers
    """
    user_id: int
    page: int


class Gpt4AllModel(CallbackData, prefix="g4a"):
    """
        Callback with information to show GPT4All content
    """
    user_id: int
    index: int


class GptBackMenu(CallbackData, prefix="gbm"):
    """
        Callback to make menu back to GPT category (ies)
    """
    user_id: int
    back_to: str


class Gpt4AllSelect(CallbackData, prefix="g4s"):
    """
        Callback with information about selecting model
    """
    user_id: int
    index: int


class GptStop(CallbackData, prefix="gs"):
    """
    Callback with information to stop conversation with GPT
    """
    user_id: int
