import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import InputFile
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import FSInputFile

from keyboard import  main_kb
from databases.db import create_db, get_db, User
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func



# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token="8461067216:AAFtD-lVa56mzsg2QLKyL9KeVVlyZJSbKtw")
# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет я бот регистрации на веломаршрут", reply_markup=main_kb)


# новый импорт!

# Запуск процесса поллинга новых апдейтов
async def main():
    await create_db()
    await dp.start_polling(bot)


# Функция для добавления пользователя в БД
async def add_user_to_db(user_id: int, username: str, full_name: str):
    async for session in get_db():
        try:
            # Проверяем, существует ли пользователь
            result = await session.execute(
                select(User).where(User.user_id == user_id)
            )
            user = result.scalar_one_or_none()

            if not user:
                # Добавляем нового пользователя
                new_user = User(
                    user_id=user_id,
                    username=username,
                    full_name=full_name
                )
                session.add(new_user)
                await session.commit()
                return True
            else:
                # Пользователь уже существует
                return False
        except Exception as e:
            await session.rollback()
            print(f"Ошибка при добавлении пользователя: {e}")
            return False


# Хендлер для кнопки Регистрация с callback_data="reg_user"
@dp.callback_query(F.data == "reg_user")
async def handle_button_1(callback: types.CallbackQuery):
    user = callback.from_user

    # Добавляем пользователя в БД
    success = await add_user_to_db(
        user_id=user.id,
        username=user.username,
        full_name=user.full_name
    )

    if success:
        await callback.message.answer("Вы успешно зарегистрированы! ✅")
    else:
        await callback.message.answer("Вы уже были зарегистрированы ранее! ℹ️")

    await callback.answer()

# Функция для получения всех пользователей из БД
async def get_all_users():
    async for session in get_db():
        try:
            result = await session.execute(
                select(User).order_by(User.created_at.desc())
            )
            users = result.scalars().all()
            return users
        except Exception as e:
            print(f"Ошибка при получении пользователей: {e}")
            return []

# Функция для получения количества пользователей
async def get_users_count():
    async for session in get_db():
        try:
            result = await session.execute(
                select(func.count(User.id))
            )
            count = result.scalar()
            return count
        except Exception as e:
            print(f"Ошибка при подсчете пользователей: {e}")
            return 0

# Обработчик нажатия на кнопку "get_all_users"
@dp.callback_query(F.data == "get_all_users")
async def handle_button_2(callback: types.CallbackQuery):
    # Получаем количество пользователей
    users_count = await get_users_count()

    if users_count == 0:
        await callback.message.answer("В базе данных нет пользователей.")
        await callback.answer()
        return

    # Получаем всех пользователей
    users = await get_all_users()

    # Формируем сообщение с информацией о пользователях
    message_text = f"Всего пользователей: {users_count}\n\nСписок пользователей:\n"

    for i, user in enumerate(users, 1):
        username = f"@{user.username}" if user.username else "не указан"
        created_at = user.created_at.strftime("%d.%m.%Y %H:%M")
        message_text += f"{i}. {user.full_name} ({username}) - зарегистрирован: {created_at}\n"

    # Если сообщение слишком длинное, разбиваем на части
    if len(message_text) > 4096:
        # Разбиваем сообщение на части по 4000 символов
        parts = [message_text[i:i + 4000] for i in range(0, len(message_text), 4000)]

        for part in parts:
            await callback.message.answer(part)
    else:
        await callback.message.answer(message_text)

    await callback.answer()

# @dp.callback_query(F.data == "info")
# async def handle_button_2(callback: types.CallbackQuery):
#     await callback.message.answer("Едем на велике")


@dp.callback_query(F.data == "info")
async def handle_button_2(callback: types.CallbackQuery):
    try:
        if os.path.exists("media/1.jpg"):
            photo = FSInputFile("media/1.jpg")
            await callback.message.answer_photo(photo, caption="Едем на велике")
        else:
            await callback.message.answer("Фото не найдено")
    except TelegramBadRequest:
        await callback.message.answer("Ошибка при отправке фото")
    finally:
        await callback.answer()

if __name__ == "__main__":
    asyncio.run(main())