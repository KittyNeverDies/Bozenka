# This file had inside all reply keyboard / menus related to bot
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

start_keyboard = ReplyKeyboardBuilder()
start_keyboard.row(
    KeyboardButton(text="Добавить в чат 🔌"),
    KeyboardButton(text="Функционал 🔨")
)
start_keyboard.add(KeyboardButton(text="О разработчиках ℹ️"))
