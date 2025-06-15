from aiogram.fsm.state import StatesGroup, State

# --- FSM States ---
class MultiLangFact(StatesGroup):
    waiting_for_category = State()
    waiting_for_fact_uz = State()
    waiting_for_fact_ru = State()
    waiting_for_fact_en = State()
