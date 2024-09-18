from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.cars import CarCreate, CarUpdate
from app.models.cars import Car
from uuid import UUID


async def get_cars(db: AsyncSession):
    result = await db.execute(select(Car))
    return result.scalars().all()


async def get_car(db: AsyncSession, car_id: UUID):
    return await db.get(Car, car_id)


async def create_car(db: AsyncSession, car: CarCreate):
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
        for key, value in car_update.model_dump().items():
            setattr(db_car, key, value)
        await db.commit()
        await db.refresh(db_car)
        return db_car
    return None