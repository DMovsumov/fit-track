from typing import Dict, List

from storage.user import get_today_log, get_user

goal_map = {
    "1": "похудение",
    "2": "массонабор",
    "3": "поддержка",
}

# База данных низкокалорийных продуктов
LOW_CALORIE_FOODS = [
    {
        "name": "Огурец",
        "calories_per_100g": 16,
        "description": "Очень низкокалорийный, богат водой",
    },
    {
        "name": "Помидор",
        "calories_per_100g": 18,
        "description": "Низкокалорийный, содержит ликопин",
    },
    {
        "name": "Салат листовой",
        "calories_per_100g": 15,
        "description": "Минимум калорий, максимум витаминов",
    },
    {
        "name": "Капуста",
        "calories_per_100g": 25,
        "description": "Низкокалорийная, богата клетчаткой",
    },
    {
        "name": "Брокколи",
        "calories_per_100g": 34,
        "description": "Низкокалорийная, много белка и витаминов",
    },
    {
        "name": "Цветная капуста",
        "calories_per_100g": 25,
        "description": "Низкокалорийная, универсальная",
    },
    {
        "name": "Шпинат",
        "calories_per_100g": 23,
        "description": "Низкокалорийный, богат железом",
    },
    {
        "name": "Грейпфрут",
        "calories_per_100g": 42,
        "description": "Низкокалорийный фрукт, помогает метаболизму",
    },
    {
        "name": "Арбуз",
        "calories_per_100g": 30,
        "description": "Низкокалорийный, много воды",
    },
    {
        "name": "Яблоко",
        "calories_per_100g": 52,
        "description": "Низкокалорийное, богато клетчаткой",
    },
    {
        "name": "Груша",
        "calories_per_100g": 57,
        "description": "Низкокалорийная, содержит пектин",
    },
    {
        "name": "Морковь",
        "calories_per_100g": 41,
        "description": "Низкокалорийная, богата бета-каротином",
    },
    {
        "name": "Перец болгарский",
        "calories_per_100g": 27,
        "description": "Низкокалорийный, много витамина C",
    },
    {
        "name": "Кабачок",
        "calories_per_100g": 24,
        "description": "Низкокалорийный, универсальный в готовке",
    },
    {
        "name": "Грибы",
        "calories_per_100g": 22,
        "description": "Очень низкокалорийные, источник белка",
    },
]

# База данных высококалорийных продуктов для массонабора
HIGH_CALORIE_FOODS = [
    {
        "name": "Авокадо",
        "calories_per_100g": 160,
        "description": "Высококалорийный, полезные жиры",
    },
    {
        "name": "Орехи (миндаль)",
        "calories_per_100g": 579,
        "description": "Очень калорийные, много белка и жиров",
    },
    {
        "name": "Арахис",
        "calories_per_100g": 567,
        "description": "Высококалорийный, источник белка",
    },
    {
        "name": "Оливковое масло",
        "calories_per_100g": 884,
        "description": "Очень калорийное, полезные жиры",
    },
    {
        "name": "Лосось",
        "calories_per_100g": 208,
        "description": "Калорийный, много белка и омега-3",
    },
    {
        "name": "Куриная грудка",
        "calories_per_100g": 165,
        "description": "Калорийная, много белка",
    },
    {
        "name": "Яйца",
        "calories_per_100g": 155,
        "description": "Калорийные, полноценный белок",
    },
    {
        "name": "Творог",
        "calories_per_100g": 159,
        "description": "Калорийный, много белка",
    },
    {
        "name": "Гречка",
        "calories_per_100g": 343,
        "description": "Калорийная, сложные углеводы",
    },
    {
        "name": "Рис",
        "calories_per_100g": 365,
        "description": "Калорийный, источник энергии",
    },
    {
        "name": "Овсянка",
        "calories_per_100g": 389,
        "description": "Калорийная, медленные углеводы",
    },
    {
        "name": "Банан",
        "calories_per_100g": 89,
        "description": "Калорийный фрукт, быстрая энергия",
    },
    {
        "name": "Финики",
        "calories_per_100g": 282,
        "description": "Очень калорийные, натуральный сахар",
    },
    {
        "name": "Мёд",
        "calories_per_100g": 304,
        "description": "Очень калорийный, натуральная энергия",
    },
]

