from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from core.utils import (
    calculate_workout_calories,
    calculate_workout_water,
)
from storage.user import get_today_log, get_user

router = Router()


@router.message(Command("log_workout"))
async def cmd_log_workout(message: Message):
    """Логировать тренировку."""
    user = get_user(message.from_user.id)

    if user["weight"] is None:
        await message.answer(
            "❌ Профиль не настроен. Используйте /set_profile для настройки профиля."
        )
        return

    parts = message.text.split()
    if len(parts) < 3:
        await message.answer(
            "Использование: /log_workout <тип тренировки> <время в минутах>\n"
            "Пример: /log_workout бег 30\n\n"
            "Доступные типы: бег, ходьба, плавание, велосипед, силовая, йога и др."
        )
        return

    workout_type = parts[1]

    try:
        minutes = int(parts[2])
        if minutes <= 0:
            await message.answer("Пожалуйста, введите положительное число минут.")
            return
    except ValueError:
        await message.answer("Пожалуйста, введите целое число минут (например: 30).")
        return

    burned_calories = calculate_workout_calories(workout_type, minutes, user["weight"])
    additional_water = calculate_workout_water(minutes)

    today_log = get_today_log(message.from_user.id)
    today_log["burned_calories"] += burned_calories
    today_log["workouts"].append(
        {"type": workout_type, "minutes": minutes, "calories": burned_calories}
    )

    user = get_user(message.from_user.id)
    remaining_calories = max(
        0, user["calorie_goal"] - today_log["calories"] + today_log["burned_calories"]
    )

    response = (
        f"Тренировка записана: {workout_type} {minutes} минут\n"
        f"🔥 Сожжено калорий: {burned_calories:.1f} ккал\n"
        f"💧 Рекомендуется выпить дополнительно: {additional_water:.1f} мл воды\n\n"
        f"📊 Прогресс по калориям:\n"
        f"- Потреблено: {today_log['calories']:.1f} ккал\n"
        f"- Сожжено: {today_log['burned_calories']:.1f} ккал\n"
        f"- Баланс: {today_log['calories'] - today_log['burned_calories']:.1f} ккал из {user['calorie_goal']:.1f} ккал\n"
        f"- Осталось: {remaining_calories:.1f} ккал"
    )

    await message.answer(response)
