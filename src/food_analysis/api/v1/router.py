from fastapi import APIRouter
from .ingredients import router as ingredients_router
from .recipes import router as recipes_router
from .audio import router as audio_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(ingredients_router)
api_v1_router.include_router(recipes_router)
api_v1_router.include_router(audio_router)
