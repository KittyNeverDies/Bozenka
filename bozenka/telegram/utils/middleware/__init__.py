__all__ = ["registration"]

import logging

from aiogram import Router, Dispatcher


def register_middlewares(dp: Dispatcher):
    """
    Registering all middlewares of bot.
    :param router:
    :return:
    """
    logging.log(msg=f"Registering middlewares of bot", level=logging.INFO)
    # dp.message.middleware(Registration)
