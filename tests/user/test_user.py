from fastapi.testclient import TestClient
from src.utils.exeption import PasswordNotMatchError, NotUserExistException, AlreadyExistUserError
from app.main import app
from jwt import ExpiredSignatureError, InvalidTokenError

client = TestClient(app)


def test_create_user(mocker):
    mocker.patch(
        "src.cruds.users.create_user", return_value={"id": 1, "email": "user@example.com", "name": "test_user"}
    )
    response = client.post(
        "/api/users/", json={"password": "password", "email": "user@example.com", "name": "test_user"}
    )
    assert response.status_code == 200


def test_create_user_exeptions(mocker):
    mocker.patch("src.cruds.users.create_user", side_effect=[AlreadyExistUserError])
    response = client.post(
        "/api/users/", json={"password": "password", "email": "user@example.com", "name": "test_user"}
    )
    assert response.status_code == 409


def test_not_authenticated_get_user(mocker):
    mocker.patch(
        "src.cruds.users.get_one_member",
        return_value={"id": 1, "email": "user@example.com", "name": "test_user"},
    )
    response = client.get("/api/users/1")
    assert response.status_code == 403
