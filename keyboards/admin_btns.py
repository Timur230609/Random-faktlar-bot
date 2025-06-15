from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup


def admin_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="➕ Fakt qo‘shish")
    return builder.as_markup(resize_keyboard=True)


def category_keyboard(lang: str) -> ReplyKeyboardMarkup:
    categories = {
        "uz": ["🐾 Hayvonlar", "🌌 Kosmos", "🧠 Inson tanasi"],
        "ru": ["🐾 Животные", "🌌 Космос", "🧠 Человеческое тело"],
        "en": ["🐾 Animals", "🌌 Space", "🧠 Human Body"],
    }

    builder = ReplyKeyboardBuilder()
    for name in categories.get(lang, categories["uz"]):
        builder.button(text=name)
    builder.button(text="🔙 Orqaga")
    return builder.as_markup(resize_keyboard=True)
