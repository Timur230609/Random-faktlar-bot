import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN
from database.db import create_tables
from handlers import start, facts, admin

# Bot va dispatcher obyektlari
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

# Routerlarni ulaymiz
dp.include_router(start.router)
dp.include_router(facts.router)
dp.include_router(admin.router)

# Asosiy ishga tushirish funksiyasi
async def main():
    create_tables()  # Ma'lumotlar bazasidagi jadvalni yaratish
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# Botni ishga tushiramiz
if __name__ == "__main__":
    asyncio.run(main())
