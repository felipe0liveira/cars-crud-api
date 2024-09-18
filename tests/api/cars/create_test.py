import pytest
from datetime import datetime
from fastapi import HTTPException
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient
from uuid import uuid4

from main import app
from app.schemas.cars import CarCreate, Car
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db


@pytest.mark.asyncio
async def test_create_car():

    car_data = {"make": "Test Car", "model": "Sedan", "year": 2023}
    created_car = Car(id=uuid4(), **car_data)

    with patch("app.controllers.cars.create_car", return_value=created_car) as mock_create_car:

        mock_db_session = AsyncMock(spec=AsyncSession)

        async def mock_get_db_override():
            yield mock_db_session

        app.dependency_overrides[get_db] = mock_get_db_override

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/v1/cars/", json=car_data)

        assert response.status_code == 201
        response_data = response.json()

        assert response_data["make"] == "Test Car"
        assert response_data["model"] == "Sedan"
        assert response_data["year"] == 2023
        assert "id" in response_data

        mock_create_car.assert_called_once()
        mock_create_car.assert_called_with(
            mock_db_session, CarCreate(**car_data))
        app.dependency_overrides = {}


@pytest.mark.asyncio
async def test_create_car_invalid_future_year():
    future_year = datetime.now().year + 2
    car_data = {"make": "Test Car", "model": "Sedan", "year": future_year}

    with patch("app.controllers.cars.create_car", side_effect=HTTPException(status_code=400, detail=f"Car year cannot be {future_year}")):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/v1/cars/", json=car_data)

        assert response.status_code == 400
        assert response.json() == {
            "detail": f"Car year cannot be {future_year}"}


@pytest.mark.asyncio
async def test_create_car_invalid_past_year():
    past_year = 1885
    car_data = {"make": "Test Car", "model": "Sedan", "year": past_year}

    with patch("app.controllers.cars.create_car", side_effect=HTTPException(status_code=400, detail=f"Car year cannot be {past_year}")):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/v1/cars/", json=car_data)

        assert response.status_code == 400
        assert response.json() == {
            "detail": f"Car year cannot be {past_year}"}


@pytest.mark.asyncio
async def test_create_car_duplicity():
    past_year = 1885
    car_data = {"make": "Test Car", "model": "Sedan", "year": past_year}

    with patch("app.controllers.cars.get_cars", return_value=[car_data]):
        with patch("app.controllers.cars.create_car", side_effect=HTTPException(status_code=409, detail=f"Car {car_data["make"]} {car_data["model"]} ({car_data["year"]}) already exists")):
            async with AsyncClient(app=app, base_url="http://test") as ac:
                response = await ac.post("/v1/cars/", json=car_data)

            assert response.status_code == 409
            assert response.json() == {
                "detail": f"Car {car_data["make"]} {car_data["model"]} ({car_data["year"]}) already exists"}
