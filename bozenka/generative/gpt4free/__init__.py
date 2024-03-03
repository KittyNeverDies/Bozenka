import logging

import g4f
import g4f.Provider
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from g4f.Provider import RetryProvider
from varname import nameof

from bozenka.generative.basic import BasicGenerative
from bozenka.instances.telegram.utils.callbacks_factory import GptStop
from bozenka.instances.telegram.utils.simpler import AnsweringGPT4Free


class DeleteMenu(CallbackData, prefix="delete"):
    """
       Callback with information to delete message
    """
    user_id_clicked: int


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


class Gpt4Free(BasicGenerative):
    """
    Object of Gpt4Free library generation
    for queue
    """

    async def generate_telegram(self, msg: Message, state: FSMContext) -> None:
        """
        Generates response for telegram user
        :param msg: Message from user
        :param state: FSM context
        :return: None
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

    generative_functions = {
        # Format is social_network_name: generative_function
        "telegram": generate_telegram
    }
    category_of_generation: str = "text2text"
    name_of_generation: str = "Gpt4Free"

