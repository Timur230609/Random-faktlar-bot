from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from database.db import get_random_fact

router = Router()

@router.callback_query(F.data.startswith("cat_"))
async def send_fact(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")
    category = callback.data.split("_")[1]

    # Kategoriya va tilni saqlab qo'yish kerak
    await state.update_data(category=category, lang=lang)

    print(f">>> Lang: {lang}, Cat: {category}")  # Test

    fact = get_random_fact(category, lang)
    await callback.message.answer(f"📌 {fact}")
    await callback.answer()

@router.message(lambda message: message.text.startswith("🔁"))
async def more_fact(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")
    category = data.get("category", "hayvonlar")  # oldingi tanlangan kategoriya

    fact = get_random_fact(category, lang)
    await message.answer(f"📌 {fact}")
