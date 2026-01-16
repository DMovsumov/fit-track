from aiogram.fsm.state import State, StatesGroup


class ProfileForm(StatesGroup):
    weight = State()
    height = State()
    age = State()
    activity = State()
    city = State()
    goal = State()  # Цель: похудение, массонабор, поддержка


class FoodForm(StatesGroup):
    product_name = State()
    amount = State()  # количество в граммах
