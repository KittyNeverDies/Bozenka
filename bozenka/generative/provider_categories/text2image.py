from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bozenka.instances.telegram.utils.simpler import AIGeneration

from .basic_category import GenerativeCategory
from ..list_of_generative import generative_dict


class Text2Image(CallbackData, prefix='text2image'):
    category_name: str
    user_id: int


class Text2ImageCategory(GenerativeCategory):
    category_name: str = "Генерация изобразений"  # Name of category
    category_command: str = "imagine"  # Command to show menu to interact with it
    category_command_description = "Start generating images using AI"
    category_description: str = "Генерация изображения с помощью искуственного интелекта\nВыберите библиотеку или API, чтобы продолжить:"  # Description of category
    category_codename = "text2image"  # Codename of category, to get list of classes
    callback_data = Text2Image
    start_menu_callback_data = "dialogimage"

    @staticmethod
    async def telegram_menu(message: Message) -> None:
        """
        Telegram menu for generating images
        :param message: Message object
        :return: None
        """
        kb = InlineKeyboardBuilder()

        for i in [i.__name__ for i in generative_dict.get("text2image").values()]:
            print(i)
            kb.row(InlineKeyboardButton(text=i,
                                        callback_data=Text2Image(category_name=i,
                                                                 user_id=message.from_user.id).pack()))

        await message.answer(
            f"Генерация изобразений 🖼\n\nГенерация изображения с помощью искуственного интелекта\nВыберите библиотеку или API, чтобы продолжить:",
            reply_markup=kb.as_markup())

    @staticmethod
    async def telegram_start_menu(call: CallbackQuery, state: FSMContext) -> None:
        """
        Telegram menu for generating images
        :param call: CallbackQuery telegram object
        :param state: FSMContext telegram object
        :return: None
        """
        status = await state.get_state()
        if status is not None and status is not AIGeneration.selection:
            await call.answer("Закончите предыдущй диалог / генерацию изображений для того, чтобы продолжить",
                              show_alert=True)
            return

        kb = InlineKeyboardBuilder()

        for i in [i.__name__ for i in generative_dict.get("text2image").values()]:
            kb.row(InlineKeyboardButton(text=i,
                                        callback_data=Text2Image(category_name=i,
                                                                 user_id=call.from_user.id).pack()))
        kb.row(InlineKeyboardButton(text="Вернуться 🔙", callback_data="back"))

        await call.message.edit_text(
            f"Генерация изобразений 🖼\n\nГенерация изображения с помощью искуственного интелекта\nВыберите библиотеку или API, чтобы продолжить:",
            reply_markup=kb.as_markup())

        await call.answer()
