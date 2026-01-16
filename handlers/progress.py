from aiogram import Router
from aiogram.filters import Command
from aiogram.types import BufferedInputFile, Message

from core.graphs import create_progress_graph
from core.recommendations import get_food_recommendations, get_workout_recommendations
from storage.user import get_today_log, get_user

router = Router()


@router.message(Command("check_progress"))
async def cmd_check_progress(message: Message):
    """Показать текущий прогресс пользователя."""
    user = get_user(message.from_user.id)

    if user["water_goal"] is None or user["calorie_goal"] is None:
        await message.answer(
            "❌ Профиль не настроен. Используйте /set_profile для настройки профиля."
        )
        return

    today_log = get_today_log(message.from_user.id)

    water_consumed = today_log["water"]
    water_remaining = max(0, user["water_goal"] - water_consumed)
    water_progress = min(100, (water_consumed / user["water_goal"]) * 100)

    calories_consumed = today_log["calories"]
    calories_burned = today_log["burned_calories"]
    calories_balance = calories_consumed - calories_burned
    calories_remaining = max(0, user["calorie_goal"] - calories_balance)
    calories_progress = (
        min(100, ((calories_balance) / user["calorie_goal"]) * 100)
        if user["calorie_goal"] > 0
        else 0
    )

    goal_display = {
        "похудение": "Похудение (дефицит)",
        "массонабор": "Массонабор (профицит)",
        "поддержка": "Поддержка веса",
    }

    goal_text = ""
    if user.get("goal"):
        goal_text = f"\n🎯 Цель: {goal_display.get(user['goal'], user['goal'])}\n"

    response = (
        f"📊 Ваш прогресс на сегодня:{goal_text}\n"
        f"💧 Вода:\n"
        f"- Выпито: {water_consumed:.1f} мл из {user['water_goal']:.1f} мл\n"
        f"- Осталось: {water_remaining:.1f} мл\n"
        f"- Прогресс: {water_progress:.1f}%\n"
        f"🔥 Калории:\n"
        f"- Потреблено: {calories_consumed:.1f} ккал\n"
        f"- Сожжено: {calories_burned:.1f} ккал\n"
        f"- Баланс: {calories_balance:.1f} ккал из {user['calorie_goal']:.1f} ккал\n"
        f"- Осталось: {calories_remaining:.1f} ккал\n"
        f"- Прогресс: {calories_progress:.1f}%\n"
    )

    if today_log["foods"]:
        response += f"🍽️ Съедено продуктов: {len(today_log['foods'])}\n"
        for food in today_log["foods"][-5:]:
            response += (
                f"  • {food['name']}: {food['amount']}г ({food['calories']:.1f} ккал)\n"
            )
        if len(today_log["foods"]) > 5:
            response += f"  ... и ещё {len(today_log['foods']) - 5}\n"
        response += "\n"

    if today_log["workouts"]:
        response += f"🏋️ Тренировок выполнено: {len(today_log['workouts'])}\n"
        for workout in today_log["workouts"][-5:]:
            response += f"  • {workout['type']}: {workout['minutes']} мин ({workout['calories']:.1f} ккал)\n"
        if len(today_log["workouts"]) > 5:
            response += f"  ... и ещё {len(today_log['workouts']) - 5}\n"

    await message.answer(response)


@router.message(Command("graph"))
async def cmd_graph(message: Message):
    """Показать график прогресса по воде и калориям."""
    user = get_user(message.from_user.id)

    if not user.get("daily_logs"):
        await message.answer(
            "❌ У вас пока нет данных для построения графика.\n"
            "Начните логировать воду и еду, чтобы увидеть свой прогресс!"
        )
        return

    parts = message.text.split()
    days = 7

    if len(parts) > 1:
        try:
            days = int(parts[1])
            if days < 2 or days > 30:
                # Кол-во дней не должно быть меньше 2 и больше 30, иначе график не будет построен
                days = 7
        except ValueError:
            days = 7

    await message.answer("📈 Строю график прогресса...")

    graph_buffer = create_progress_graph(message.from_user.id, days)

    if graph_buffer is None:
        await message.answer("Не удалось построить график. Проверьте, данные.")
        return

    graph_file = BufferedInputFile(graph_buffer.read(), filename="progress_graph.png")

    await message.answer_photo(
        graph_file, caption=f"📊 Ваш прогресс за последние {days} дней"
    )


@router.message(Command("recommendations"))
async def cmd_recommendations(message: Message):
    """Рекомендации по продуктам и тренировкам."""
    user = get_user(message.from_user.id)

    if user.get("goal") is None:
        await message.answer(
            "❌ Профиль не настроен. Используйте /set_profile для настройки профиля."
        )
        return

    goal = user.get("goal", "поддержка")

    goal_display = {
        "похудение": "📉 Похудение",
        "массонабор": "📈 Массонабор",
        "поддержка": "⚖️ Поддержка веса",
    }

    food_recs = get_food_recommendations(message.from_user.id, count=5)
    workout_recs = get_workout_recommendations(message.from_user.id, count=3)

    response = f"💡 Рекомендации для вашей цели ({goal_display.get(goal, goal)}):\n\n"

    response += "🍽️ Рекомендуемые продукты:\n"
    for i, food in enumerate(food_recs, 1):
        response += (
            f"{i}. {food['name']} - {food['calories_per_100g']} ккал/100г\n"
            f"   {food.get('description', '')}\n\n"
        )

    response += "🏋️ Рекомендуемые тренировки:\n"
    for i, workout in enumerate(workout_recs, 1):
        response += (
            f"{i}. {workout['type'].title()} ({workout['minutes']} мин)\n"
            f"   {workout['description']}\n"
            f"   Примерно сожжётся: ~{workout['estimated_calories']:.0f} ккал\n\n"
        )

    # Доп советы в зависимости от цели
    today_log = get_today_log(message.from_user.id)
    consumed_calories = today_log.get("calories", 0)
    calorie_goal = user.get("calorie_goal", 2000)
    remaining = calorie_goal - consumed_calories

    # TODO: убрать кучу условий
    response += "💬 Советы:\n"
    if goal == "похудение":
        if remaining > 0:
            response += f"- У вас осталось {remaining:.0f} ккал до цели. Выбирайте низкокалорийные продукты.\n"
        else:
            response += "- Вы уже достигли дневной нормы калорий. Отличная работа! 🎉\n"
        response += "- Рекомендуется сочетать кардио-тренировки с силовыми для лучшего результата.\n"
    elif goal == "массонабор":
        if remaining > 0:
            response += f"- Вам нужно добавить ещё {remaining:.0f} ккал. Выбирайте высококалорийные продукты.\n"
        else:
            response += "- Вы уже достигли дневной нормы калорий. Отлично! 🎉\n"
        response += "- Фокус на силовых тренировках для набора мышечной массы.\n"
    else:
        if abs(remaining) < 200:
            response += "- Ваш баланс калорий близок к идеальному! 👍\n"
        elif remaining > 0:
            response += f"- Вам можно добавить ещё {remaining:.0f} ккал.\n"
        else:
            response += f"- Вы превысили норму на {abs(remaining):.0f} ккал. Рассмотрите дополнительную тренировку.\n"
        response += "- Поддерживайте баланс между кардио и силовыми тренировками.\n"

    await message.answer(response)
