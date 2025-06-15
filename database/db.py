import sqlite3
import random
import os
from test_insert import facts  # test_insert.py faylidagi TEST_FACTS dict

DB_PATH = "data.db"
os.makedirs("database", exist_ok=True)


def create_tables():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    # facts jadvalini yaratamiz (agar mavjud bo'lmasa)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            category TEXT NOT NULL,
            lang TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

# --- Fakt qo‘shish ---

def insert_fact(text, category, lang):
    import sqlite3
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO facts (text, category, lang) VALUES (?, ?, ?)", (text, category, lang))
    
    conn.commit()
    conn.close()
    
# --- Random test faktni olish (test_insert dan foydalanadi) ---

def get_random_fact(category: str, lang: str) -> str:
    conn = sqlite3.connect("data.db")  # To‘liq yo‘lni ko‘rsating
    cursor = conn.cursor()

    cursor.execute("SELECT text FROM facts WHERE category = ? AND lang = ?", (category, lang))
    results = cursor.fetchall()
    conn.close()

    if results:
        return random.choice(results)[0]
    else:
        return None