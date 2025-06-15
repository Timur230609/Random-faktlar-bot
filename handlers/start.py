from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.buttons import keyboard
from database.db import get_random_fact
from text import TEXTS

router = Router()

# === HOLATLAR ===
class LanguageState(StatesGroup):
    choosing = State()

# === /start KOMANDASI ===
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.button(text="🇺🇿 O‘zbek", callback_data="lang_uz")
    builder.button(text="🇷🇺 Русский", callback_data="lang_ru")
    builder.button(text="🇬🇧 English", callback_data="lang_en")

    await message.answer("Iltimos, tilni tanlang:", reply_markup=builder.as_markup())
    await state.set_state(LanguageState.choosing)

# === TIL TANLASH ===
@router.callback_query(LanguageState.choosing)
async def choose_language(callback: CallbackQuery, state: FSMContext):
    _, lang = callback.data.split("_")
    await state.update_data(lang=lang)

    # Tildagi matnlar va kategoriyalar
    texts = TEXTS.get(lang, TEXTS["uz"])
    categories = {
        "uz": [("🐾 Hayvonlar", "hayvonlar"),
               ("🌌 Kosmos", "kosmos"),
               ("🧠 Inson tanasi", "tana")],
        "ru": [("🐾 Животные", "hayvonlar"),
               ("🌌 Космос", "kosmos"),
               ("🧠 Человеческое тело", "tana")],
        "en": [("🐾 Animals", "hayvonlar"),
               ("🌌 Space", "kosmos"),
               ("🧠 Human Body", "tana")],
    }
    cat_list = categories.get(lang, categories["uz"])

    builder = InlineKeyboardBuilder()
    for text, cb_data in cat_list:
        builder.button(text=text, callback_data=f"cat_{cb_data}")

    await callback.message.answer(texts["greeting"])
    await callback.message.answer(texts["choose_category"], reply_markup=builder.as_markup())
    await state.set_state(None)
    await callback.answer()

# === FAKTNI CHIQARISH ===
@router.callback_query(F.data.startswith("cat_"))
async def send_fact(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")
    category = callback.data.split("_")[1]

    await state.update_data(category=category)

    fact = get_random_fact(category, lang)
    if fact:
        await callback.message.answer(f"📌 {fact}", reply_markup=keyboard)
    else:
        msg = {
            "uz": "😔 Bu kategoriya uchun fakt mavjud emas.",
            "ru": "😔 Факт для этой категории отсутствует.",
            "en": "😔 No fact available for this category."
        }.get(lang, "😔 Fakt mavjud emas.")
        await callback.message.answer(msg)

    await callback.answer()

# === 🔁 YANA FAKT TUGMASI ===
@router.message(lambda message: message.text.startswith("🔁"))
async def more_fact(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")
    category = data.get("category", "hayvonlar")

    fact = get_random_fact(category, lang)
    if fact:
        await message.answer(f"📌 {fact}", reply_markup=keyboard)
    else:
        msg = {
            "uz": "😔 Fakt topilmadi.",
            "ru": "😔 Факт не найден.",
            "en": "😔 Fact not found."
        }.get(lang, "😔 Fakt topilmadi.")
        await message.answer(msg)
