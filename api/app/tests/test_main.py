from fastapi.testclient import TestClient

from ..config import settings
from ..main import app

client = TestClient(app)


def test_home():
    response = client.get("/", headers={"X-API-Key": settings.api_key})
    assert response.status_code == 200
    assert response.json() == {
        "message": "This is the API for the property price prediction model."
    }


def test_health():
    response = client.get("/health", headers={"X-API-Key": settings.api_key})
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_wrong_api_key():
    response = client.post(
        "/predict",
        json={
            "type": "casa",
            "sector": "la reina",
            "net_usable_area": 100,
            "net_area": 120,
            "n_rooms": 3,
            "n_bathroom": 2,
            "latitude": -33.45,
            "longitude": -70.6,
        },
        headers={"X-API-Key": "wrong-api-key"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid API Key"}
