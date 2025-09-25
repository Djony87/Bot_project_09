from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types


main_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Регистрация", callback_data="reg_user"),
        InlineKeyboardButton(text="Инфо.", callback_data="info")
    ],
    [
        InlineKeyboardButton(text="Поддержка", url="https://www.google.com"),
        InlineKeyboardButton(text="Выход", callback_data="start")
    ]
])



# keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
# InlineKeyboardButton(text="Все пользователи", callback_data="get_all_users")