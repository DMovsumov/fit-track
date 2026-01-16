from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.api import get_food_info
from states.forms import FoodForm
from storage.user import get_today_log, get_user

router = Router()


@router.message(Command("log_food"))
async def cmd_log_food(message: Message, state: FSMContext):
    """Логирования еды."""
    user = get_user(message.from_user.id)

    if user["calorie_goal"] is None:
        await message.answer(
            "❌ Профиль не настроен. Используйте /set_profile для настройки профиля."
        )
        return

    parts = message.text.split(" ")

    product_name = parts[1]
    await state.update_data(product_name=product_name)

    await message.answer(f"🔍 Ищу информацию о продукте '{product_name}'...")

    food_info = await get_food_info(product_name)

    if not food_info:
        await message.answer(
            f"❌ Не удалось найти информацию о продукте '{product_name}'.\n"
            f"Попробуйте другое название или проверьте написание.\n\n"
        )
        await state.clear()
        return

    await state.update_data(
        food_name=food_info["name"], calories_per_100g=food_info["calories_per_100g"]
    )

    await message.answer(
        f"✅ Найден продукт: {food_info['name']}\n"
        f"📊 Калорийность: {food_info['calories_per_100g']} ккал на 100 г\n\n"
        f"Сколько грамм вы съели?"
    )
    await state.set_state(FoodForm.amount)


@router.message(FoodForm.amount)
async def process_food_amount(message: Message, state: FSMContext):
    """Обработать количество съеденного продукта."""
    try:
        amount = float(message.text.replace(",", "."))

        data = await state.get_data()

        food_name = data["food_name"]
        calories_per_100g = data["calories_per_100g"]

        calories = (amount / 100) * calories_per_100g

        today_log = get_today_log(message.from_user.id)
        today_log["calories"] += calories
        today_log["foods"].append(
            {"name": food_name, "amount": amount, "calories": calories}
        )

        user = get_user(message.from_user.id)
        remaining = max(
            0,
            user["calorie_goal"] - today_log["calories"] + today_log["burned_calories"],
        )
        progress_percent = min(
            100,
            (
                (today_log["calories"] - today_log["burned_calories"])
                / user["calorie_goal"]
            )
            * 100,
        )

        response = (
            f"✅ Записано: {food_name} — {calories:.1f} ккал ({amount} г)\n\n"
            f"📊 Прогресс по калориям:\n"
            f"- Потреблено: {today_log['calories']:.1f} ккал\n"
            f"- Сожжено: {today_log['burned_calories']:.1f} ккал\n"
            f"- Баланс: {today_log['calories'] - today_log['burned_calories']:.1f} ккал из {user['calorie_goal']:.1f} ккал\n"
            f"- Осталось: {remaining:.1f} ккал\n"
            f"- Прогресс: {progress_percent:.1f}%"
        )

        await message.answer(response)
        await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введите число (например: 150 или 150.5):")
