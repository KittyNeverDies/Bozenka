import dataclasses

from aiogram.fsm.context import FSMContext
from aiogram.types import Message


@dataclasses.dataclass
class GenerativeCateogory:
    """
    Shows infromaton
    about generative category of one item
    """
    category_text: str              # text of category
    category_transcription: str     # transcription of category to readable text
    category_description:  str      # description of category


class BasicGenerative:
    """
    Object for basic generative
    category
    """

    def generate_telegram(self, msg: Message, state: FSMContext):
        """
        Example function of generation content for telegram
        """

    generative_functions = {
        # Format is social_network_name: generative_function
        "telegram": generate_telegram
    }
    category_of_generation: str = "example"
    name_of_generation: str = "example"

