import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
from uuid import uuid4, UUID
from main import app
from core.database import get_db


@pytest.mark.asyncio
async def test_delete_car():
    car_id = str(uuid4())
    car_data = {
        "id": car_id,
        "make": "Test Car 1",
        "model": "Sedan",
        "year": 2023
    }

    with patch("app.controllers.cars.delete_car", return_value=car_data) as mock_car_data:

        mock_db_session = AsyncMock(spec=AsyncSession)

        async def mock_get_db_override():
            yield mock_db_session

        app.dependency_overrides[get_db] = mock_get_db_override

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.delete(f"/v1/cars/{car_id}")

        assert response.status_code == 200
        response_data = response.json()

        assert response_data == car_data

        mock_car_data.assert_called_once()
        mock_car_data.assert_called_once_with(mock_db_session, UUID(car_id))
        app.dependency_overrides = {}


@pytest.mark.asyncio
async def test_delete_car_not_found():
    car_id = str(uuid4())

    with patch("app.controllers.cars.delete_car", return_value=None) as mock_car_data:

        mock_db_session = AsyncMock(spec=AsyncSession)

        async def mock_get_db_override():
            yield mock_db_session

        app.dependency_overrides[get_db] = mock_get_db_override

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.delete(f"/v1/cars/{car_id}")

        assert response.status_code == 404
        response_data = response.json()

        assert response_data["detail"] == "Car not found"

        mock_car_data.assert_called_once()
        mock_car_data.assert_called_once_with(mock_db_session, UUID(car_id))
        app.dependency_overrides = {}
