from fastapi.testclient import TestClient
from src.utils.exeption import PasswordNotMatchError, NotUserExistException
from app.main import app
from jwt import ExpiredSignatureError, InvalidTokenError

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


def test_republish_token_exeptions(mocker):
    mocker.patch(
        "src.cruds.auth.token_republish_by_refresh_token", side_effect=[ExpiredSignatureError, InvalidTokenError]
    )

    response = client.post("/api/auth/refresh-token", json={"refresh_token": "refresh_token"})
    assert response.status_code == 401

    response = client.post("/api/auth/refresh-token", json={"refresh_token": "refresh_token"})
    assert response.status_code == 401


def test_delete_refresh_token(mocker):
    mocker.patch("src.cruds.auth.delete_refresh_token_by_email", return_value=None)
    response = client.request("DELETE", "/api/auth/refresh-token", json={"email": "user@example.com"})
    assert response.status_code == 200


def test_delete_refresh_token_exeptions(mocker):
    mocker.patch("src.cruds.auth.delete_refresh_token_by_email", side_effect=[NotUserExistException, InvalidTokenError])
    response = client.request("DELETE", "/api/auth/refresh-token", json={"email": "non-user@example.com"})
    assert response.status_code == 404

    response = client.request("DELETE", "/api/auth/refresh-token", json={"email": "user@example.com"})
    assert response.status_code == 401
