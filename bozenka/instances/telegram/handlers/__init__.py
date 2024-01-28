import logging

from aiogram import Dispatcher

from bozenka.instances.telegram.handlers.chat_admin import register_admin_cmd
from bozenka.instances.telegram.handlers.queries import register_queries
from bozenka.instances.telegram.handlers.dev import register_dev_cmd
from bozenka.instances.telegram.handlers.main import register_main_cmd
from bozenka.instances.telegram.handlers.chat_user import register_user_cmd
from bozenka.instances.telegram.utils.middleware import register_middlewares


def register_handlers(dp: Dispatcher) -> None:
    """
    Registers all handlers
    :param dp:
    :return:
    """
    logging.log(msg="Starting registering all handlers", level=logging.INFO)
    register_dev_cmd(dp)
    register_user_cmd(dp)
    register_admin_cmd(dp)
    register_main_cmd(dp)
    register_queries(dp)
    register_middlewares(dp)
