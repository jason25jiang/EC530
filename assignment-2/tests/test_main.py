from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users/?user_id=1&name=John")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "John"}

def test_get_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "John"}

def test_create_device():
    client.post("/users/?user_id=1&name=John")
    client.post("/houses/?house_id=1&name=MyHome&owner_id=1")
    client.post("/rooms/?room_id=1&name=Living Room&house_id=1")
    response = client.post("/devices/?device_id=1&name=Light&type=Smart Light&room_id=1")
    assert response.status_code == 200
    assert response.json()["name"] == "Light"
