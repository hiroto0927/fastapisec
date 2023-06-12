from fastapi.testclient import TestClient
from src.utils.exeption import PasswordNotMatchError, NotUserExistException
from app.main import app
from src.schemas.auth import Create
from src.models.user import User

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


def test_create_token_exeptions(mocker):
    mocker.patch("src.cruds.auth.create_token_by_email", side_effect=[PasswordNotMatchError, NotUserExistException])

    response = client.post("/api/auth/token", json={"password": "pASSword", "email": "user@example.com"})
    assert response.status_code == 401

    response = client.post("/api/auth/token", json={"password": "password", "email": "non-user@example.com"})
    assert response.status_code == 404


def test_republish_token(mocker):
    mocker.patch(
        "src.cruds.auth.token_republish_by_refresh_token",
        return_value={"access_token": "access_token", "refresh_token": "refresh_token"},
    )
    response = client.post("/api/auth/refresh-token", json={"refresh_token": "refresh_token"})
    assert response.status_code == 200
