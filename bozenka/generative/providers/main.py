import dataclasses

from aiogram.fsm.context import FSMContext
from aiogram.types import Message


class BasicAiGenerativeProvider:
    """
    Object for basic generative
    category
    """

    @staticmethod
    def generate_telegram(msg: Message, state: FSMContext):
        """
        Example function of generation content for telegram
        """

    generative_functions = {
        # Format is social_network_name: generative_function
        "telegram": generate_telegram
    }
    handlers_functions = {
        # Format is social_network_name: [[function_name, function_parameter]]
    }
    category_of_generation: str = "example"
    name_of_generation: str = "example"
