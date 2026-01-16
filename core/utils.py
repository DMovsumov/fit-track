from typing import Optional


def calculate_water_goal(
    weight: float, activity_minutes: int, temperature: Optional[float] = None
) -> float:
    """
    Рассчет дневной нормы воды.

    Формула:
    - Базовая норма = вес × 30 мл/кг
    - +500 мл за каждые 30 минут активности
    - +500-1000 мл за жаркую погоду (>25°C)
    """
    base_water = weight * 30  # мл

    activity_water = (activity_minutes / 30) * 500

    weather_water = 0.0
    if temperature is not None:
        if temperature > 25:
            weather_water = min(1000, (temperature - 25) * 100)

    total_water = base_water + activity_water + weather_water
    return round(total_water, 1)


def calculate_calorie_goal(
    weight: float,
    height: float,
    age: int,
    activity_minutes: int,
    goal: str = "поддержка",
) -> float:
    """
    Рассчет дневной нормы калорий с учётом цели.

    Формула Миффлина-Сан Жеора (базовая):
    BMR = 10 × вес (кг) + 6.25 × рост (см) - 5 × возраст

    Затем добавляем калории за активность:
    - 200-400 ккал в зависимости от времени активности

    Цели:
    - "похудение": дефицит 15% от базовой нормы (примерно 300-500 ккал)
    - "массонабор": профицит 15% от базовой нормы (примерно 300-500 ккал)
    - "поддержка": базовая норма без изменений

    UPD: можно найти вариант с учетом пола и уровня активности
    """
    bmr = 10 * weight + 6.25 * height - 5 * age

    activity_calories = activity_minutes * 6
    maintenance_calories = bmr * 1.2

    total_calories = maintenance_calories + activity_calories

    goal_lower = goal.lower()
    if goal_lower == "похудение":
        total_calories = total_calories * 0.85
    elif goal_lower == "массонабор":
        total_calories = total_calories * 1.15

    return round(total_calories, 1)


def calculate_workout_calories(workout_type: str, minutes: int, weight: float) -> float:
    # МЕТ (Metabolic Equivalent of Task) - метаболический эквивалент задачи
    # Количество калорий на кг веса в час
    met_values = {
        "бег": 9.8,
        "бег трусцой": 7.0,
        "ходьба": 3.5,
        "быстрая ходьба": 5.0,
        "плавание": 6.0,
        "велосипед": 7.5,
        "силовая": 6.0,
        "йога": 3.0,
        "пилатес": 3.0,
        "аэробика": 7.0,
        "танцы": 4.8,
        "футбол": 7.0,
        "баскетбол": 8.0,
        "теннис": 7.0,
    }

    workout_lower = workout_type.lower()
    met = met_values.get(workout_lower, 5.0)

    # Формула: калории = MET × вес (кг) × время (часы)
    hours = minutes / 60
    calories = met * weight * hours

    return round(calories, 1)


def calculate_workout_water(minutes: int) -> float:
    return (minutes / 30) * 200
