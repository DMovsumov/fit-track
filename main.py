import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from core.config import TOKEN
from core.middlewares import LoggingMiddleware
from handlers import (
    food_router,
    progress_router,
    start_router,
    user_router,
    water_router,
    workout_router,
)


async def main():
    print("Bot is started")

    bot = Bot(token=TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_routers(
        start_router,
        user_router,
        water_router,
        food_router,
        progress_router,
        workout_router,
    )
    dp.message.middleware(LoggingMiddleware())

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
