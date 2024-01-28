import logging

from aiogram import types
from aiogram.fsm.context import FSMContext
from gpt4all import GPT4All

from bozenka.instances.telegram.utils.simpler.fsm_states import *

# Callbacks for GPT
from bozenka.instances.telegram.utils.callbacks_factory import (
    ImageGeneration,
    ImageGenerationCategory
)
# Keyboards for messages
from bozenka.instances.telegram.utils.keyboards import (
    gpt4free_models_by_provider_keyboard,
    gpt4free_providers_keyboard,
    delete_keyboard, gpt_categories_keyboard, generate_gpt4all_page, gpt4all_model_menu, image_resolution_keyboard
)
# Simpler utlilities
from bozenka.instances.telegram.utils.simpler import (
    AnsweringGPT4Free,
    AnsweringGpt4All,
)


async def inline_image_size(call: types.CallbackQuery, callback_data: ImageGenerationCategory, state: FSMContext) -> None:
    """
    Query, what shows menu for image size to generate in
    :param call:
    :param callback_data:
    :param state:
    :return:
    """
    if call.from_user.id != callback_data.user_id:
        return

    await state.update_data(set_category=callback_data.category)
    await state.set_state(GeneratingImages.set_size)
    await call.message.edit_text("Пожалуста, выберите размер изображения 🖼",
                                 reply_markup=image_resolution_keyboard(user_id=call.from_user.id,
                                                                        category=callback_data.category))


async def inline_image_ready(call: types.CallbackQuery, callback_data: ImageGeneration, state: FSMContext) -> None:
    """
    Query, what shows menu for image size to generate in
    :param call:
    :param callback_data:
    :param state:
    :return:
    """
    if call.from_user.id != callback_data.user_id:
        return
    await state.update_data(set_size=callback_data.size)
    await state.set_state(GeneratingImages.ready_to_generate)
    await call.message.edit_text(f"Вы выбрали {callback_data.category} для генерации изображений в размере {callback_data.size}.\n"
                                 "Напишите /cancel для отмены",
                                 reply_markup=delete_keyboard(admin_id=call.from_user.id))

