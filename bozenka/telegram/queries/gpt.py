import logging

from aiogram import types
from aiogram.fsm.context import FSMContext

# Callbacks for GPT
from bozenka.telegram.utils.callbacks_factory import (
    GptCategory,
    Gpt4FreeProvider,
    Gpt4freeResult,
    Gpt4FreePage,
    Gpt4All
)
# Keyboards for messages
from bozenka.telegram.utils.keyboards import (
    gpt4free_models_keyboard,
    generate_gpt4free_page,
    delete_keyboard
)
# Simpler utlilities
from bozenka.telegram.utils.simpler import (
    AnsweringGPT4Free,
    AnsweringGpt4All,
    ru_cmds
)


async def inline_gpt4free(call: types.CallbackQuery, callback_data: GptCategory, state: FSMContext) -> None:
    """
    Query, what creating providers selecting menu.
    :param state:
    :param call:
    :param callback_data:
    :return:
    """
    if call.from_user.id != callback_data.user_id:
        return
    logging.log(msg=f"Selected gpt4free category by user_id={call.from_user.id}",
                level=logging.INFO)
    await state.update_data(set_category=callback_data.category)
    await state.set_state(AnsweringGPT4Free.set_provider)
    await call.message.edit_text(ru_cmds["select_provider_message"],
                                 reply_markup=generate_gpt4free_page(page=0, user_id=callback_data.user_id))
    await call.answer(ru_cmds["select_provider"])


async def inline_gpt4free_models(call: types.CallbackQuery, callback_data: Gpt4FreeProvider, state: FSMContext) -> None:
    """
    Query, what creating models selecting menu.
    :param state:
    :param call:
    :param callback_data:
    :return:
    """
    if call.from_user.id != callback_data.user_id:
        return
    logging.log(msg=f"Selected gpt4free provider {callback_data.provider} by user_id={call.from_user.id}",
                level=logging.INFO)
    await state.update_data(set_provider=callback_data.provider)
    await state.set_state(AnsweringGPT4Free.set_model)
    await call.message.edit_text(ru_cmds["select_model_message"], reply_markup=gpt4free_models_keyboard(
        user_id=callback_data.user_id,
        provider=callback_data.provider
    ))
    await call.answer(ru_cmds["select_model"])


async def inline_g4f_ready(call: types.CallbackQuery, callback_data: Gpt4freeResult, state: FSMContext) -> None:
    """
    Query, what says about getting ready to questions for ChatGPT from Gpt4Free.
    :param state:
    :param call:
    :param callback_data:
    :return:
    """
    if call.from_user.id != callback_data.user_id:
        return
    logging.log(msg=f"Selected gpt4free model {callback_data.model} by user_id={call.from_user.id}",
                level=logging.INFO)
    await state.update_data(set_model=callback_data.model)
    await state.set_state(AnsweringGPT4Free.ready_to_answer)
    logging.log(msg=f"Loaded GPT answering status for user_id={call.from_user.id}",
                level=logging.INFO)

    await call.message.edit_text(ru_cmds["finish_gptfree_message"]
                                 .replace("modelname", callback_data.model).
                                 replace("providername", callback_data.provider),
                                 reply_markup=delete_keyboard(admin_id=callback_data.user_id))
    await call.answer(ru_cmds["finish_gpt"])


async def inline_g4a_ready(call: types.CallbackQuery, callback_data: Gpt4All, state: FSMContext) -> None:
    """
    Query, what says about getting ready for questions for Gpt4All.
    :param call:
    :param callback_data:
    :param state:
    :return:
    """
    if callback_data.user_id != call.from_user.id:
        return
    await state.set_state(AnsweringGpt4All.answering)
    logging.log(msg=f"Loaded GPT answering status for user_id={call.from_user.id}",
                level=logging.INFO)
    await call.message.edit_text(ru_cmds["finish_gpt4all_message"],
                                 reply_markup=delete_keyboard(admin_id=callback_data.user_id))
    await call.answer(ru_cmds["finish_gpt"])


async def generate_next_page(call: types.CallbackQuery, callback_data: Gpt4FreePage, state: FSMContext) -> None:
    """
    Query, what generates a next page for user.
    :param call:
    :param callback_data:
    :param state:
    :return:
    """
    if call.from_user.id != callback_data.user_id:
        return
    logging.log(msg=f"Changed page to {str(callback_data.page+1)} user_id={call.from_user.id}",
                level=logging.INFO)
    await call.message.edit_text(ru_cmds["select_provider_page"].replace("pagecount", str(callback_data.page+1)),
                                 reply_markup=generate_gpt4free_page(user_id=callback_data.user_id, page=callback_data.page))
    await call.answer(ru_cmds["moved_page"].replace("pagecount", str(callback_data.page+1)))


async def inline_return_pages(call: types.CallbackQuery) -> None:
    """
    Query, made for helping purposes.
    Shows current page.
    :param call:
    :return:
    """
    logging.log(msg=f"Showed helping info for user_id={call.from_user.id}",
                level=logging.INFO)
    await call.answer(ru_cmds["help_notification"])

