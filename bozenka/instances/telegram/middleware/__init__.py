import logging

from aiogram import Dispatcher


def register_middlewares(dp: Dispatcher) -> None:
    """
    Registering all middlewares of bot.
    :param dp: Dispatcher aiogram object
    :return: Nothing
    """
    logging.log(msg=f"Registering middlewares of bot", level=logging.INFO)

    # Throttling middlewares

    """
    dp.message.middleware(CounterMiddleware)
    dp.callback_query.middleware(CallbackThrottlingMiddleware)
    # Retry middlewares
    """
    """
    dp.error.middleware(RetryMessageMiddleware)
    dp.error.middleware(RetryCallbackMiddleware)
    """
