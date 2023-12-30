import logging

from aiogram import types
from aiogram.fsm.context import FSMContext
from gpt4all import GPT4All

from bozenka.instances.telegram.utils.simpler.fsm_states import *

# Callbacks for GPT
from bozenka.instances.telegram.utils.callbacks_factory import (
    GptCategory,
    Gpt4FreeProvider,
    Gpt4freeResult,
    Gpt4FreeProviderPage,
    Gpt4FreeModelPage, GptStop, GptBackMenu, Gpt4AllModel, Gpt4AllSelect
)
# Keyboards for messages
from bozenka.instances.telegram.utils.keyboards import (
    gpt4free_models_keyboard,
    gpt4free_providers_keyboard,
    delete_keyboard, gpt_categories_keyboard, generate_gpt4all_page, gpt4all_model_menu
)
# Simpler utlilities
from bozenka.instances.telegram.utils.simpler import (
    AnsweringGPT4Free,
    AnsweringGpt4All,
)
