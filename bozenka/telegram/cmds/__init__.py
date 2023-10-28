import logging

from aiogram import Dispatcher

from bozenka.telegram.cmds.admin import register_admin_cmd
from bozenka.telegram.queries import register_queries
from bozenka.telegram.cmds.dev import register_dev_cmd
from bozenka.telegram.cmds.main import register_main_cmd
from bozenka.telegram.cmds.user import register_user_cmd
from bozenka.telegram.utils.middleware import register_middlewares


def register_handlers(dp: Dispatcher):
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
