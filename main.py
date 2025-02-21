from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
import logging
import asyncio

from db.db_manager import create_tables
from users.router.routers import users_routers
from zaek.router.routers import zaek_routers
from other.router.routers import other_routers

import os
from dotenv import load_dotenv
from settings import BOT_TOKEN
# Вместо BOT TOKEN HERE нужно вставить токен вашего бота, полученный у @BotFather
# BOT_TOKEN = '6701060927:AAFws19vmPrO-Yfm0wS-eW1aV31taq8bt2w'


BOT_TOKEN = BOT_TOKEN

# Создаем объекты бота и диспетчера

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)  # Указываем parse_mode здесь
)
dp = Dispatcher()


logging.basicConfig(level=logging.INFO)






@dp.message(Command("start","menu"))
async def cmd_start(message: types.Message):
    await message.answer("Привет, я Жуль-Писюль. Выбери раздел:", reply_markup=main_menu_kb())


def main_menu_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Zaek", callback_data="app_zaek_menu")
    builder.button(text="Различные функции", callback_data="app_other_menu")
    builder.button(text="Пользователь", callback_data="app_users")
    builder.adjust(1)
    return builder.as_markup()


dp.include_routers(zaek_routers)
dp.include_routers(other_routers)
dp.include_routers(users_routers)


async def main():
    await dp.start_polling(bot)
    await create_tables()

if __name__ == "__main__":
    asyncio.run(main())