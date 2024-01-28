import logging

from aiogram import Router, Dispatcher

from bozenka.instances.telegram.utils.middleware.antiflood import MessageThrottlingMiddleware, \
    CallbackThrottlingMiddleware
from bozenka.instances.telegram.utils.middleware.retry import RetryMessageMiddleware, RetryCallbackMiddleware


def register_middlewares(dp: Dispatcher) -> None:
    """
    Registering all middlewares of bot.
    :param dp: Dispatcher aiogram object
    :return: Nothing
    """
    logging.log(msg=f"Registering middlewares of bot", level=logging.INFO)

    # Throttling middlewares
    dp.message.middleware.register(MessageThrottlingMiddleware)
    dp.callback_query.middleware(CallbackThrottlingMiddleware)
    # Retry middlewares
    dp.error.middleware(RetryMessageMiddleware)
    dp.error.middleware(RetryCallbackMiddleware)
