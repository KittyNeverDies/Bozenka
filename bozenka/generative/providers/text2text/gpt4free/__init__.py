import logging
from typing import Any

import g4f
import g4f.Provider
from aiogram import F
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from g4f.Provider import RetryProvider

from bozenka.generative.providers.main import BasicAiGenerativeProvider
from bozenka.instances.telegram.utils.callbacks_factory import GptStop, GptCategory, GptBackMenu, Gpt4FreeCategory, \
    Gpt4FreeProviderPage, Gpt4FreeProvsModelPage, Gpt4FreeProvider, Gpt4FreeModelPage, Gpt4FreeModel, Gpt4freeResult
from bozenka.instances.telegram.utils.simpler import AIGeneration


class DeleteMenu(CallbackData, prefix="delete"):
    """
       Callback with information to delete message
    """
    user_id_clicked: int


class TextToText(CallbackData, prefix='text2text'):
    category_name: str
    user_id: int


# Helper
def items_list_generator(page: int, list_of_items, count_of_items: int) -> list[Any]:
    """
    Generate page, made for backend
    :param page: Number of page
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


def telegram_gpt4free_providers_keyboard(user_id: int, page: int) -> InlineKeyboardMarkup:
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
    from g4f.models import ModelUtils
    full_list = ModelUtils.convert.keys()
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


def text_response_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """
    Generating menu for response from GPT
    :param user_id:
    :return:
    """
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Спасибо, удали сообщение ✅", callback_data=DeleteMenu(user_id_clicked=str(user_id)).pack())],
        [InlineKeyboardButton(text="Завершить диалог 🚫", callback_data=GptStop(user_id=str(user_id)).pack())]
    ])
    return kb


def generate_gpt4free_providers():
    """
    Generates list of g4f providers
    :return:
    """
    return {prov: g4f.Provider.ProviderUtils.convert[prov] for prov in g4f.Provider.__all__
            if prov != "BaseProvider" and prov != "AsyncProvider" and prov != "RetryProvider" and
            g4f.Provider.ProviderUtils.convert[prov].working}


def generate_gpt4free_models():
    """
    Generates list of g4f models
    :return:
    """
    models = {}
    for model_name, model in g4f.models.ModelUtils.convert.items():
        if type(model.best_provider) is RetryProvider:
            for pr in model.best_provider.providers:
                if pr.__name__ in models:
                    models[pr.__name__].append(model_name)
                else:
                    models[pr.__name__] = [model_name]
        else:
            if model.best_provider.__name__ in models:
                models[model.best_provider.__name__].append(model_name)
            else:
                models[model.best_provider.__name__] = [model_name]
    print(models)
    return models


class Gpt4Free(BasicAiGenerativeProvider):
    """
    Object of Gpt4Free library generation
    for handlers and queue generation
    """

    @staticmethod
    async def generate_telegram(msg: Message, state: FSMContext) -> None:
        """
        Generates response for telegram user
        :param msg: Message from user
        :param state: FSM context
        :return: None
        """

        info = await state.get_data()

        providers = generate_gpt4free_providers()
        reply = await msg.reply("Пожалуйста подождите, мы генерируем ответ от провайдера ⏰\n"
                                "Если что-то пойдет не так, мы вам сообщим 👌")

        current_messages = []
        if info.get("ready_to_answer"):
            for message in info["ready_to_answer"]:
                current_messages.append(message)

        if not info.get("provider"):
            info["provider"] = None

        current_messages.append({"role": "user", "content": msg.text})

        response = ""
        try:
            response = await g4f.ChatCompletion.create_async(
                model=info["model"],
                messages=current_messages,
                provider=None if info["provider"] is None else providers[info["provider"]],
                stream=False
            )

        except NameError or SyntaxError:
            try:
                response = g4f.ChatCompletion.create(
                    model=info["model"],
                    messages=current_messages,
                    provider=None if info["provider"] is None else providers[info["provider"]],
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
        await state.set_state(AIGeneration.ready_to_answer)

    @staticmethod
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

        await call.message.edit_text("Выберите пожалуйста одного из провайдеров 👨‍💻",
                                     reply_markup=telegram_gpt4free_providers_keyboard(user_id=call.from_user.id, page=0))

    @staticmethod
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

        await call.answer("Вы выбрали модели 🤖")

        await call.message.edit_text("Выберите пожалуйста модель нейронной сети 👾\n\n"
                                     "Режим модели - мы будем использовать выбранную вами модель нейронной сети с помощью переченя из веб ресурсов, с помощью которых мы будем генерировать ответ\n"
                                     "Учитывайте, что перечень из провайдеров (веб сервисов) может не работать!",
                                     reply_markup=gpt4free_models_keyboard(user_id=call.from_user.id, page=0))

    @staticmethod
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

        await state.update_data(model=callback_data.model)
        await state.set_state(AIGeneration.ready_to_answer)

        await call.answer("Вы можете начать общаться 🤖")

        await call.message.edit_text("Отлично ✅\n\n"
                                     "Вы теперь можете спокойно вести диалог с нейронной сетью 🤖\n"
                                     f"Вы выбрали модель <b>{callback_data.model}</b> у библиотеки <b>Gpt4Free</b>👾\n"
                                     "Чтобы прекратить общение, используйте /cancel или кнопку под этим и следующим сообщением.",
                                     reply_markup=text_response_keyboard(user_id=call.from_user.id))

    @staticmethod
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

        await call.message.edit_text("Выберите пожалуйста модель нейронной сети 👾\n\n"
                                     "Режим модели - мы будем использовать выбранную вами модель нейронной сети с помощью переченя из веб ресурсов, с помощью которых мы будем генерировать ответ\n"
                                     "Учитывайте, что перечень из провайдеров (веб сервисов) может не работать!",
                                     reply_markup=gpt4free_models_keyboard(user_id=call.from_user.id,
                                                                           page=callback_data.page))

    @staticmethod
    async def telegram_g4f_category_handler(call: CallbackQuery, callback_data: TextToText | GptBackMenu, state: FSMContext) -> None:
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

        if type(callback_data) == TextToText:
            await state.update_data(category="text2text", name="Gpt4Free")

        await call.answer("Вы выбрали Gpt4Free 🤖")
        await call.message.edit_text("Библиотека Gpt4Free\nВыберите, что лучше вам выбрать: модель или провайдера 🤖\n\n"
                                     "Провайдер - конкретный веб ресурс, с помощью которого мы будем обращаться к модели нейронной сети и генерировать ответ\n"
                                     "Модель - мы будем использовать выбранную вами модель с помощью переченя из веб ресурсов, с помощью которых мы будем генерировать ответ",
                                     reply_markup=gpt4free_categories_keyboard(user_id=call.from_user.id))
        await call.answer("Выберите, по какому пункту мы будем вести диалог с нейронной сети 🤖")

    @staticmethod
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

        await call.message.edit_text("Выберите пожалуйста одного из провайдеров 👨‍💻\n\n"
                                     "Если выбирать по провайдеру - конкретный веб ресурс, с помощью которого мы будем обращаться к модели нейронной сети и генерировать ответ\n"
                                     "Учитывайте, что провайдеры могут быть недоступны или не работать, так что будьте аккуратны.",
                                     reply_markup=telegram_gpt4free_providers_keyboard(page=0, user_id=callback_data.user_id))
        await call.answer("Выберите пожалуйста одного из провайдеров 👨‍💻")

    @staticmethod
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

        await state.update_data(provider=callback_data.provider)

        await call.message.edit_text("Выберите пожалуйста модель нейронной сети, доступные у провайдера 👾\n\n"
                                     "Учитывайте, что провайдер может не работать и быть не доступным!",
                                     reply_markup=gpt4free_models_by_provider_keyboard(
                                         user_id=callback_data.user_id,
                                         provider=callback_data.provider,
                                         page=0
                                     ))
        await call.answer("Выберите пожалуйста модель ИИ 👾")

    @staticmethod
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

        await state.update_data(model=callback_data.model)
        await state.set_state(AIGeneration.ready_to_answer)

        logging.log(msg=f"Loaded GPT answering status for user_id={call.from_user.id}",
                    level=logging.INFO)

        await call.message.edit_text("Отлично ✅\n\n"
                                     "Вы теперь можете спокойно вести диалог с нейронной сетью 🤖\n"
                                     f"Вы выбрали модель <b>{callback_data.model}</b>👾, от провайдера <b>{callback_data.provider}</b>👨‍💻у библиотеки <b>Gpt4Free</b>👾\n"
                                     "Чтобы прекратить общение, используйте /cancel или кнопку под этим и следующим сообщением.",
                                     reply_markup=text_response_keyboard(user_id=call.from_user.id))
        await call.answer("Вы теперь можете спокойно вести диалог 🤖")

    @staticmethod
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

    @staticmethod
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
                                     reply_markup=telegram_gpt4free_providers_keyboard(user_id=callback_data.user_id,
                                                                                       page=callback_data.page))
        await call.answer(f"Вы перелистнули на страницу {callback_data.page + 1}📄")

    generative_functions = {
        # Format is social_network_name: generative_function
        "telegram": generate_telegram
    }
    handlers_functions = {
        "telegram": [
            # g4f
            [telegram_g4f_category_handler, [TextToText.filter(F.category_name == "Gpt4Free")]],
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
        ]
    }
    category_of_generation: str = "text2text"
    name_of_generation: str = "Gpt4Free"
