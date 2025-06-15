from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from text import TEXTS  # to‘g‘ri papka nomi

lang = "uz" 

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=TEXTS[lang]["more_fact"])]
    ],
    resize_keyboard=True
)

def get_more_fact_keyboard(lang: str):

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=TEXTS[lang]["more_fact"])]
        ],
        resize_keyboard=True
    )

