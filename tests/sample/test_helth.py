from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_helth_check():
    response = client.get("/health-check")

    assert response.status_code == 200
    assert response.json() == {"msg": "hello"}
