from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_token(mocker):
    mocker.patch("src.cruds.auth.create_token_by_email", return_value={"access_token": "test", "refresh_token": "test"})
    response = client.post("/api/auth/token", json={"password": "password", "email": "user@example.com"})
    assert response.status_code == 200

    response = client.post("/api/auth/token", json={"password": "passwor", "email": "user@example.com"})
    assert response.status_code == 422

    response = client.post("/api/auth/token", json={"password": "password", "email": "user@example"})
    assert response.status_code == 422

    response = client.post("/api/auth/token", json={"password": "p@sswOrd", "email": "user@example.com"})
    assert response.status_code == 200


# def test_create_token(mocker):
#     user = mocker.patch(
#         "src.cruds.auth.user",
#         return_value={
#             {"id": 1, "name": "test_user", "email": "user@example.com", "hashedpass": "test", "salt": "test"}
#         },
#     )
#     access_token = mocker.patch("src.libs.jwt.create_access_token", return_value="test")
#     refresh_token = mocker.patch("src.libs.jwt.create_refresh_token", return_value="test")
