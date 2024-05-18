import asyncio
import base64
import json
import logging
import os
import time

import pathlib

import aiofiles
import aiohttp
import requests
from aiogram import F
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bozenka.generative.providers.main import BasicAiGenerativeProvider
from bozenka.generative import image_generative_size
from bozenka.instances.telegram.utils.delete import delete_keyboard
from bozenka.instances.telegram.utils.simpler import AIGeneration


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


class Text2Image(CallbackData, prefix='text2image'):
    category_name: str
    user_id: int


class KadinskySelectSize(CallbackData, prefix="kss"):
    """
    Callback with information related to image
    """
    user_id: int
    category: str
    size: str


def telegram_image_response_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """
    Generating menu for image
    :param user_id: User_id of called user
    :return: InlineKeyboardMarkup
    """
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Спасибо, удали сообщение ✅",
                              callback_data=DeleteMenu(user_id_clicked=str(user_id)).pack())],
        [InlineKeyboardButton(text="Остановить генерацию 🚫", callback_data=GptStop(user_id=str(user_id)).pack())]
    ])
    return kb


def telegram_image_resolution_keyboard(user_id: int, category: str) -> InlineKeyboardMarkup:
    """
    Create keyboard with list of resolution to generate image
    :param category: Category name
    :param user_id: User_id of called user
    :return: InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    for size in image_generative_size:
        builder.row(InlineKeyboardButton(text=size,
                                         callback_data=KadinskySelectSize(
                                             user_id=user_id,
                                             category=category,
                                             size=size
                                         ).pack()))
    return builder.as_markup()


class FusionBrainAPI:
    """
    Kadinsky class from their documentation.
    """

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    async def get_model(self):
        """
        Gets model from Fusion Brain API
        :return: Model ID
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS) as response:
                data = await response.json()
                return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        """
        Generates image by FusionBrain API
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

    async def get_styles(self):
        # TODO: Add access to styles of fusion brain + support to it
        """
        Gets list of styles from Fusion Brain API
        """
        pass

    async def check_generation(self, request_id, attempts=10, delay=10):
        """
        Check generation status
        :param request_id:
        :param attempts:
        :param delay:
        :return:
        """
        while attempts > 0:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.URL + 'key/api/v1/text2image/status/' + request_id,
                                       headers=self.AUTH_HEADERS) as response:
                    data = await response.json()
                    if data['status'] == 'DONE':
                        logging.log(msg="Generating of image done", level=logging.INFO)
                        return data['images']

            attempts -= 1
            await asyncio.sleep(delay)

    @staticmethod
    async def save_image(data_of_image, file_name) -> str:
        """
        Saves image to path
        """
        path = os.path.join(pathlib.Path().absolute(), "image", file_name + ".jpg")
        async with aiofiles.open(path, "wb") as file:
            await file.write(base64.b64decode(data_of_image))
        return path


kadinsky_gen = FusionBrainAPI('https://api-key.fusionbrain.ai/', os.getenv("kadinsky_api"),
                              os.getenv("kadinsky_secret"))


class FusionBrain(BasicAiGenerativeProvider):
    """
    Kadinsky class for generatig images
    in queue
    """

    category_of_generation: str = "text2image"
    name_of_generation: str = "FusionBrain"

    @staticmethod
    async def generate_telegram(msg: Message, state: FSMContext) -> None:
        """
        Message handler for kandinsky to generate image by text from message
        :param msg: Message telegram object
        :param state: FSM state of bot
        :return:
        """
        message = await msg.answer(text="Пожалуйста подождите, мы генерируем изображение ⏰\n"
                                        "Если что-то пойдет не так, мы вам сообщим 👌",
                                   reply_markup=telegram_image_response_keyboard(user_id=msg.from_user.id))
        data = await state.get_data()
        try:
            model_id = await kadinsky_gen.get_model()
            width, height = data["size"].split("x")
            generating = kadinsky_gen.generate(model=model_id,
                                               prompt=msg.text,
                                               width=int(width),
                                               height=int(height))
            result = await kadinsky_gen.check_generation(request_id=generating)

            if result:
                path = await kadinsky_gen.save_image(result[0], f"telegram_{msg.from_user.id}")
                photo = FSInputFile(path)
                await msg.answer_photo(photo=photo,
                                       caption=msg.text,
                                       reply_markup=telegram_image_response_keyboard(user_id=msg.from_user.id))
                await message.delete()
            else:
                await message.edit_text("Простите, произошла ошибка 😔\n"
                                        "Убедитесь, что севрера kadinsky работают и ваш промпт (запрос) не является неподобающим и неприемлимым\n"
                                        "Если это продолжается, пожалуйста используйте /cancel",
                                        reply_markup=telegram_image_response_keyboard(user_id=msg.from_user.id))
        except Exception as ex:
            logging.log(msg=f"Get an exception for generating answer={ex}",
                        level=logging.ERROR)
            await message.edit_text("Простите, произошла ошибка 😔\n"
                                    "Убедитесь, что севрера kadinsky работают и ваш промпт (запрос) не является неподобающим и неприемлимым\n"
                                    "Если это продолжается, пожалуйста используйте /cancel",
                                    reply_markup=telegram_image_response_keyboard(user_id=msg.from_user.id))

        finally:
            logging.log(msg=f"Generated image for user_id={msg.from_user.id} with promt",
                        level=logging.INFO)

        await state.set_state(AIGeneration.ready_to_answer)

    @staticmethod
    async def telegram_fusionbrain_selected_handler(call: CallbackQuery, callback_data: KadinskySelectSize,
                                                    state: FSMContext) -> None:
        """
        Query, what shows menu for image size to generate in
        :param call: CallbackQuery object
        :param callback_data: ImageGeneration object
        :param state: FsContext aiogram obbject
        :return: None
        """
        if call.from_user.id != callback_data.user_id:
            return
        await state.update_data(size=callback_data.size)
        await state.set_state(AIGeneration.ready_to_answer)
        await call.message.edit_text(
            f"Отлично ✅\n\nВы выбрали {callback_data.category} для генерации изображений в размере {callback_data.size}.\n"
            f"Для того, чтобы начать генерировать изображение, напишите ваш запрос в текстовом сообщении\n"
            "Напишите /cancel или кнопки для того, чтобы отменить генерацию изображений",
            reply_markup=delete_keyboard(admin_id=call.from_user.id))

    @staticmethod
    async def telegram_select_image_size_fusionbrain_handler(call: CallbackQuery,
                                                             callback_data: Text2Image,
                                                             state: FSMContext) -> None:
        """
        Query, what shows menu for image size to generate in
        :param call: CallbackQuery object
        :param callback_data: ImageGenerationCategory
        :param state: FSMContext aiogram object
        :return: None
        """
        if call.from_user.id != callback_data.user_id or await state.get_state():
            return

        await state.update_data(category="text2image", name="FusionBrain")
        await state.set_state(AIGeneration.selection)
        await call.message.edit_text("Пожалуста, выберите размер изображения 🖼",
                                     reply_markup=telegram_image_resolution_keyboard(user_id=call.from_user.id,
                                                                                     category=callback_data.category_name))

    generative_functions = {
        # Format is social_network_name: generative_function
        "telegram": generate_telegram
    }
    handlers_functions = {
        "telegram": [
            [telegram_select_image_size_fusionbrain_handler, [Text2Image.filter(F.category_name == "FusionBrain")]],
            [telegram_fusionbrain_selected_handler, [KadinskySelectSize.filter()]]]
    }
