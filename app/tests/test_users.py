from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_user():
    init_data = "your_test_init_data"
    response = client.post("/api/v1/users/", json={"init_data": init_data})
    assert response.status_code == 200
    assert "data" in response.json()
