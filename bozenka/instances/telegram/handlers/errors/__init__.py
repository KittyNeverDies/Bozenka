import logging

from aiogram import Router, F
from aiogram.filters import Command


from bozenka.instances.telegram.utils.filters import (
    IsAdminFilter,
    UserHasPermissions, BotHasPermissions
)


def register_admin_cmd(router: Router) -> None:
    """
    Registers all commands related to administrators in group.
    All commands there require access to some group perms.
    :param router:
    :return:
    """
    logging.log(msg="Registering administrator commands", level=logging.INFO)
    # Helpig handlers

