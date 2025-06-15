import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

load_dotenv()

BOT_TOKEN="7984680821:AAHAyCfl9seX1HtiY3bYESEKhLklqbaFarM"
ADMIN_IDS=[7776081021]

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

dp = Dispatcher(storage=MemoryStorage())