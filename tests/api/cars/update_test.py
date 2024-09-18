import pytest
from datetime import datetime
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient
from uuid import uuid4

from main import app
from app.schemas.cars import CarUpdate, Car
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db


@pytest.mark.asyncio
async def test_update_car():
    car_id = uuid4()
    car_update_data = {"make": "Updated Make", "model": "SUV", "year": 2023}
    updated_car = Car(id=car_id, **car_update_data)

    with patch("app.controllers.cars.get_car", return_value=updated_car) as mock_get_car:
        mock_db_session = AsyncMock(spec=AsyncSession)

        async def mock_get_db_override():
            yield mock_db_session

        app.dependency_overrides[get_db] = mock_get_db_override

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.put(f"/v1/cars/{car_id}", json=car_update_data)

        assert response.status_code == 200
        response_data = response.json()

        assert response_data["make"] == "Updated Make"
        assert response_data["model"] == "SUV"
        assert response_data["year"] == 2023

        mock_get_car.assert_called_once_with(mock_db_session, car_id)

        app.dependency_overrides = {}


@pytest.mark.asyncio
async def test_car_invalid_future_year():
    car_id = uuid4()
    car_year = 2027
    car_update_data = {"make": "Updated Make",
                       "model": "SUV", "year": car_year}
    updated_car = Car(id=car_id, **car_update_data)

    with patch("app.controllers.cars.get_car", return_value=updated_car) as mock_get_car:
        mock_db_session = AsyncMock(spec=AsyncSession)

        async def mock_get_db_override():
            yield mock_db_session

        app.dependency_overrides[get_db] = mock_get_db_override

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.put(f"/v1/cars/{car_id}", json=car_update_data)

        assert response.status_code == 400
        assert response.json() == {
            "detail": f"Car year cannot be {car_year}"}

        mock_get_car.assert_called_once_with(mock_db_session, car_id)

        app.dependency_overrides = {}


@pytest.mark.asyncio
async def test_car_invalid_past_year():
    car_id = uuid4()
    car_year = 1885
    car_update_data = {"make": "Updated Make",
                       "model": "SUV", "year": car_year}
    updated_car = Car(id=car_id, **car_update_data)

    with patch("app.controllers.cars.get_car", return_value=updated_car) as mock_get_car:
        mock_db_session = AsyncMock(spec=AsyncSession)

        async def mock_get_db_override():
            yield mock_db_session

        app.dependency_overrides[get_db] = mock_get_db_override

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.put(f"/v1/cars/{car_id}", json=car_update_data)

        assert response.status_code == 400
        assert response.json() == {
            "detail": f"Car year cannot be {car_year}"}

        mock_get_car.assert_called_once_with(mock_db_session, car_id)

        app.dependency_overrides = {}
