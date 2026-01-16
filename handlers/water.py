from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from storage.user import get_today_log, get_user

router = Router()


@router.message(Command("log_water"))
async def cmd_log_water(message: Message):
    """Логировать потребление воды."""
    user = get_user(message.from_user.id)

    if user["water_goal"] is None:
        await message.answer(
            "❌ Профиль не настроен. Используйте /set_profile для настройки профиля."
        )
        return

    # Парсим количество воды из команды
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer(
            "Использование: /log_water <количество>\n"
            "Пример: /log_water 500 (добавить 500 мл воды)"
        )
        return

    try:
        amount = float(parts[1].replace(",", "."))
        if amount <= 0:
            await message.answer("Пожалуйста, введите положительное число.")
            return

        today_log = get_today_log(message.from_user.id)
        today_log["water"] += amount

        # Рассчитываем оставшееся количество
        remaining = max(0, user["water_goal"] - today_log["water"])
        progress_percent = min(100, (today_log["water"] / user["water_goal"]) * 100)

        response = (
            f"💧 Вода добавлена: {amount} мл\n\n"
            f"📊 Прогресс по воде:\n"
            f"- Выпито: {today_log['water']:.1f} мл из {user['water_goal']:.1f} мл\n"
            f"- Осталось: {remaining:.1f} мл\n"
            f"- Прогресс: {progress_percent:.1f}%"
        )

        if today_log["water"] >= user["water_goal"]:
            response += "\n\n🎉 Поздравляем! Вы выполнили дневную норму воды!"

        await message.answer(response)
    except ValueError:
        await message.answer(
            "Пожалуйста, введите число (например: 500 или 0.5 для литров)."
        )
