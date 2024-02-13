import logging
from typing import Any

import g4f
from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from gpt4all import GPT4All

from bozenka.database.tables.telegram import TelegramChatSettings
from bozenka.features.main import BasicFeature
from bozenka.generative import text_generative_categories
from bozenka.generative.gpt4all import model_path, check
from bozenka.generative.gpt4free import generate_gpt4free_providers, generate_gpt4free_models
from bozenka.instances.telegram.utils.callbacks_factory import Gpt4FreeProvsModelPage, Gpt4FreeProviderPage, \
    Gpt4AllSelect, Gpt4AllModel, GptCategory, Gpt4freeResult, \
    Gpt4FreeProvider, GptBackMenu, Gpt4FreeModel, Gpt4FreeCategory, Gpt4FreeModelPage, GptStop
from bozenka.instances.telegram.utils.delete import delete_keyboard
from bozenka.instances.telegram.utils.simpler import AnsweringGPT4Free, AnsweringGpt4All



def gpt_categories_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """
    Create list keyboard list of gpt libraries, available in the bot
    :param user_id:
    :return: InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    for category in text_generative_categories:
        builder.row(InlineKeyboardButton(text=category,
                                         callback_data=GptCategory(user_id=str(user_id), category=category).pack()))
    return builder.as_markup()


# Helper
def items_list_generator(page: int, list_of_items, count_of_items: int) -> list[Any]:
    """
    Generate page, made for backend
    :param page:
    :param list_of_items:
    :param count_of_items:
    """
    items = []
    required_items = [item + page * count_of_items for item in range(count_of_items)]
    for item, count in zip(list_of_items, range(0, len(list_of_items))):
        if count not in required_items:
            continue
        items.append(item)
    return items


def text_response_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """
    Generating menu for response from GPT
    :param user_id:
    :return:
    """
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Спасибо ✅", callback_data=DeleteMenu(user_id_clicked=str(user_id)).pack())],
        [InlineKeyboardButton(text="Завершить диалог 🚫", callback_data=GptStop(user_id=str(user_id)).pack())]
    ])
    return kb


def gpt4free_providers_keyboard(user_id: int, page: int) -> InlineKeyboardMarkup:
    """
    Generate page of gpt providers, can be used by user.
    :param user_id:
    :param page:
    :return:
    """
    providers = generate_gpt4free_providers()
    names = items_list_generator(page, providers, 4)
    pages = [len(providers) // 4 - 1 if page - 1 == -1 else page - 1,
             0 if page + 1 >= len(providers) // 4 else page + 1]
    generated_page = InlineKeyboardMarkup(inline_keyboard=[
        # First one provider
        [InlineKeyboardButton(text=names[0],
                              callback_data=Gpt4FreeProvider(user_id=user_id, provider=names[0], page="0").pack())],
        # Second one provider
        [InlineKeyboardButton(text=names[1],
                              callback_data=Gpt4FreeProvider(user_id=user_id, provider=names[1], page="0").pack())],
        # Third one provider
        [InlineKeyboardButton(text=names[2],
                              callback_data=Gpt4FreeProvider(user_id=user_id, provider=names[2], page="0").pack())],
        # Fourh one provider (if exist)
        [InlineKeyboardButton(text=names[3],
                              callback_data=Gpt4FreeProvider(user_id=user_id, provider=names[3],
                                                             page="0").pack())] if len(
            names) == 4 else [],
        # Page right
        [InlineKeyboardButton(text=str(len(providers) // 4 if page == 0 else "1"),
                              callback_data=Gpt4FreeProviderPage(
                                  page=str(len(providers) // 4 - 1 if page == 0 else "0"),
                                  user_id=user_id).pack()),

         InlineKeyboardButton(text="⬅️", callback_data=Gpt4FreeProviderPage(page=pages[0], user_id=user_id).pack()),
         InlineKeyboardButton(text=str(page + 1), callback_data="gotpages"),
         # Page left
         InlineKeyboardButton(text="➡️", callback_data=Gpt4FreeProviderPage(page=pages[1], user_id=user_id).pack()),
         InlineKeyboardButton(text=str(len(providers) // 4 if page != len(providers) // 4 - 1 else "1"),
                              callback_data=Gpt4FreeProviderPage(
                                  page=str(len(providers) // 4 - 1 if page != len(providers) // 4 - 1 else "0"),
                                  user_id=user_id).pack())
         ],
        # Under list buttons
        [InlineKeyboardButton(text="🔙 Вернуться к категориям",
                              callback_data=GptBackMenu(user_id=user_id, back_to="g4fcategory").pack())],
        [InlineKeyboardButton(text="Спасибо, не надо ❌",
                              callback_data=GptStop(user_id=str(user_id)).pack())]])
    return generated_page


def gpt4free_categories_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """
    Menu of categories in Gpt4Free (Providers / Models)
    :param user_id:
    :return:
    """
    print("!231234")
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="По моделям 🤖",
                             callback_data=Gpt4FreeCategory(category="models", user_id=user_id).pack())
    ], [
        InlineKeyboardButton(text="По провайдерам 🤖",
                             callback_data=Gpt4FreeCategory(category="providers", user_id=user_id).pack())
    ]])
    return kb


def gpt4free_models_keyboard(user_id: int, page: int) -> InlineKeyboardMarkup:
    """
    Generating list of GPT4FREE models, can be used to generate text.
    :param user_id:
    :param page:
    :return:
    """
    builder = InlineKeyboardBuilder()
    full_list = g4f.ModelUtils.convert.keys()
    models = items_list_generator(page=page, list_of_items=full_list, count_of_items=4)
    pages = [len(full_list) // 4 - 1 if page - 1 == -1 else page - 1,
             0 if page + 1 >= len(full_list) // 4 else page + 1]

    for model in models:
        builder.row(InlineKeyboardButton(text=model,
                                         callback_data=Gpt4FreeModel(user_id=user_id, model=model).pack()))
    builder.row(
        # First page button
        InlineKeyboardButton(text=str(len(full_list) // 4 if page == 0 else "1"),
                             callback_data=Gpt4FreeModelPage(
                                 page=str(len(full_list) // 4 - 1 if page == 0 else "1"),
                                 user_id=user_id).pack(),
                             ),
        # Page back button
        InlineKeyboardButton(text="⬅️",
                             callback_data=Gpt4FreeModelPage(user_id=str(user_id), page=pages[0], ).pack()),
        # Count of page button
        InlineKeyboardButton(text=str(page + 1), callback_data="gotpages"),
        # Next page button
        InlineKeyboardButton(text="➡️",
                             callback_data=Gpt4FreeModelPage(user_id=str(user_id), page=pages[1]).pack()),
        # Last page button
        InlineKeyboardButton(text=str(len(full_list) // 4 if page != 0 else "1"),
                             callback_data=Gpt4FreeModelPage(
                                 page=str(len(full_list) // 4 - 1) if page != 0 else "1",
                                 user_id=user_id).pack(), ))
    builder.row(InlineKeyboardButton(text="🔙 Вернуться",
                                     callback_data=GptBackMenu(user_id=user_id, back_to="g4fcategory").pack()))
    builder.row(InlineKeyboardButton(text="Спасибо, не надо ❌",
                                     callback_data=GptStop(user_id=str(user_id)).pack()))
    return builder.as_markup()


def gpt4free_models_by_provider_keyboard(user_id: int, provider: str, page: int) -> InlineKeyboardMarkup:
    """
    Generating list of GPT4Free provider's models, can be used to generate text.
    Will be also reworked.
    :param user_id:
    :param provider:
    :param page:
    :return:
    """
    builder = InlineKeyboardBuilder()
    models = generate_gpt4free_models()
    providers = generate_gpt4free_providers()
    if provider in models:
        if providers[provider].supports_gpt_4:
            models[provider].append("")
        names = items_list_generator(page, models[provider], 4)
        for name in names:
            builder.row(InlineKeyboardButton(text=name.replace('-', ' '),
                                             callback_data=Gpt4freeResult(user_id=str(user_id), provider=provider,
                                                                          model=name).pack()))
        pages = [len(models[provider]) // 4 - 1 if page - 1 == -1 else page - 1,
                 0 if page + 1 >= len(models[provider]) // 4 else page + 1]
        if len(models[provider]) > 4:
            builder.row(
                # First page button
                InlineKeyboardButton(text=str(len(models[provider]) // 4 if page == 0 else "1"),
                                     callback_data=Gpt4FreeProvsModelPage(
                                         page=str(len(models[provider]) // 4 - 1 if page == 0 else "1"),
                                         user_id=user_id,
                                         provider=provider).pack(),
                                     ),
                # Page back button
                InlineKeyboardButton(text="⬅️",
                                     callback_data=Gpt4FreeProvsModelPage(user_id=str(user_id), page=pages[0],
                                                                          provider=provider).pack()),
                # Count of page button
                InlineKeyboardButton(text=str(page + 1), callback_data="gotpages"),
                # Next page button
                InlineKeyboardButton(text="➡️",
                                     callback_data=Gpt4FreeProvsModelPage(user_id=str(user_id), page=pages[1],
                                                                          provider=provider).pack()),
                # Last page button
                InlineKeyboardButton(text=str(len(models[provider]) // 4 if page != 0 else "1"),
                                     callback_data=Gpt4FreeProvsModelPage(
                                         page=str(len(models[provider]) // 4 - 1) if page != 0 else "1",
                                         user_id=user_id,
                                         provider=provider).pack(), ))
    else:
        if providers[provider].supports_gpt_4:
            builder.row(InlineKeyboardButton(text="gpt 4",
                                             callback_data=Gpt4freeResult(user_id=str(user_id),
                                                                          provider=provider,
                                                                          model="gpt-4").pack()))
        if providers[provider].supports_gpt_35_turbo:
            builder.row(InlineKeyboardButton(text="gpt 3.5 turbo",
                                             callback_data=Gpt4freeResult
                                             (user_id=str(user_id), provider=provider, model="gpt-3.5-turbo").pack()))
    builder.row(InlineKeyboardButton(text="🔙 Вернуться к провайдерам",
                                     callback_data=GptBackMenu(user_id=user_id, back_to="providers").pack()))
    builder.row(InlineKeyboardButton(text="Спасибо, не надо ❌", callback_data=GptStop(user_id=str(user_id)).pack()))
    return builder.as_markup()


# Gpt4All related keyboards
def generate_gpt4all_page(user_id: int) -> InlineKeyboardMarkup:
    """
    Generating list of GPT4All models.
    :param user_id:
    :return:
    """
    models = GPT4All.list_models()

    builder = InlineKeyboardBuilder()

    for model in models:
        builder.row(InlineKeyboardButton(
            text=model["name"],
            callback_data=Gpt4AllModel(user_id=str(user_id), index=str(models.index(model))).pack())
        )
    builder.row(InlineKeyboardButton(text="🔙 Вернуться к списку",
                                     callback_data=GptBackMenu(user_id=user_id, back_to="g4fcategory").pack()))
    builder.row(InlineKeyboardButton(text="Спасибо, не надо ❌",
                                     callback_data=GptStop(user_id=str(user_id)).pack()))
    return builder.as_markup()


def gpt4all_model_menu(user_id: int, index: int) -> InlineKeyboardMarkup:
    """
    Generating menu for selection on of GPT4ALL models
    :param user_id:
    :param index:
    """
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Выбрать ✅",
                              callback_data=Gpt4AllSelect(user_id=user_id, index=str(index)).pack())],
        [InlineKeyboardButton(text="🔙 Вернуться к списку",
                              callback_data=GptBackMenu(user_id=user_id, back_to="g4amodels").pack())],
        [InlineKeyboardButton(text="Спасибо, не надо ❌",
                              callback_data=GptStop(user_id=str(user_id)).pack())]
    ])
    return kb




class TextGeneratrion(BasicFeature):
    """
    A class, what have inside all handlers / functions
    related to text generation of bozenka
    """

    async def telegram_already_answering_handler(msg: Message, state: FSMContext) -> None:
        """
        Giving response, if answering user now,
        but he still asks something
        :param msg: Message telegram object
        :param state: FSM state of bot
        :return: Nothing
        """
        await msg.answer(
            "Подождите пожалуйста, мы уже генерируем ответ для вас, подождите, когда мы ответим на ваш передыдущий вопрос",
            reply_markup=delete_keyboard(admin_id=msg.from_user.id))

    async def telegram_conversation_cmd_handler(msg: Message, state: FSMContext) -> None:
        """
        /conversation command handler, start
        :param msg: Message telegram object
        :param state: FSM state of bot
        :return:
        """
        if await state.get_state():
            return
        await msg.answer("Пожалуста, выберите сервис для ИИ.",
                         reply_markup=gpt_categories_keyboard
                         (user_id=msg.from_user.id))

    async def telegram_cancel_cmd_handler(msg: Message, state: FSMContext) -> None:
        """
        Canceling dialog with generative model
        Works on command /cancel
        :param msg: Message telegram object
        :param state: FSM state of bot
        :return:
        """
        current = await state.get_state()
        if current is None:
            return
        await state.clear()
        await msg.answer("Удача ✅\n"
                         "Диалог отменён!", reply_markup=delete_keyboard(admin_id=msg.from_user.id))

    # G4F telegram category
    # All handlers and other stuff
    # All code and comments
    async def telegram_g4f_generate_handler(msg: Message, state: FSMContext) -> None:
        """
        Generating answer if GPT4Free model and provider has been selected
        :param msg: Message telegram object
        :param state: FSM state of bot
        :return:
        """
        await state.set_state(AnsweringGPT4Free.answering)

        info = await state.get_data()

        providers = generate_gpt4free_providers()
        reply = await msg.reply("Пожалуйста подождите, мы генерируем ответ от провайдера ⏰\n"
                                "Если что-то пойдет не так, мы вам сообщим 👌")

        current_messages = []
        if info.get("ready_to_answer"):
            for message in info["ready_to_answer"]:
                current_messages.append(message)

        if not info.get("set_provider"):
            info["set_provider"] = None

        current_messages.append({"role": "user", "content": msg.text})

        response = ""
        try:
            response = await g4f.ChatCompletion.create_async(
                model=info["set_model"],
                messages=current_messages,
                provider=None if info["set_provider"] is None else providers[info["set_provider"]],
                stream=False
            )

        except NameError or SyntaxError:
            try:
                response = g4f.ChatCompletion.create(
                    model=info["set_model"],
                    messages=current_messages,
                    provider=None if info["set_provider"] is None else providers[info["set_provider"]],
                    stream=False
                )
            except Exception as S:
                response = "Простите, произошла ошибка 😔\nЕсли это продолжается, пожалуйста используйте /cancel"
                logging.log(msg=f"Get an exception for generating answer={S}",
                            level=logging.ERROR)
        except Exception as S:
            response = "Простите, произошла ошибка 😔\nЕсли это продолжается, пожалуйста используйте /cancel"
            logging.log(msg=f"Get an exception for generating answer={S}",
                        level=logging.ERROR)
        finally:
            await reply.edit_text(text=response, reply_markup=text_response_keyboard(user_id=msg.from_user.id))
            current_messages.append({"role": "assistant", "content": response})
            await state.update_data(ready_to_answer=current_messages)
        await state.set_state(AnsweringGPT4Free.ready_to_answer)

    async def telegram_instart_conversation_handler(call: CallbackQuery, callback_data: GptBackMenu,
                                                    state: FSMContext) -> None:
        """
        Query, what shows when clicking on button in /start menu
        :param call: CallbackQuery class
        :param state: FSMContext aiogram class
        :param callback_data: GptBackMenu class
        :return: Nothing
        """
        if call.from_user.id != callback_data.user_id or await state.get_state():
            return
        await call.message.edit_text("Пожалуста, выберите сервис для ИИ.",
                                     reply_markup=gpt_categories_keyboard(user_id=call.from_user.id))

    async def telegram_g4f_providers_handlers(call: CallbackQuery, callback_data: Gpt4FreeCategory,
                                              state: FSMContext) -> None:
        """
        Query, what creating providers selecting menu.
        :param call: CallbackQuery class
        :param state: FSMContext aiogram class
        :param callback_data: Gpt4FreeCategory
        return: Nothing
        """
        if call.from_user.id != callback_data.user_id:
            return

        logging.log(msg=f"Selected gpt4free category by user_id={call.from_user.id}",
                    level=logging.INFO)

        await call.answer("Вы выбрали провайдеры 🤖")

        await state.set_state(AnsweringGPT4Free.set_provider)
        await call.message.edit_text("Выберите пожалуйста одного из провайдеров 👨‍💻",
                                     reply_markup=gpt4free_providers_keyboard(user_id=call.from_user.id, page=0))

    async def telegram_g4f_models_handler(call: CallbackQuery, callback_data: GptCategory, state: FSMContext) -> None:
        """
        Query, what creating models selecting menu
        :param call: CallbackQuery class
        :param state: FSMContext aiogram class
        :param callback_data: GptCategory
        return: Nothing
        """
        if call.from_user.id != callback_data.user_id:
            return

        await state.set_state(AnsweringGPT4Free.set_model)

        await call.answer("Вы выбрали модели 🤖")

        await call.message.edit_text("Выберите модель, с которой будете общаться 🤖",
                                     reply_markup=gpt4free_models_keyboard(user_id=call.from_user.id, page=0))

    async def telegram_g4f_model_ready_handler(call: CallbackQuery, callback_data: Gpt4FreeModel,
                                               state: FSMContext) -> None:
        """
        Query, what ending g4f model selecting
        :param call: CallbackQuery class
        :param callback_data: Gpt4FreeModel model
        :param state: FSMContext aiogram class
        :return: Nothing
        """
        if call.from_user.id != callback_data.user_id:
            return

        await state.update_data(set_model=callback_data.model)
        await state.set_state(AnsweringGPT4Free.ready_to_answer)

        await call.answer("Вы можете начать общаться 🤖")

        await call.message.edit_text("Удача ✅\n"
                                     "Вы теперь можете спокойно вести диалог 🤖\n"
                                     f"Вы выбрали модель <b>{callback_data.model}</b>👾\n"
                                     "Чтобы прекратить общение, используйте /cancel ",
                                     reply_markup=delete_keyboard(admin_id=call.from_user.id))

    async def telegram_g4f_next_model_handler(call: CallbackQuery, callback_data: Gpt4FreeModelPage,
                                              state: FSMContext) -> None:
        """
        Query, what creating models selecting menu
        :param state: FSMContext aiogram class
        :param call: CallbackQuery class
        :param callback_data: Gpt4FreeModelPage class
        :return: None
        """
        if call.from_user.id != callback_data.user_id:
            return

        await call.answer(f"Вы перелистнули на страницу {callback_data.page + 1}📄")

        await call.message.edit_text("Выберите модель, с которой будете общаться 🤖",
                                     reply_markup=gpt4free_models_keyboard(user_id=call.from_user.id,
                                                                           page=callback_data.page))

    async def telegram_g4f_category_handler(call: CallbackQuery, callback_data: GptCategory | GptBackMenu, state: FSMContext) -> None:
        """
        Query, what creating providers selecting menu.
        :param state: FSMContext aiogram class
        :param call: CallbackQuery class
        :param callback_data: GptCategory class
        :return: None
        """
        if call.from_user.id != callback_data.user_id:
            return

        logging.log(msg=f"Selected gpt4free category by user_id={call.from_user.id}",
                    level=logging.INFO)

        if type(callback_data) == GptCategory:
            await state.update_data(set_category=callback_data.category)

        await call.answer("Вы выбрали Gpt4Free 🤖")
        await call.message.edit_text("Выберите, по какому пункту мы будем вести диалог с нейронной сети 🤖",
                                     reply_markup=gpt4free_categories_keyboard(user_id=call.from_user.id))
        await call.answer("Выберите, по какому пункту мы будем вести диалог с нейронной сети 🤖")

    async def telegram_g4f_back_provider_handler(call: CallbackQuery, callback_data: GptBackMenu,
                                                 state: FSMContext) -> None:
        """
        Query, what creating providers selecting menu.
        :param state: FSMContext aiogram class
        :param call: CallbackQuery telegram class
        :param callback_data: GptBackMenu class
        :return: None
        """
        if call.from_user.id != callback_data.user_id:
            return

        logging.log(msg=f"Back to providers menu by user_id={call.from_user.id}",
                    level=logging.INFO)
        await state.set_state(AnsweringGPT4Free.set_provider)

        await call.message.edit_text("Выберите пожалуйста одного из провайдеров 👨‍💻",
                                     reply_markup=gpt4free_providers_keyboard(page=0, user_id=callback_data.user_id))
        await call.answer("Выберите пожалуйста одного из провайдеров 👨‍💻")

    async def telegram_g4f_by_provider_models(call: CallbackQuery, callback_data: Gpt4FreeProvider,
                                              state: FSMContext) -> None:
        """
        Query, what creating models selecting menu.
        :param state: FSMContext aiogram class
        :param call: CallbackQuery telegram class
        :param callback_data: Gpt4FreeProvider Class
        :return: None
        """
        if call.from_user.id != callback_data.user_id:
            return

        logging.log(msg=f"Selected gpt4free provider {callback_data.provider} by user_id={call.from_user.id}",
                    level=logging.INFO)

        await state.update_data(set_provider=callback_data.provider)
        await state.set_state(AnsweringGPT4Free.set_model)

        await call.message.edit_text("Выберите пожалуйста модель ИИ 👾",
                                     reply_markup=gpt4free_models_by_provider_keyboard(
                                         user_id=callback_data.user_id,
                                         provider=callback_data.provider,
                                         page=0
                                     ))
        await call.answer("Выберите пожалуйста модель ИИ 👾")

    async def telegram_g4f_provider_ready_handler(call: CallbackQuery, callback_data: Gpt4freeResult, state: FSMContext) -> None:
        """
        Query, what says about getting ready to questions for ChatGPT from Gpt4Free.
        :param state: FSMContext aiogram class
        :param call: CallbackQuery telegram class
        :param callback_data: Gpt4freeResult
        :return: None
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
                                     f"Вы выбрали модель <b>{callback_data.model}</b>👾, от провайдера <b>{callback_data.provider}</b>👨‍💻\n"
                                     "Чтобы прекратить общение, используйте /cancel ",
                                     reply_markup=delete_keyboard(admin_id=callback_data.user_id))
        await call.answer("Вы теперь можете спокойно вести диалог 🤖")

    async def telegram_g4f_models_by_provider_handler(call: CallbackQuery, callback_data: Gpt4FreeProvsModelPage,
                                                      state: FSMContext) -> None:
        """
        Query, what generates a next page of models for user.
        :param state: FSMContext aiogram class
        :param call: CallbackQuery telegram class
        :param callback_data: Gpt4FreeProvsModelPage
        :return: None
        """
        if call.from_user.id != callback_data.user_id:
            return
        logging.log(msg=f"Changed page to {str(callback_data.page + 1)} user_id={call.from_user.id}",
                    level=logging.INFO)
        await call.message.edit_text(call.message.text,
                                     reply_markup=gpt4free_models_by_provider_keyboard(
                                         user_id=callback_data.user_id,
                                         provider=callback_data.provider,
                                         page=callback_data.page
                                     ))
        await call.answer(f"Вы перелистали на страницу {callback_data.page + 1}📄")

    async def telegram_next_g4f_providers_handler(call: CallbackQuery, callback_data: Gpt4FreeProviderPage,
                                                  state: FSMContext) -> None:
        """
        Query, what generates a next page of providers for user
        :param state: FSMContext aiogram class
        :param call: CallbackQuery telegram class
        :param callback_data: Gpt4FreeProviderPage class
        :return: None
        """
        if call.from_user.id != callback_data.user_id:
            return
        logging.log(msg=f"Changed page to {str(callback_data.page + 1)} user_id={call.from_user.id}",
                    level=logging.INFO)
        await call.message.edit_text(call.message.text,
                                     reply_markup=gpt4free_providers_keyboard(user_id=callback_data.user_id,
                                                                              page=callback_data.page))
        await call.answer(f"Вы перелистнули на страницу {callback_data.page + 1}📄")

    # G4A telegram handlers section
    # All code and commentaries here
    # All handlers here

    async def telegram_g4a_generate_handler(msg: Message, state: FSMContext) -> None:
        """
        Generating answer if Gpt4All has been selected
        :param msg: Message telegram object
        :param state: FSM state of bot
        :return:
        """
        await state.set_state(AnsweringGpt4All.answering)

        models = GPT4All.list_models()
        info = await state.get_data()
        answer = ""

        main_msg = await msg.answer("Пожалуйста подождите, мы генерируем вам ответ ⏰\n"
                                    "Если что-то пойдет не так, мы вам сообщим 👌",
                                    reply_markup=text_response_keyboard(user_id=msg.from_user.id))

        if not check(models[info["set_model"]]["filename"]):
            main_msg = await main_msg.edit_text(main_msg.text + "\nПодождите пожалуста, мы скачиваем модель...",
                                                reply_markup=main_msg.reply_markup)

        try:
            # Setting Gpt4All model
            model = GPT4All(model_name=models[info['set_model']]['filename'],
                            model_path=model_path,
                            allow_download=True)
            # Setting our chat session if exist
            model.current_chat_session = [] if not info.get("ready_to_answer") else info["ready_to_answer"]
            # Generating answer
            with model.chat_session():
                answer = model.generate(msg.text)
                await state.update_data(ready_to_answer=model.current_chat_session)

        except Exception as S:
            answer = "Простите, произошла ошибка 😔\nЕсли это продолжается, пожалуйста используйте /cancel"
            logging.log(msg=f"Get an exception for generating answer={S}",
                        level=logging.ERROR)
        finally:
            await main_msg.edit_text(answer, reply_markup=text_response_keyboard(user_id=msg.from_user.id))

        await state.set_state(AnsweringGpt4All.ready_to_answer)

    async def telegram_g4a_handler(call: CallbackQuery, callback_data: GptCategory, state: FSMContext) -> None:
        """
        Query, what shows list for gpt4all models
        :param state: FSMContext aiogram class
        :param call: CallbackQuery telegram class
        :param callback_data: GptCategory class
        :return: None
        """
        if callback_data.user_id != call.from_user.id:
            return
        await state.set_state(AnsweringGpt4All.set_model)
        await call.message.edit_text("Выберите пожалуйста модель ИИ 👾",
                                     reply_markup=generate_gpt4all_page(user_id=call.from_user.id))

    async def telegram_g4a_back_handler(call: CallbackQuery, callback_data: GptCategory, state: FSMContext) -> None:
        """
        Query, what shows list for gpt4all models back
        :param state: FSMContext aiogram class
        :param call: CallbackQuery telegram class
        :param callback_data: GptCategory class
        :return: None
        """
        if callback_data.user_id != call.from_user.id:
            return
        await state.set_state(AnsweringGpt4All.set_model)
        await call.message.edit_text("Выберите пожалуйста модель ИИ 👾",
                                     reply_markup=generate_gpt4all_page(user_id=call.from_user.id))

    async def telegram_g4a_infomration_handler(call: CallbackQuery, callback_data: Gpt4AllModel,
                                               state: FSMContext) -> None:
        """
        Query, what show information about clicked gpt4all model from list
        :param state: FSMContext aiogram class
        :param call: CallbackQuery telegram class
        :param callback_data: Gpt4AllModel class
        :return: None
        """
        if callback_data.user_id != call.from_user.id:
            return
        models = GPT4All.list_models()
        name = models[callback_data.index]['name']
        await call.message.edit_text(f"{name}\n"
                                     f"Обученно на основе {models[callback_data.index]['parameters']} строк 👨‍💻",
                                     reply_markup=gpt4all_model_menu(user_id=call.from_user.id,
                                                                     index=callback_data.index))

    async def telegram_g4a_end_handler(call: CallbackQuery, callback_data: Gpt4AllSelect,
                                       state: FSMContext) -> None:
        """
        Query, what says about getting ready for question for Gpt4All model
        :param state: FSMContext aiogram class
        :param call: CallbackQuery telegram class
        :param callback_data: Gpt4AllSelect class
        :return: None
        """
        if callback_data.user_id != call.from_user.id:
            return
        await state.update_data(set_model=callback_data.index)
        await state.set_state(AnsweringGpt4All.ready_to_answer)
        models = GPT4All.list_models()

        await call.message.edit_text("Удача ✅\n"
                                     "Вы теперь можете спокойно вести диалог 🤖\n"
                                     f"Вы выбрали модель <b>{models[callback_data.index]['name']}</b>👾 от Gpt4All\n"
                                     "Чтобы прекратить общение, используйте /cancel ",
                                     reply_markup=delete_keyboard(admin_id=callback_data.user_id))

    async def telegram_pages_handler(call: CallbackQuery) -> None:
        """
        Query, made for helping purposes.
        Shows current page.
        :param call: CallbackQuery telegram class
        :return: None
        """
        logging.log(msg=f"Showed helping info for user_id={call.from_user.id}",
                    level=logging.INFO)
        await call.answer("Здесь расположается текущая странница 📃")

    async def telegram_stop_dialog_handler(call: CallbackQuery, callback_data: GptStop, state: FSMContext) -> None:
        """
        Query, what stops dialog
        :param call: CallbackQuery telegram class
        :param callback_data: GptStop class
        :param state: None
        """
        # Checking user_id of user
        if callback_data.user_id != call.from_user.id:
            return
        # Clearing state
        await state.clear()
        # Answering something
        await call.answer("Хорошо ✅")
        if await state.get_state() == AnsweringGPT4Free.ready_to_answer or await state.get_state() == AnsweringGpt4All.answering:
            await call.message.edit_text(text=call.message.text + "\n\nДиалог остановлен ✅\n",
                                         reply_markup=delete_keyboard(admin_id=call.from_user.id))
        else:
            await call.message.delete()

    # Telegram feature settings
    telegram_category = "user"
    telegram_db_name = TelegramChatSettings.text_generation
    telegram_setting_in_list = True
    telegram_setting_name = "ИИ ЧатБот 🤖"
    telegram_setting_description = "<b>ИИ ЧатБот </b>🤖" \
                                   "\nЕсть поддержка:\n" \
                                   "- Моделей Gpt4All\n" \
                                   "- Провайдеров Gpt4Free и моделей\n" \
                                   "Для использования:\n" \
                                   "<pre>/conversations</pre>" \
                                   "\nНаходится в разработке, планируется в будущем. Следите за обновлениями 😘"
    telegram_commands: dict[str: str] = {
        'conversation': 'Starts conversation with text generative ai'
    }
    telegram_cmd_avaible = True  # Is a feature have a commands
    telegram_message_handlers = (
        [telegram_conversation_cmd_handler, [Command(commands=["conversation"])]],
        [telegram_g4a_generate_handler, [AnsweringGpt4All.ready_to_answer, ~Command(commands=["cancel"])]],
        [telegram_g4f_generate_handler, [AnsweringGPT4Free.ready_to_answer, ~Command(commands=["cancel"])]],
        [telegram_already_answering_handler, [AnsweringGPT4Free.answering, AnsweringGpt4All.answering]]
    )
    telegram_callback_handlers = (
        # g4a
        [telegram_g4a_handler, [GptCategory.filter(F.category == "Gpt4All")]],
        [telegram_g4a_infomration_handler, [Gpt4AllModel.filter()]],
        [telegram_g4a_end_handler, [Gpt4AllSelect.filter()]],
        # g4f
        [telegram_g4f_category_handler, [GptCategory.filter(F.category == "Gpt4Free")]],
        [telegram_g4f_category_handler, [GptBackMenu.filter(F.back_to == "g4fcategory")]],
        # categories
        [telegram_g4f_models_handler, [Gpt4FreeCategory.filter(F.category == "models")]],
        [telegram_g4f_providers_handlers, [Gpt4FreeCategory.filter(F.category == "providers")]],
        # providers list
        [telegram_g4f_providers_handlers, [GptBackMenu.filter(F.back_to == "providers")]],
        [telegram_next_g4f_providers_handler, [Gpt4FreeProviderPage.filter()]],
        # models by provider list
        [telegram_g4f_models_by_provider_handler, [Gpt4FreeProvsModelPage.filter()]],
        [telegram_g4f_by_provider_models, [Gpt4FreeProvider.filter()]],
        # models list
        [telegram_g4f_next_model_handler, [Gpt4FreeModelPage.filter()]],
        # end features
        [telegram_g4f_model_ready_handler, [Gpt4FreeModel.filter()]],
        [telegram_g4f_provider_ready_handler, [Gpt4freeResult.filter()]],
        # stop talking
        [telegram_stop_dialog_handler, [GptStop.filter()]]
    )
