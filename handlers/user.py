from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.api import get_temperature
from core.recommendations import goal_map
from core.utils import (
    calculate_calorie_goal,
    calculate_water_goal,
)
from states.forms import ProfileForm
from storage.user import get_user, reset_daily_logs

router = Router()

goal_display = {
    "похудение": "📉 Похудение (дефицит калорий)",
    "массонабор": "📈 Массонабор (профицит калорий)",
    "поддержка": "⚖️ Поддержка текущего веса",
}


@router.message(Command("set_profile"))
async def cmd_set_profile(message: Message, state: FSMContext):
    """Начать процесс настройки профиля."""
    await message.answer("Давайте настроим ваш профиль! 📊\n\nВведите ваш вес (в кг):")
    await state.set_state(ProfileForm.weight)


@router.message(ProfileForm.weight)
async def process_weight(message: Message, state: FSMContext):
    """Обработать вес пользователя."""
    try:
        weight = float(message.text.replace(",", "."))

        await state.update_data(weight=weight)
        await message.answer(
            f"Вес сохранён: {weight} кг ✅\n\nВведите ваш рост (в см):"
        )
        await state.set_state(ProfileForm.height)
    except ValueError:
        await message.answer("Пожалуйста, введите число (например: 80 или 80.5):")


@router.message(ProfileForm.height)
async def process_height(message: Message, state: FSMContext):
    """Обработать рост пользователя."""
    try:
        height = float(message.text.replace(",", "."))

        await state.update_data(height=height)
        await message.answer(f"Рост сохранён: {height} см ✅\n\nВведите ваш возраст:")
        await state.set_state(ProfileForm.age)
    except ValueError:
        await message.answer("Пожалуйста, введите число (например: 25):")


@router.message(ProfileForm.age)
async def process_age(message: Message, state: FSMContext):
    """Обработать возраст пользователя."""
    try:
        age = int(message.text)

        await state.update_data(age=age)
        await message.answer(
            f"Возраст сохранён: {age} лет ✅\n\n"
            "Сколько минут активности у вас в день? (включая тренировки, ходьбу и т.д.)"
        )
        await state.set_state(ProfileForm.activity)
    except ValueError:
        await message.answer("Пожалуйста, введите целое число (например: 30):")


@router.message(ProfileForm.activity)
async def process_activity(message: Message, state: FSMContext):
    """Обработать уровень активности пользователя."""
    try:
        activity = int(message.text)

        await state.update_data(activity_minutes=activity)
        await message.answer(
            f"Активность сохранена: {activity} минут в день ✅\n\n"
            "В каком городе вы находитесь? (для учёта температуры)"
        )
        await state.set_state(ProfileForm.city)
    except ValueError:
        await message.answer("Пожалуйста, введите целое число (например: 45):")


@router.message(ProfileForm.city)
async def process_city(message: Message, state: FSMContext):
    """Обработать город пользователя и запросить цель."""
    city = message.text.strip()
    await state.update_data(city=city)

    await message.answer(
        f"Город сохранён: {city} ✅\n\n"
        "Какова ваша цель? Выберите один из вариантов:\n\n"
        "1️⃣ Похудение (дефицит калорий)\n"
        "2️⃣ Массонабор (профицит калорий)\n"
        "3️⃣ Поддержка текущего веса\n\n"
        "Введите номер (1, 2 или 3):"
    )
    await state.set_state(ProfileForm.goal)


@router.message(ProfileForm.goal)
async def process_goal(message: Message, state: FSMContext):
    """Обработать цель пользователя"""
    goal_text = message.text.strip()

    goal = goal_map.get(goal_text)

    await state.update_data(goal=goal)

    data = await state.get_data()

    weight = data["weight"]
    height = data["height"]
    age = data["age"]
    activity_minutes = data["activity_minutes"]
    city = data["city"]

    temperature = await get_temperature(city)

    water_goal = calculate_water_goal(weight, activity_minutes, temperature)
    calorie_goal = calculate_calorie_goal(weight, height, age, activity_minutes, goal)

    user = get_user(message.from_user.id)
    user["weight"] = weight
    user["height"] = height
    user["age"] = age
    user["activity_minutes"] = activity_minutes
    user["city"] = city
    user["goal"] = goal
    user["water_goal"] = water_goal
    user["calorie_goal"] = calorie_goal

    reset_daily_logs(message.from_user.id)

    temp_text = f"{temperature}°C" if temperature else "не удалось получить"

    response = (
        f"Профиль успешно настроен! ✅\n\n"
        f"📊 Ваши данные:\n"
        f"Вес: {weight} кг\n"
        f"Рост: {height} см\n"
        f"Возраст: {age} лет\n"
        f"Активность: {activity_minutes} мин/день\n"
        f"Город: {city} (температура: {temp_text})\n"
        f"Цель: {goal_display.get(goal, goal)}\n\n"
        f"🎯 Ваши дневные нормы:\n"
        f"Вода: {water_goal} мл\n"
        f"Калории: {calorie_goal} ккал\n\n"
        f"Используйте команды:\n"
        f"/log_water <количество> - добавить воду\n"
        f"/log_food <продукт> - добавить еду\n"
        f"/log_workout <тип> <время> - добавить тренировку\n"
        f"/check_progress - посмотреть прогресс\n"
        f"/recommendations - получить рекомендации по продуктам и тренировкам\n"
        f"/graph - посмотреть график\n"
        f"/help - получить справку по командам\n"
        f"/start - начать заново"
    )

    await message.answer(response)
    await state.clear()


@router.message(Command("profile"))
async def cmd_show_profile(message: Message):
    user = get_user(message.from_user.id)

    weight = user["weight"]
    height = user["height"]
    age = user["age"]
    activity_minutes = user["activity_minutes"]
    city = user["city"]
    goal = user["goal"]
    water_goal = user["water_goal"]
    calorie_goal = user["calorie_goal"]

    temperature = await get_temperature(city)

    temp_text = f"{temperature}°C" if temperature else "не удалось получить"

    response = (
        f"Профиль успешно настроен! ✅\n\n"
        f"📊 Ваши данные:\n"
        f"Вес: {weight} кг\n"
        f"Рост: {height} см\n"
        f"Возраст: {age} лет\n"
        f"Активность: {activity_minutes} мин/день\n"
        f"Город: {city} (температура: {temp_text})\n"
        f"Цель: {goal_display.get(goal, goal)}\n\n"
        f"🎯 Ваши дневные нормы:\n"
        f"Вода: {water_goal} мл\n"
        f"Калории: {calorie_goal} ккал\n\n"
        f"Используйте команды:\n"
        f"/log_water <количество> - добавить воду\n"
        f"/log_food <продукт> - добавить еду\n"
        f"/log_workout <тип> <время> - добавить тренировку\n"
        f"/check_progress - посмотреть прогресс\n"
        f"/recommendations - получить рекомендации по продуктам и тренировкам\n"
        f"/graph - посмотреть график\n"
        f"/help - получить справку по командам\n"
        f"/start - начать заново"
    )

    await message.answer(response)
