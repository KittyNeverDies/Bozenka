import base64
import json
import logging
import os
import time

import pathlib

import requests
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message, InlineKeyboardMarkup, InlineKeyboardButton

from bozenka.generative.basic import BasicGenerative
from bozenka.instances.telegram.utils.simpler import GeneratingImages


class DeleteMenu(CallbackData, prefix="delete"):
    """
       Callback with information to delete message
    """
    user_id_clicked: int


class GptStop(CallbackData, prefix="gs"):
    """
    Callback with information to stop conversation with GPT
    """
    user_id: int


def telegram_image_response_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """
    Generating menu for image
    :param user_id: User_id of called user
    :return: InlineKeyboardMarkup
    """
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Спасибо ✅", callback_data=DeleteMenu(user_id_clicked=str(user_id)).pack())],
        [InlineKeyboardButton(text="Хватит 🚫", callback_data=GptStop(user_id=str(user_id)).pack())]
    ])
    return kb



class KadinskyAPI:
    """
    Kadinsky class from their documentation.
    """
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        """
        Generates image by kadinsky api
        :param prompt:
        :param model:
        :param images:
        :param width:
        :param height:
        :return:
        """
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        """
        Checks status of image generation by kadinsky
        :param request_id:
        :param attempts:
        :param delay:
        """
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                print("Fine!")
                return data['images']

            attempts -= 1
            time.sleep(delay)

    @staticmethod
    def save_image(data_of_image, file_name):
        """
        Saves image and returns its path
        :param data_of_image:
        :param file_name:
        """
        path = str(pathlib.Path().absolute()) + "\\image\\" + file_name + ".jpg"
        with open(path, "wb") as file:
            file.write(base64.b64decode(data_of_image))
            file.close()
        return path


kadinsky_gen = KadinskyAPI('https://api-key.fusionbrain.ai/', os.getenv("kadinsky_api"), os.getenv("kadinsky_secret"))


class KadinskyApiGenetartion(BasicGenerative):
    """
    Kadinsky class for generatig images
    in queue
    """

    @staticmethod
    async def generate_telegram(msg: Message, state: FSMContext) -> None:
        """
        Message handler for kandinsky to generate image by text from message
        :param msg: Message telegram object
        :param state: FSM state of bot
        :return:
        """
        await state.set_state(GeneratingImages.generating)
        message = await msg.answer("Пожалуйста подождите, мы генерируем изображение ⏰\n"
                                   "Если что-то пойдет не так, мы вам сообщим 👌")
        data = await state.get_data()

        try:

            model_id = kadinsky_gen.get_model()
            width, height = data["set_size"].split("x")
            generating = kadinsky_gen.generate(model=model_id,
                                               prompt=msg.text,
                                               width=int(width),
                                               height=int(height))
            result = kadinsky_gen.check_generation(request_id=generating)

            if result:
                path = kadinsky_gen.save_image(result[0], f"telegram_{msg.from_user.id}")
                photo = FSInputFile(path)
                await msg.answer_photo(photo=photo,
                                       caption=msg.text,
                                       reply_markup=telegram_image_response_keyboard(user_id=msg.from_user.id))
                await message.delete()
            else:
                await message.edit_text("Простите, произошла ошибка 😔\n"
                                        "Убедитесь, что севрера kadinsky работают и ваш промт не является неподобающим и неприемлимым\n"
                                        "Если это продолжается, пожалуйста используйте /cancel",
                                        reply_markup=telegram_image_response_keyboard(user_id=msg.from_user.id))

        except Exception as ex:
            logging.log(msg=f"Get an exception for generating answer={ex}",
                        level=logging.ERROR)
        finally:
            logging.log(msg=f"Generated image for user_id={msg.from_user.id} with promt",
                        level=logging.INFO)
        await state.set_state(GeneratingImages.ready_to_generate)

    generative_functions = {
        # Format is social_network_name: generative_function
        "telegram": generate_telegram
    }
    category_of_generation: str = "text2text"
    name_of_generation: str = "Gpt4Free"


