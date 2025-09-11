import asyncio
import logging
import sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command

from keyboard import keyboard, main_kb

with sqlite3.connect("new_db") as conn:
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            Date INTEGER
        )
    ''')
    # cursor.execute('create table if DATA_Table ('
    #                'id integer primary key,'
    #                'Date integer,'
    #                'Name string)')

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token="8461067216:AAFtD-lVa56mzsg2QLKyL9KeVVlyZJSbKtw")
# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Как подавать котлеты?", reply_markup=keyboard)


# новый импорт!



@dp.message(F.text.lower() == "с пюрешкой")
async def with_puree(message: types.Message):
    await message.reply("Отличный выбор!", reply_markup=main_kb)


@dp.message(F.text.lower() == "без пюрешки")
async def without_puree(message: types.Message):
    await message.reply("Так невкусно!")


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

# Хендлер для кнопки 1 с callback_data="button_1"
@dp.callback_query(F.data == "button_1")
async def handle_button_1(callback: types.CallbackQuery):
    await callback.message.answer("Вы нажали кнопку 1! ✅")
    await callback.answer()  # Убирает часики у кнопки

# Хендлер для кнопки 2 с callback_data="button_2"
@dp.callback_query(F.data == "button_2")
async def handle_button_2(callback: types.CallbackQuery):
    await callback.message.answer("Вы нажали кнопку 2! 🔄")
    await callback.answer()  # Убирает часики у кнопки

if __name__ == "__main__":
    asyncio.run(main())