'''
import logging
from typing import Callable

from aiogram import Dispatcher, F
from aiogram.filters import CommandObject, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, Message, CallbackQuery, FSInputFile, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import async_sessionmaker

from bozenka.database.tables.telegram import TelegramChatSettings
from bozenka.features.main import BasicFeature
from bozenka.generative import image_generative_size, image_generative_categories
from bozenka.generative.text_to_image import kadinsky_gen
from bozenka.instances.telegram.filters import IsSettingEnabled
from bozenka.instances.telegram.utils.callbacks_factory import ImageGenerationCategory, ImageGeneration, DeleteMenu, \
    GptStop
from bozenka.instances.telegram.utils.delete import delete_keyboard
from bozenka.instances.telegram.utils.simpler import GeneratingImages


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




def telegram_image_generation_categories_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """
    Create keyboard with list of image generation librarioes avaible in the bozenka
    :param user_id: User_id of called user
    :return: InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    for category in image_generative_categories:
        builder.row(InlineKeyboardButton(text=category,
                                         callback_data=ImageGenerationCategory(user_id=user_id,
                                                                               category=category).pack()))
    return builder.as_markup()


class ImageGeneratrion(BasicFeature):
    """
    A classic class of lineral (basic)
    feature of bozenka. IN FUTURE!
    """
    async def telegram_select_image_size_handler(call: CallbackQuery, callback_data: ImageGenerationCategory,
                                                 state: FSMContext) -> None:
        """
        Query, what shows menu for image size to generate in
        :param call: CallbackQuery object
        :param callback_data: ImageGenerationCategory
        :param state: FSMContext aiogram object
        :return: None
        """
        if call.from_user.id != callback_data.user_id:
            return

        await state.update_data(set_category=callback_data.category)
        await state.set_state(GeneratingImages.set_size)
        await call.message.edit_text("Пожалуста, выберите размер изображения 🖼",
                                     reply_markup=telegram_image_resolution_keyboard(user_id=call.from_user.id,
                                                                                     category=callback_data.category))

    async def telegram_end_generation_handler(call: CallbackQuery, callback_data: ImageGeneration,
                                              state: FSMContext) -> None:
        """
        Query, what shows menu for image size to generate in
        :param call:
        :param callback_data:
        :param state:
        :return: None
        """
        if call.from_user.id != callback_data.user_id:
            return
        await state.update_data(set_size=callback_data.size)
        await state.set_state(GeneratingImages.ready_to_generate)
        await call.message.edit_text(
            f"Вы выбрали {callback_data.category} для генерации изображений в размере {callback_data.size}.\n"
            "Напишите /cancel для отмены",
            reply_markup=delete_keyboard(admin_id=call.from_user.id))

    async def telegram_already_generating_handler(msg: Message, state: FSMContext) -> None:
        """
        Giving response, if generating image for user right now,
        but user still asks something
        :param msg: Message telegram object
        :param state: FSM state of bot
        :return:
        """
        await msg.answer(
            "Подождите пожалуйста, мы уже генерируем изображение для вас, подождите, когда мы ответим на ваш передыдущий вопрос",
            reply_markup=delete_keyboard(admin_id=msg.from_user.id))

    async def telegram_imagine_handler(msg: Message | CallbackQuery, state: FSMContext) -> None:
        """
        /imagine command handler, start menu
        :param msg: Message telegram object
        :param state: FSM state of bot
        :return:
        """
        if await state.get_state():
            return

        if type(msg) == CallbackQuery:
            msg = msg.message

        await msg.answer("Пожалуста, выберите сервис / модель для генерации изображений",
                         reply_markup=telegram_image_generation_categories_keyboard(user_id=msg.from_user.id))

    async def telegram_kadinsky_generating_handler(msg: Message, state: FSMContext) -> None:
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
            width, height = data.get("set_size").split("x")
            if height is None and width is None:
                width, height = "500", "500"
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

    """
    Telegram feature settings
    """
    # Telegram feature settings
    telegram_category = "user"
    telegram_db_name = TelegramChatSettings.image_generation
    telegram_commands: dict[str: str] = {'imagine': 'Starts conversation with image generative ai'}
    telegram_setting_in_list = True
    telegram_setting_name = "Генерация изображений 📸"
    telegram_setting_description = "<b>Генерация изображений </b>🤖" \
                                   "\nНаходится в разработке.\n" \
                                   "На текущий момент есть поддержка:\n" \
                                   "- Kadinksy\n" \
                                   " Следите за обновлениями 😘"
    telegram_cmd_avaible = True  # Is a feature have a commands
    telegram_message_handlers = [
        [telegram_kadinsky_generating_handler, [GeneratingImages.ready_to_generate, ~Command(commands=["cancel"])]],
        [telegram_imagine_handler, [Command(commands=["imagine"]), IsSettingEnabled(telegram_db_name)]]
    ]
    telegram_callback_handlers = [
        [telegram_select_image_size_handler, [ImageGenerationCategory.filter()]],
        [telegram_end_generation_handler, [ImageGeneration.filter()]],
        [telegram_imagine_handler, [F.data == "dialogimage"]]
    ]
'''