# База данных тренировок
WORKOUTS_FOR_WEIGHT_LOSS = [
    {
        "type": "бег",
        "minutes": 30,
        "calories_burned_per_kg": 0.12,
        "description": "Отличная кардио-тренировка для сжигания калорий",
    },
    {
        "type": "быстрая ходьба",
        "minutes": 45,
        "calories_burned_per_kg": 0.08,
        "description": "Низкая нагрузка, но эффективное сжигание калорий",
    },
    {
        "type": "велосипед",
        "minutes": 40,
        "calories_burned_per_kg": 0.10,
        "description": "Кардио-тренировка с низкой нагрузкой на суставы",
    },
    {
        "type": "плавание",
        "minutes": 30,
        "calories_burned_per_kg": 0.10,
        "description": "Полноценная тренировка всего тела",
    },
    {
        "type": "аэробика",
        "minutes": 30,
        "calories_burned_per_kg": 0.11,
        "description": "Интенсивная кардио-тренировка",
    },
    {
        "type": "интервальная тренировка",
        "minutes": 20,
        "calories_burned_per_kg": 0.15,
        "description": "Высокоинтенсивная тренировка для максимального сжигания",
    },
]

WORKOUTS_FOR_MASS_GAIN = [
    {
        "type": "силовая",
        "minutes": 45,
        "calories_burned_per_kg": 0.08,
        "description": "Тренировка для набора мышечной массы",
    },
    {
        "type": "тренировка с отягощениями",
        "minutes": 60,
        "calories_burned_per_kg": 0.07,
        "description": "Интенсивная силовая тренировка",
    },
    {
        "type": "кроссфит",
        "minutes": 30,
        "calories_burned_per_kg": 0.12,
        "description": "Комплексная тренировка силы и выносливости",
    },
    {
        "type": "йога",
        "minutes": 60,
        "calories_burned_per_kg": 0.03,
        "description": "Низкая интенсивность, но помогает восстановлению",
    },
    {
        "type": "пилатес",
        "minutes": 45,
        "calories_burned_per_kg": 0.04,
        "description": "Укрепление мышц кора и гибкость",
    },
]

WORKOUTS_FOR_MAINTENANCE = [
    {
        "type": "ходьба",
        "minutes": 30,
        "calories_burned_per_kg": 0.06,
        "description": "Умеренная активность для поддержания формы",
    },
    {
        "type": "велосипед",
        "minutes": 30,
        "calories_burned_per_kg": 0.10,
        "description": "Кардио-тренировка средней интенсивности",
    },
    {
        "type": "плавание",
        "minutes": 30,
        "calories_burned_per_kg": 0.10,
        "description": "Сбалансированная тренировка всего тела",
    },
    {
        "type": "йога",
        "minutes": 45,
        "calories_burned_per_kg": 0.03,
        "description": "Гибкость и баланс",
    },
]


def get_food_recommendations(user_id: int, count: int = 5) -> List[Dict]:
    user = get_user(user_id)
    goal = user.get("goal", "поддержка")

    today_log = get_today_log(user_id)
    consumed_calories = today_log.get("calories", 0)
    calorie_goal = user.get("calorie_goal", 2000)

    # Нужны ли доп калории
    remaining_calories = calorie_goal - consumed_calories

    if goal == "похудение":
        recommendations = LOW_CALORIE_FOODS[:count]
    elif goal == "массонабор":
        if remaining_calories > 300:
            recommendations = HIGH_CALORIE_FOODS[:count]
        else:
            recommendations = [
                f
                for f in HIGH_CALORIE_FOODS
                if "белок" in f["description"].lower()
                or "протеин" in f["description"].lower()
            ][:count]
            if not recommendations:
                recommendations = HIGH_CALORIE_FOODS[:count]
    else:
        if remaining_calories > 200:
            recommendations = (
                HIGH_CALORIE_FOODS[: count // 2] + LOW_CALORIE_FOODS[: count // 2]
            )
        else:
            recommendations = LOW_CALORIE_FOODS[:count]

    return recommendations[:count]


def get_workout_recommendations(user_id: int, count: int = 3) -> List[Dict]:
    user = get_user(user_id)
    goal = user.get("goal", "поддержка")
    weight = user.get("weight", 70)

    if goal == "похудение":
        workouts = WORKOUTS_FOR_WEIGHT_LOSS
    elif goal == "массонабор":
        workouts = WORKOUTS_FOR_MASS_GAIN
    else:
        workouts = WORKOUTS_FOR_MAINTENANCE

    recommendations = []

    for workout in workouts[:count]:
        estimated_calories = (
            workout["calories_burned_per_kg"] * weight * workout["minutes"]
        )

        recommendations.append(
            {**workout, "estimated_calories": round(estimated_calories, 1)}
        )

    return recommendations
