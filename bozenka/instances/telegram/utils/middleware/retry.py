import time
from typing import Callable, Dict, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramRetryAfter
from aiogram.types import Message, ErrorEvent, Update, CallbackQuery


class RetryMessageMiddleware(BaseMiddleware):
    """
    Protects from user don't get update by message
    """

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: ErrorEvent[TelegramRetryAfter, Update],
        data: Dict[str, Any]
    ) -> Any:
        time.sleep(event.exception.retry_after)
        return await handler(event.update.message, data)


class RetryCallbackMiddleware(BaseMiddleware):
    """
    Protects from user don't get update by callbackquery
    """

    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: ErrorEvent[TelegramRetryAfter, Update],
        data: Dict[str, Any]
    ) -> Any:
        time.sleep(event.exception.retry_after)
        return await handler(event.update.callback_query, data)
