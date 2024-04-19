from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bozenka.generative.generative_dict import generative_dict


class YourCallbackData(CallbackData, prefix='your_callback_data'):
    """
    Your custom callback data...
    """
    category_name: str
    user_id: int


class GenerativeCategory:
    """
    Basic class for generative
    category of bozenka!
    """
    category_name: str = "Your category name"  # Name of category
    category_command: str = "/test"  # Command to show menu to interact with it
    category_command_description: str = "Your description, what shows in menu.\n Lorem ipsum dolor sit amet"   # Description of command
    category_description: str = "Your description, what shows in menu.\n Lorem ipsum dolor sit amet"  # Description of category
    category_codename = "your_codename"  # Codename of category, to get list of classes
    callback_data = YourCallbackData
    start_menu_callback_data = "yourdata"

    def generate_list(self) -> list | None:
        """
        Generates list of libraries, classes
        utilits in the category.
        """
        return [i.__name__ for i in generative_dict.get(self.category_codename)] if generative_dict.get(self.category_codename) else None

    @staticmethod
    async def telegram_menu(message: Message):
        """
        Telegram menu for category.
        Shows list of libraries, classes, by command.
        """
        print(message)

    @staticmethod
    async def telegram_start_menu(call: CallbackQuery, state: FSMContext):
        """
        Telegram start menu for category.
        Shows list of libraries, classes, by command.
        """
        print(call, state)



