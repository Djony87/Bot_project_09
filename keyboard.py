from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types


main_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Регистрация", callback_data="reg_user"),
        InlineKeyboardButton(text="Все пользователи", callback_data="get_all_users")
    ],
    [
        InlineKeyboardButton(text="Поддержка", url="https://www.google.com"),
        InlineKeyboardButton(text="Выход", callback_data="/start")
    ]
])

kb = [
    [types.KeyboardButton(text="С пюрешкой")],
    [types.KeyboardButton(text="Без пюрешки")]
]
keyboard = types.ReplyKeyboardMarkup(keyboard=kb)