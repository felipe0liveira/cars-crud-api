import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
from uuid import uuid4, UUID
from main import app
from core.database import get_db


@pytest.mark.asyncio
async def test_get_cars():
    cars_data = [
        {
            "id": str(uuid4()),
            "make": "Test Car 1",
            "model": "Sedan",
            "year": 2023
        },
        {
            "id": str(uuid4()),
            "make": "Test Car 2",
            "model": "SUV",
            "year": 2024
        }]

    with patch("app.controllers.cars.get_cars", return_value=cars_data) as mock_cars_data:

        mock_db_session = AsyncMock(spec=AsyncSession)

        async def mock_get_db_override():
            yield mock_db_session

        app.dependency_overrides[get_db] = mock_get_db_override

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/v1/cars/")

        assert response.status_code == 200
        response_data = response.json()

        assert len(response_data) == 2
        assert "id" in response_data[0]
        assert "id" in response_data[1]

        mock_cars_data.assert_called_once()
        app.dependency_overrides = {}


@pytest.mark.asyncio
async def test_get_one_car():
    car_id = str(uuid4())
    car_data = {
        "id": car_id,
        "make": "Test Car 1",
        "model": "Sedan",
        "year": 2023
    }

    with patch("app.controllers.cars.get_car", return_value=car_data) as mock_car_data:

        mock_db_session = AsyncMock(spec=AsyncSession)

        async def mock_get_db_override():
            yield mock_db_session

        app.dependency_overrides[get_db] = mock_get_db_override

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(f"/v1/cars/{car_id}")

        assert response.status_code == 200
        response_data = response.json()

        assert response_data == car_data

        mock_car_data.assert_called_once()
        mock_car_data.assert_called_once_with(mock_db_session, UUID(car_id))
        app.dependency_overrides = {}


@pytest.mark.asyncio
async def test_get_one_car_invalid_id():
    with patch("app.controllers.cars.get_car"):

        mock_db_session = AsyncMock(spec=AsyncSession)

        async def mock_get_db_override():
            yield mock_db_session

        app.dependency_overrides[get_db] = mock_get_db_override

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(f"/v1/cars/1234")

        assert response.status_code == 422
        response_data = response.json()

        assert response_data["detail"][0]["type"] == "uuid_parsing"
        assert ".".join(response_data["detail"][0]["loc"]) == "path.id"

        app.dependency_overrides = {}


@pytest.mark.asyncio
async def test_get_one_car_not_found():

    car_id = str(uuid4())
    with patch("app.controllers.cars.get_car", return_value=None) as mock_car_data:

        mock_db_session = AsyncMock(spec=AsyncSession)

        async def mock_get_db_override():
            yield mock_db_session

        app.dependency_overrides[get_db] = mock_get_db_override

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(f"/v1/cars/{car_id}")

        assert response.status_code == 404
        response_data = response.json()

        assert response_data["detail"] == "Car not found"

        mock_car_data.assert_called_once()
        mock_car_data.assert_called_once_with(mock_db_session, UUID(car_id))
        app.dependency_overrides = {}
