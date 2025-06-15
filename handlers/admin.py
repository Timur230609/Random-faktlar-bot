from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from keyboards.admin_btns import category_keyboard, admin_menu
from database.db import insert_fact
from aiogram.filters import Command
from states.state import MultiLangFact
router = Router()


@router.message(Command("admin"))
async def admin_menu_start(message: Message):
    await message.answer("Admin menyusi:", reply_markup=admin_menu())



# --- Start fact qo'shish ---
@router.callback_query(F.data == "admin_add_multilang")
async def start_multilang(callback: CallbackQuery, state: FSMContext):
    await state.set_state(MultiLangFact.waiting_for_category)
    await callback.message.answer("Kategoriya tanlang:", reply_markup=category_keyboard())
    await callback.answer()

# --- Kategoriya tanlanganda ---
@router.message(F.text == "➕ Fakt qo‘shish")
async def handle_add_fact_button(message: Message, state: FSMContext):
    await state.set_state(MultiLangFact.waiting_for_category)
    await message.answer("Kategoriya tanlang:", reply_markup=category_keyboard(lang="uz"))  # Tilni istalgancha o‘zgartirsa bo‘ladi


@router.message(MultiLangFact.waiting_for_category)
async def ask_fact_uz(message: Message, state: FSMContext):
    category_text = message.text.strip().lower()

    category_map = {
        "🐾 hayvonlar": "hayvonlar",
        "🌌 kosmos": "kosmos",
        "🧠 inson tanasi": "tana",
    }
    category = category_map.get(category_text)

    if not category:
        await message.answer("❌ Noto‘g‘ri kategoriya. Qaytadan tanlang.")
        return

    await state.update_data(category=category)
    await state.set_state(MultiLangFact.waiting_for_fact_uz)
    await message.answer("Fakt matnini *O‘zbek tilida* kiriting:", reply_markup=ReplyKeyboardRemove())

# --- O'zbekcha fakt qabul qilish ---
@router.message(MultiLangFact.waiting_for_fact_uz)
async def ask_fact_ru(message: Message, state: FSMContext):
    await state.update_data(fact_uz=message.text.strip())
    await state.set_state(MultiLangFact.waiting_for_fact_ru)
    await message.answer("Fakt matnini *Rus tilida* kiriting:")

# --- Ruscha fakt qabul qilish ---
@router.message(MultiLangFact.waiting_for_fact_ru)
async def ask_fact_en(message: Message, state: FSMContext):
    await state.update_data(fact_ru=message.text.strip())
    await state.set_state(MultiLangFact.waiting_for_fact_en)
    await message.answer("Fakt matnini *Ingliz tilida* kiriting:")

# --- Inglizcha fakt qabul qilish va bazaga qo'shish ---
@router.message(MultiLangFact.waiting_for_fact_en)
async def save_fact(message: Message, state: FSMContext):
    try:
        await state.update_data(fact_en=message.text.strip())
        data = await state.get_data()

        print("✅ State dan olingan data:", data)  # <-- Debug uchun

        # Bazaga saqlash
        insert_fact(category=data["category"], lang="uz", text=data["fact_uz"])
        insert_fact(category=data["category"], lang="ru", text=data["fact_ru"])
        insert_fact(category=data["category"], lang="en", text=data["fact_en"])

        await message.answer("✅ Faktlar 3 tilda saqlandi!", reply_markup=admin_menu())
        await state.clear()

    except Exception as e:
        await message.answer(f"❌ Xatolik yuz berdi: {e}")
        print("❌ Xatolik:", e)
