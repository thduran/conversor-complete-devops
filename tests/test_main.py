from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_celsius_to_fahrenheit():
    response = client.get("/convert/celsius-to-fahrenheit?c=0")
    data = response.json()
    assert response.status_code == 200
    assert data["fahrenheit"] == 32

def test_kilometers_to_miles():
    response = client.get("/convert/kilometers-to-miles?km=1")
    data = response.json()
    assert response.status_code == 200
    assert abs(data["miles"] - 0.621371) < 0.0001