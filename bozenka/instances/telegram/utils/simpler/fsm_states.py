from aiogram.fsm.state import StatesGroup, State

# GPT answering states, only one btw


class AnsweringGPT4Free(StatesGroup):
    """
    Gpt4Free states for generating answers and setting models & provider
    """
    set_provider = State()
    set_model = State()
    ready_to_answer = State()
    answering = State()


class AnsweringGpt4All(StatesGroup):
    """
    Gpt4All states for generating answers and setting models soon.
    """
    set_model = State()
    ready_to_answer = State()
    answering = State()


