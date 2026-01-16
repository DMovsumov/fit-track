from .food import router as food_router
from .progress import router as progress_router
from .start import router as start_router
from .user import router as user_router
from .water import router as water_router
from .workout import router as workout_router

__all__ = [
    "food_router",
    "progress_router",
    "start_router",
    "user_router",
    "water_router",
    "workout_router",
]
