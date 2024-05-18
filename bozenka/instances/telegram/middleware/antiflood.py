from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import Update, Message, CallbackQuery
from cachetools import TTLCache


class CounterMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
        **kwargs: Any
    ) -> Any:
        self.counter += 1
        print(self.counter)
        return await handler(event, data)


class MessageThrottlingMiddleware(BaseMiddleware):
    """
    This middleware is skidded from public codes
    It's fitlering a spam of messages, like /start and etc
    """

    def __init__(self, time_to_wait: int = 5) -> None:
        """
        Setting up middleware
        :param time_to_wait: time, what we need to wait after some messages
        :return: Nothing
        """
        self.cache = TTLCache(maxsize=10_000, ttl=time_to_wait)

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        """
        Working after getting an Update of Message
        :param handler: A handler, what handling message
        :param event: A message, what we need to work with
        :param data: A data we are getting
        :return:
        """
        if event.chat.id in self.cache:
            return
        self.cache[event.chat.id] = None
        return await handler(event, data)


class CallbackThrottlingMiddleware(BaseMiddleware):
    """
    This middleware is skidded from public codes
    It's fitlering a spam of callbackquery, like pressing to much on buttons
    """

    def __init__(self, time_to_wait: int = 5) -> None:
        """
        Setting up middleware
        :param time_to_wait: time, what we need to wait after some messages
        :return: Nothing
        """
        self.cache = TTLCache(maxsize=10_000, ttl=time_to_wait)

    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any],
    ) -> Any:
        """
        Working after getting an Update of Callback
        :param handler: A handler, what handling callback
        :param event: A callback, what we need to work with
        :param data: A data we are getting
        :return:
        """
        if event.message.chat.id in self.cache:
            return
        self.cache[event.message.chat.id] = None
        return await handler(event, data)


