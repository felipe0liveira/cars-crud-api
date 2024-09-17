from fastapi import APIRouter

from .cars import router as cars_router

v1_router = APIRouter()
v1_router.include_router(cars_router, prefix="/cars")
