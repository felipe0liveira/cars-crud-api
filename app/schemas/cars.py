from pydantic import BaseModel
from uuid import UUID


class CarBase(BaseModel):
    make: str
    model: str
    year: int


class CarCreate(CarBase):
    pass


class Car(CarBase):
    id: UUID

    class Config:
        orm_mode = True
