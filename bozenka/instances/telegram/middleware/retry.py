import time
from typing import Callable, Dict, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramRetryAfter
from aiogram.types import Message, ErrorEvent, Update, CallbackQuery


