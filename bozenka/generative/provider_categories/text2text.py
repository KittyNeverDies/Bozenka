from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .basic_category import GenerativeCategory
from ..generative_dict import generative_dict
from ...instances.telegram.utils.simpler import AIGeneration


class Text2Text(CallbackData, prefix='text2text'):
    category_name: str
    user_id: int


class Text2TextCategory(GenerativeCategory):
    category_name: str = "Чатбот ИИ"  # Name of category
    category_command: str = "conversation"  # Command to show menu to interact with it
    category_command_description = "Start generating text using AI"
    category_description: str = "Диалог с искуственным интелектом\nВыберите библиотеку или API, чтобы продолжить:"  # Description of category
    category_codename = "text2text"  # Codename of category, to get list of classes
    callback_data = Text2Text
    start_menu_callback_data = "dialogai"

    @staticmethod
    async def telegram_menu(message: Message) -> None:
        """
        Telegram menu for generating images
        :param message: Message object
        :return: None
        """
        kb = InlineKeyboardBuilder()
        print(generative_dict)
        for i in [i.__name__ for i in generative_dict.get("text2text").values()]:
            kb.row(InlineKeyboardButton(text=i,
                                        callback_data=Text2Text(category_name=i,
                                                                user_id=message.from_user.id).pack()))

        await message.answer(
            f"ЧатБот ИИ\n\nДиалог с искуственным интелектом / нейросетью\nВыберите библиотеку или API, чтобы продолжить:",
            reply_markup=kb.as_markup())

    @staticmethod
    async def telegram_start_menu(call: CallbackQuery, state: FSMContext) -> None:
        """
        Telegram menu for generating images
        :param call: CallbackQuery telegram object
        :param state: FSMContext aiogram object
        :return: None
        """
        status = await state.get_state()
        if status is not None and status is not AIGeneration.selection:
            await call.answer("Закончите предыдущй диалог / генерацию изображений для того, чтобы продолжить", show_alert=True)
            return

        kb = InlineKeyboardBuilder()

        for i in [i.__name__ for i in generative_dict.get("text2text").values()]:
            kb.row(InlineKeyboardButton(text=i,
                                        callback_data=Text2Text(category_name=i,
                                                                user_id=call.from_user.id).pack()))
        kb.row(InlineKeyboardButton(text="Вернуться 🔙", callback_data="back"))

        await call.message.edit_text(
            f"Чатбот ИИ\n\nДиалог с искуственным интелектом / нейросетью\nВыберите библиотеку или API, чтобы продолжить:",
            reply_markup=kb.as_markup())

        await call.answer()
