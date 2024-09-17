from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import cars as schema
from app.controllers import cars as controller
from core.database import get_db

from uuid import UUID



router = APIRouter()


@router.post("/", response_model=schema.Car, status_code=status.HTTP_201_CREATED)
async def create_car(car: schema.CarCreate, db: AsyncSession = Depends(get_db)):
    return await controller.create_car(db, car)


@router.get("/", response_model=list[schema.Car], status_code=status.HTTP_200_OK)
async def read_cars(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    cars = await controller.get_cars(db)
    return cars


@router.get("/{id}", response_model=schema.Car, status_code=status.HTTP_200_OK)
async def read_car(id: UUID, db: AsyncSession = Depends(get_db)):
    car = await controller.get_car(db, id)
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return car


@router.delete("/{id}", response_model=schema.Car, status_code=status.HTTP_200_OK)
async def delete_car(id: UUID, db: AsyncSession = Depends(get_db)):
    car = await controller.delete_car(db, id)
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return car
