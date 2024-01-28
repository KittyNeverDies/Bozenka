import logging

from aiogram.filters import Command

from bozenka.instances.telegram.handlers.dev.hello import hi, testing
from bozenka.instances.telegram.handlers.dev.text_generation import *
from bozenka.instances.telegram.handlers.dev.image_generation import *

from bozenka.instances.telegram.utils.simpler import AnsweringGPT4Free, AnsweringGpt4All, GeneratingImages
from aiogram import Router


def register_dev_cmd(router: Router) -> None:
    """
    Registering testing commands in development or planned in future and need much time to realise it.
    Don't need any special perms in group.
    :param router:
    :return:
    """
    logging.log(msg="Registering developer commands", level=logging.INFO)
    router.message.register(hi, Command(commands=["hi", "welcome", "sup", "wassup", "hello", "priv",
                                                  "privet", "хай", "прив", "привет", "ку"]))
    router.message.register(start_dialog_cmd, Command(commands=["conversation"]))
    router.message.register(g4f_generate_answer, AnsweringGPT4Free.ready_to_answer, ~Command(commands=["cancel"]))
    router.message.register(already_answering, AnsweringGpt4All.answering, ~Command(commands=["cancel"]))
    router.message.register(already_answering, AnsweringGPT4Free.answering, ~Command(commands=["cancel"]))
    router.message.register(g4a_generate_answer, AnsweringGpt4All.ready_to_answer, ~Command(commands=["cancel"]))
    router.message.register(kadinsky_generating_images, GeneratingImages.ready_to_generate, ~Command(commands=["cancel"]))
    router.message.register(start_imagine_cmd, Command(commands=["imagine"]))
    router.message.register(cancel_answering, Command(commands=["cancel"]))
    router.message.register(testing, Command(commands=["testingtest"]))
