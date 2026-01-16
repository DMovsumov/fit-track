from datetime import date, timedelta

"""
Хранилище данных пользователей в памяти.
Структура данных:
{
    "user_id": {
        "weight": float,  # вес в кг
        "height": float,  # рост в см
        "age": int,  # возраст
        "activity_minutes": int,  # минуты активности в день
        "city": str,  # город
        "goal": str,  # цель: "похудение", "массонабор", "поддержка"
        "water_goal": float,  # норма воды в мл
        "calorie_goal": float,  # норма калорий
        "logged_water": float,  # выпито воды за день в мл
        "logged_calories": float,  # потреблено калорий за день
        "burned_calories": float,  # сожжено калорий за день
        "daily_logs": {  # логи за каждый день
            "YYYY-MM-DD": {
                "water": float,
                "calories": float,
                "burned_calories": float,
                "foods": list,  # список съеденных продуктов
                "workouts": list  # список тренировок
            }
        }
    }
}
"""

storage = {}


def get_user(user_id: int | None) -> dict:
    if user_id not in storage:
        storage[user_id] = {
            "weight": None,
            "height": None,
            "age": None,
            "activity_minutes": None,
            "city": None,
            "goal": None,
            "water_goal": None,
            "calorie_goal": None,
            "daily_logs": {},
        }

    return storage[user_id]


def get_today_log(user_id: int) -> dict:
    user = get_user(user_id)
    today = date.today().isoformat()

    if today not in user["daily_logs"]:
        user["daily_logs"][today] = {
            "water": 0.0,
            "calories": 0.0,
            "burned_calories": 0.0,
            "foods": [],
            "workouts": [],
        }
    return user["daily_logs"][today]


def reset_daily_logs(user_id: int):
    user = get_user(user_id)
    today = date.today().isoformat()

    user["daily_logs"][today] = {
        "water": 0.0,
        "calories": 0.0,
        "burned_calories": 0.0,
        "foods": [],
        "workouts": [],
    }


def get_daily_logs(user_id: int, days: int = 7):
    user = get_user(user_id)

    if not user.get("daily_logs"):
        return None

    today = date.today()

    dates = []
    water_data = []
    calories_data = []
    burned_calories_data = []

    for i in range(days - 1, -1, -1):
        check_date = today - timedelta(days=i)
        date_str = check_date.isoformat()

        dates.append(check_date)

        if date_str in user["daily_logs"]:
            log = user["daily_logs"][date_str]
            water_data.append(log.get("water", 0))
            calories_data.append(log.get("calories", 0))
            burned_calories_data.append(log.get("burned_calories", 0))
        else:
            water_data.append(0)
            calories_data.append(0)
            burned_calories_data.append(0)

    return dates, water_data, calories_data, burned_calories_data
