# This file had inside all reply keyboard / menus related to bot
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

start_keyboard_builder = ReplyKeyboardBuilder()
start_keyboard_builder.row(
    KeyboardButton(text="Добавить в чат 🔌"),
    KeyboardButton(text="Функционал 🔨")
)
start_keyboard_builder.adjust(1, 2)
start_keyboard_builder.add(KeyboardButton(text="О разработчиках ℹ️"))