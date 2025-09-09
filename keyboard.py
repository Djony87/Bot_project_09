from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types


main_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="кнопка 1", callback_data="button_1")],
    [InlineKeyboardButton(text="кнопка 2", callback_data="button_2")],
    [InlineKeyboardButton(text="Поддержка", url="https://www.google.com")],
    [InlineKeyboardButton(text="Выход", callback_data="/start")]
                                ])

kb = [
    [types.KeyboardButton(text="С пюрешкой")],
    [types.KeyboardButton(text="Без пюрешки")]
]
keyboard = types.ReplyKeyboardMarkup(keyboard=kb)