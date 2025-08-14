import asyncio
from flask import Flask, request
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Update

from config import BOT_TOKEN
from database.db import create_tables
from handlers import start, facts, admin

# Flask app
app = Flask(__name__)

# Aiogram bot va dispatcher
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Routerlarni ulash
dp.include_router(start.router)
dp.include_router(facts.router)
dp.include_router(admin.router)

# Webhook endpoint
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
async def webhook():
    data = request.get_json()
    if data:
        update = Update.model_validate(data)
        await dp.feed_webhook_update(bot, update)
    return "ok"

# Lokal test uchun ishga tushirish
if __name__ == "__main__":
    create_tables()
    app.run(host="0.0.0.0", port=8000)

