import logging

from aiogram import types
from aiogram.fsm.context import FSMContext

# Callbacks for GPT
from bozenka.instances.telegram.utils.callbacks_factory import (
    GptCategory,
    Gpt4FreeProvider,
    Gpt4freeResult,
    Gpt4FreeProviderPage,
    Gpt4FreeModelPage, GptStop, GptBackMenu
)
# Keyboards for messages
from bozenka.instances.telegram.utils.keyboards import (
    generate_gpt4free_models_page,
    generate_gpt4free_providers_page,
    delete_keyboard, gpt_categories_keyboard
)
# Simpler utlilities
from bozenka.instances.telegram.utils.simpler import (
    AnsweringGPT4Free,
    AnsweringGpt4All,
    ru_cmds
)


async def inline_start_gpt(call: types.CallbackQuery, callback_data: GptBackMenu, state: FSMContext) -> None:
    if call.from_user.id != callback_data.user_id:
        return
    await call.message.edit_text("Пожалуста, выберите сервис для ИИ.",
                                 reply_markup=gpt_categories_keyboard(user_id=call.from_user.id))


async def inline_g4f_providers(call: types.CallbackQuery, callback_data: GptCategory, state: FSMContext) -> None:
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

    await call.message.edit_text("Выберите пожалуйста одного из провайдеров 👨‍💻",
                                 reply_markup=generate_gpt4free_providers_page(page=0, user_id=callback_data.user_id))
    await call.answer("Выберите пожалуйста одного из провайдеров 👨‍💻")


async def inline_g4f_providers_back(call: types.CallbackQuery, callback_data: GptBackMenu, state: FSMContext) -> None:
    """
    Query, what creating providers selecting menu.
    :param state:
    :param call:
    :param callback_data:
    :return:
    """
    if call.from_user.id != callback_data.user_id:
        return

    logging.log(msg=f"Back to providers menu by user_id={call.from_user.id}",
                level=logging.INFO)
    await state.set_state(AnsweringGPT4Free.set_provider)

    await call.message.edit_text("Выберите пожалуйста одного из провайдеров 👨‍💻",
                                 reply_markup=generate_gpt4free_providers_page(page=0, user_id=callback_data.user_id))
    await call.answer("Выберите пожалуйста одного из провайдеров 👨‍💻")


async def inline_g4f_models(call: types.CallbackQuery, callback_data: Gpt4FreeProvider, state: FSMContext) -> None:
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

    await call.message.edit_text("Выберите пожалуйста модель ИИ 👾", reply_markup=generate_gpt4free_models_page(
        user_id=callback_data.user_id,
        provider=callback_data.provider,
        page=0
    ))
    await call.answer("Выберите пожалуйста модель ИИ 👾")


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

    await call.message.edit_text("Удача ✅\n"
                                 "Вы теперь можете спокойно вести диалог 🤖\n"
                                 f"Вы выбрали модель <pre>{callback_data.model}</pre>👾, от провайдера <pre>{callback_data.model}</pre>👨‍💻\n"
                                 "Чтобы прекратить общение, используйте /cancel ",
                                 reply_markup=delete_keyboard(admin_id=callback_data.user_id))
    await call.answer("Вы теперь можете спокойно вести диалог 🤖")


"""
async def inline_g4a_ready(call: types.CallbackQuery, callback_data: Gpt4All, state: FSMContext) -> None:
    Query, what says about getting ready for questions for Gpt4All.
    :param call:
    :param callback_data:
    :param state:
    :return:
    if callback_data.user_id != call.from_user.id:
        return
    await state.set_state(AnsweringGpt4All.answering)
    logging.log(msg=f"Loaded GPT answering status for user_id={call.from_user.id}",
                level=logging.INFO)
    await call.message.edit_text("Удача ✅\n"
                                 "Вы теперь можете спокойно вести диалог 🤖\n"
                                 "Чтобы прекратить общение, используйте /cancel",
                                 reply_markup=delete_keyboard(admin_id=callback_data.user_id))
    await call.answer("Вы теперь можете спокойно вести диалог 🤖")
"""


async def next_g4f_providers(call: types.CallbackQuery, callback_data: Gpt4FreeProviderPage,
                             state: FSMContext) -> None:
    """
    Query, what generates a next page of providers for user
    :param call:
    :param callback_data:
    :param state:
    :return:
    """
    if call.from_user.id != callback_data.user_id:
        return
    logging.log(msg=f"Changed page to {str(callback_data.page + 1)} user_id={call.from_user.id}",
                level=logging.INFO)
    await call.message.edit_text(call.message.text,
                                 reply_markup=generate_gpt4free_providers_page(user_id=callback_data.user_id,
                                                                               page=callback_data.page))
    await call.answer(f"Вы перелистали на страницу {callback_data.page + 1}📄")


async def next_g4f_models(call: types.CallbackQuery, callback_data: Gpt4FreeModelPage,
                          state: FSMContext) -> None:
    """
    Query, what generates a next page of models for user.
    :param call:
    :param callback_data:
    :param state:
    :return:
    """
    if call.from_user.id != callback_data.user_id:
        return
    logging.log(msg=f"Changed page to {str(callback_data.page + 1)} user_id={call.from_user.id}",
                level=logging.INFO)
    await call.message.edit_text(call.message.text,
                                 reply_markup=generate_gpt4free_models_page(
                                     user_id=callback_data.user_id,
                                     provider=callback_data.provider,
                                     page=callback_data.page
                                 ))
    await call.answer(f"Вы перелистали на страницу {callback_data.page + 1}📄")


async def inline_return_pages(call: types.CallbackQuery) -> None:
    """
    Query, made for helping purposes.
    Shows current page.
    :param call:
    :return:
    """
    logging.log(msg=f"Showed helping info for user_id={call.from_user.id}",
                level=logging.INFO)
    await call.answer("Здесь расположается текущая странница 📃")


async def inline_stop_dialog(call: types.CallbackQuery, callback_data: GptStop, state: FSMContext) -> None:
    """
    Query, what stops dialog
    :param call:
    :param callback_data:
    :param state:
    """
    if callback_data.user_id != call.from_user.id:
        return
    await state.clear()
    await call.answer()
    await call.message.edit_text(text=call.message.text + "\n\nДиалог остановлен ✅\n",
                                 reply_markup=delete_keyboard(admin_id=call.from_user.id))
