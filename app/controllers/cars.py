from datetime import datetime
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_
from app.schemas.cars import CarCreate, CarUpdate
from app.models.cars import Car
from uuid import UUID
from .exceptions import InvalidCarYearException, ExistingCarException


def is_car_year_invalid(year):
    current_year = datetime.now().year
    if year < 1886 or year > (current_year + 1):
        return True
    return False


async def get_cars(db: AsyncSession, make: str = None, model: str = None, year: int = None):
    query = select(Car)

    filters = []
    if make:
        filters.append(Car.make == make)
    if model:
        filters.append(Car.model == model)
    if year:
        filters.append(Car.year == year)

    if filters:
        query = query.where(and_(*filters))

    result = await db.execute(query)
    return result.scalars().all()


async def get_car(db: AsyncSession, car_id: UUID):
    return await db.get(Car, car_id)


async def create_car(db: AsyncSession, car: CarCreate):
    if is_car_year_invalid(car.year):
        raise InvalidCarYearException(car.year)
    
    found_cars = await get_cars(db, car.make, car.model, car.year)

    if len(found_cars) > 0:
        raise ExistingCarException(**car.model_dump())

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
        
        found_cars = await get_cars(db, car_update.make, car_update.model, car_update.year)

        if len(found_cars) > 0:
            raise ExistingCarException(**car_update.model_dump())

        for key, value in car_update.model_dump().items():
            setattr(db_car, key, value)

        await db.commit()
        await db.refresh(db_car)
        return db_car

    return None
