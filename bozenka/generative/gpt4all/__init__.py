import logging
import os

from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from gpt4all import GPT4All

from bozenka.generative.basic import BasicGenerative
import pathlib

from bozenka.instances.telegram.utils.callbacks_factory import GptStop
from bozenka.instances.telegram.utils.simpler import AnsweringGpt4All

model_path = os.getcwd() + "\\model\\"


class DeleteMenu(CallbackData, prefix="delete"):
    """
       Callback with information to delete message
    """
    user_id_clicked: int


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


class Gpt4All(BasicGenerative):

    @staticmethod
    async def generate_telegram(msg: Message, data: dict, queue: list, state: FSMContext):
        """
        Generates response for telegram user
        :param msg: Telegram message object
        :param data: Data for generating respose
        :param state: FSMContext aiogram object
        :return: None
        """

        models = GPT4All.list_models()
        answer = ""

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
            model.current_chat_session = [] if not data.get("ready_to_answer") else data["ready_to_answer"]
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

    generative_functions = {
        # Format is social_network_name: generative_function
        "telegram": generate_telegram
    }
    category_of_generation: str = "text2text"
    name_of_generation: str = "GPT4All"


