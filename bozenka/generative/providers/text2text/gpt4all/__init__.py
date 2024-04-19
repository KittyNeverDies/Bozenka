import logging
import os

from aiogram import F
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from gpt4all import GPT4All

from bozenka.generative.providers.main import BasicAiGenerativeProvider
from bozenka.instances.telegram.utils.callbacks_factory import GptStop, GptCategory, GptBackMenu, Gpt4AllSelect, \
    Gpt4AllModel
from bozenka.instances.telegram.utils.delete import delete_keyboard
from bozenka.instances.telegram.utils.simpler import AIGeneration


model_path = os.getcwd() + "\\model\\"


class DeleteMenu(CallbackData, prefix="delete"):
    """
       Callback with information to delete message
    """
    user_id_clicked: int


class TextToText(CallbackData, prefix='text2text'):
    category_name: str
    user_id: int


def check(model_filename: str) -> bool:
    """
    Checking & downloading our gpt4all models
    Returns True if it's already downloaded
    Returns False if it's not downloaded
    :param model_filename: File name of gpt4all model
    :return: Does it exist
    """
    print(os.path.exists("models\\" + model_filename))
    return os.path.exists("models\\" + model_filename)


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


class Gpt4All(BasicAiGenerativeProvider):
    model_path = os.getcwd() + "\\model\\"

    @staticmethod
    async def generate_telegram(msg: Message, state: FSMContext):
        """
        Generates response for telegram user
        :param msg: Telegram message object
        :param state: FSMContext aiogram object
        :return: None
        """

        models = GPT4All.list_models()
        answer = ""
        data = await state.get_data()

        main_msg = await msg.answer("Пожалуйста подождите, мы генерируем вам ответ ⏰\n"
                                    "Если что-то пойдет не так, мы вам сообщим 👌",
                                    reply_markup=text_response_keyboard(user_id=msg.from_user.id))

        if not check(models[data["model"]]["filename"]):
            main_msg = await main_msg.edit_text(main_msg.text + "\nПодождите пожалуста, мы скачиваем модель...",
                                                reply_markup=main_msg.reply_markup)

        try:
            # Setting Gpt4All model
            model = GPT4All(model_name=models[data["model"]]["filename"],
                            model_path=model_path,
                            allow_download=True)
            # Setting our chat session if exist
            model.current_chat_session = [] if not data.get("chat_history") else data["chat_history"]
            # Generating answer
            with model.chat_session():
                answer = model.generate(msg.text)
                await state.update_data(chat_history=model.current_chat_session)

        except Exception as S:
            answer = "Простите, произошла ошибка 😔\nЕсли это продолжается, пожалуйста используйте /cancel или кнокпу под сообщением."
            logging.log(msg=f"Get an exception for generating answer={S}",
                        level=logging.ERROR)
        finally:
            await main_msg.edit_text(answer, reply_markup=text_response_keyboard(user_id=msg.from_user.id))

        await state.set_state(AIGeneration.ready_to_answer)

    @staticmethod
    async def telegram_g4a_handler(call: CallbackQuery, callback_data: TextToText, state: FSMContext) -> None:
        """
        Query, what shows list for gpt4all models
        :param state: FSMContext aiogram class
        :param call: CallbackQuery telegram class
        :param callback_data: GptCategory class
        :return: None
        """
        if callback_data.user_id != call.from_user.id or await state.get_state():
            return

        await state.update_data(category="text2text", name="Gpt4All")

        await state.set_state(AIGeneration.selection)
        await call.message.edit_text("Библиотека Gpt4All\n\n"
                                     "Все модели нейронных сетей будут скачиваться на сервер, по этому вам нужно будет подождать некоторое время загрузки\n"
                                     "Не зависит от веб ресурсов, как Gpt4Free, но требует больше времени на генерацию ответа на сервере.\n\n"
                                     "Выберите пожалуйста модель искуственного интелекта 👾",
                                     reply_markup=generate_gpt4all_page(user_id=call.from_user.id))

    @staticmethod
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
        await call.message.edit_text("Библиотека Gpt4All\n\n"
                                     "Все модели нейронных сетей будут скачиваться на сервер, по этому вам нужно будет подождать некоторое время загрузки\n"
                                     "Не зависит от веб ресурсов, как Gpt4Free, но требует больше времени на генерацию ответа на сервере.\n\n"
                                     "Выберите пожалуйста модель искуственного интелекта 👾",
                                     reply_markup=generate_gpt4all_page(user_id=call.from_user.id))

    @staticmethod
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
        await call.message.edit_text(f"{name}\n\n"
                                     f"Обученно на основе {models[callback_data.index]['parameters']} строк 👨‍💻\n"
                                     f"Тип модели: {models[callback_data.index]['type']}\n\n"
                                     f"Чтобы выбрать это модель, нажимте не кнопку <b>Выбрать</b>\n"
                                     f"Чтобы вернуться к списку моделей, нажмите на кнопку <b>Вернуться к списку.</b>\n"
                                     f"Чтобы отменить выбор, нажмите на кнопку <b>Спасибо, не надо.</b>\n",
                                     reply_markup=gpt4all_model_menu(user_id=call.from_user.id,
                                                                     index=callback_data.index))

    @staticmethod
    async def telegram_g4a_selected_handler(call: CallbackQuery, callback_data: Gpt4AllSelect,
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
        await state.update_data(model=callback_data.index)
        await state.set_state(AIGeneration.ready_to_answer)
        models = GPT4All.list_models()

        await call.message.edit_text("Удача ✅\n"
                                     "Вы теперь можете спокойно вести диалог 🤖\n"
                                     f"Вы выбрали модель <b>{models[callback_data.index]['name']}</b>👾 от Gpt4All\n"
                                     "Чтобы прекратить общение, используйте /cancel ",
                                     reply_markup=delete_keyboard(admin_id=callback_data.user_id))

    generative_functions = {
        # Format is social_network_name: generative_function
        "telegram": generate_telegram
    }
    handlers_functions = {
        "telegram": [
            [telegram_g4a_handler, [TextToText.filter(F.category_name == "Gpt4All")]],
            [telegram_g4a_infomration_handler, [Gpt4AllModel.filter()]],
            [telegram_g4a_selected_handler, [Gpt4AllSelect.filter()]],
        ]
    }
    category_of_generation: str = "text2text"
    name_of_generation: str = "Gpt4All"
