__all__ = ["ai", "hello"]

import logging

from aiogram.filters import Command

from bozenka.telegram.cmds.dev.hello import hi, testing
from bozenka.telegram.cmds.dev.ai import *
from bozenka.telegram.utils.simpler import AnsweringGPT4Free, AnsweringGpt4All
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
    router.message.register(start_gpt_cmd, Command(commands=["conversation"]))
    router.message.register(g4f_generate_answer, AnsweringGPT4Free.ready_to_answer, ~Command(commands=["cancel"]))
    router.message.register(g4a_generate_answer, AnsweringGpt4All.answering)
    router.message.register(cancel_answering, Command(commands=["cancel"]))
    router.message.register(testing, Command(commands=["testingtest"]))
