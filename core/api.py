import asyncio
from typing import Optional

import aiohttp

from core.config import OPENWEATHER_API_KEY


async def get_temperature(city: str) -> Optional[float]:
    if not OPENWEATHER_API_KEY:
        print("Предупреждение: OPENWEATHER_API_KEY не установлен")
        return None

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["main"]["temp"]
                else:
                    print(f"Ошибка получения погоды: {response.status}")
                    return None
    except Exception as e:
        print(f"Ошибка при запросе погоды: {e}")
        return None


async def get_food_info(product_name: str) -> Optional[dict]:
    try:
        url = f"https://world.openfoodfacts.org/cgi/search.pl?action=process&search_terms={product_name}&json=true"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    products = data.get("products", [])

                    if products:
                        first_product = products[0]
                        return {
                            "name": first_product.get("product_name", "Неизвестно"),
                            "calories_per_100g": first_product.get(
                                "nutriments", {}
                            ).get("energy-kcal_100g", 0),
                        }
                    return None
    except asyncio.TimeoutError:
        print(f"Таймаут при запросе OpenFoodFacts для '{product_name}'")
    except Exception as e:
        print(f"Ошибка при запросе OpenFoodFacts: {e}")

    return None
