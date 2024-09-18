from datetime import datetime
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.cars import CarCreate, CarUpdate
from app.models.cars import Car
from uuid import UUID
from .exceptions import InvalidCarYearException


def is_car_year_invalid(year):
    current_year = datetime.now().year
    if year < 1886 or year > (current_year + 1):
        return True
    return False


async def get_cars(db: AsyncSession):
    result = await db.execute(select(Car))
    return result.scalars().all()


async def get_car(db: AsyncSession, car_id: UUID):
    return await db.get(Car, car_id)


async def create_car(db: AsyncSession, car: CarCreate):
    if is_car_year_invalid(car.year):
        raise InvalidCarYearException(car.year)

    db_car = Car(**car.model_dump())
    db.add(db_car)
    await db.commit()
    await db.refresh(db_car)
    return db_car


async def delete_car(db: AsyncSession, car_id: int):
    db_car = await get_car(db, car_id)
    if db_car:
        await db.delete(db_car)
        await db.commit()
    return db_car


async def update_car(db: AsyncSession, car_id: UUID, car_update: CarUpdate):
    db_car = await get_car(db, car_id)

    if db_car:
        if is_car_year_invalid(car_update.year):
            raise InvalidCarYearException(car_update.year)

        for key, value in car_update.model_dump().items():
            setattr(db_car, key, value)

        await db.commit()
        await db.refresh(db_car)
        return db_car

    return None
