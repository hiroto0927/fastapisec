from fastapi.testclient import TestClient
from src.libs.pwd import get_cuurent_user
from src.utils.exeption import NotUserExistException, AlreadyExistUserError
from app.main import app
from datetime import datetime
from datetime import timedelta

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


def mock_get_current_user():
    return {"sub": "test-user@example.com", "iat": datetime.utcnow(), "exp": datetime.utcnow() + timedelta(minutes=30)}


def test_authenticated_get_user(mocker):
    app.dependency_overrides[get_cuurent_user] = mock_get_current_user
    mocker.patch(
        "src.cruds.users.get_one_member", return_value={"id": 1, "email": "test-user@example.com", "name": "test_user"}
    )
    response = client.get("/api/users/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "email": "test-user@example.com", "name": "test_user"}


def test_get_user_exeptions(mocker):
    app.dependency_overrides[get_cuurent_user] = mock_get_current_user
    mocker.patch("src.cruds.users.get_one_member", side_effect=[NotUserExistException])
    response = client.get("/api/users/100")
    assert response.status_code == 404


def test_create_user(mocker):
    mocker.patch(
        "src.cruds.users.create_user",
        return_value={
            "id": 1,
            "name": "test_user",
            "email": "user@example.com",
            "salt": "salt",
            "hashedpass": "hashedpass",
        },
    )
    response = client.post("/api/users/", json={"name": "string", "password": "stringst", "email": "user@example.com"})
    assert response.status_code == 200


def test_create_user_exeptions(mocker):
    mocker.patch("src.cruds.users.create_user", side_effect=[AlreadyExistUserError])
    response = client.post("/api/users/", json={"name": "string", "password": "stringst", "email": "user@example.com"})
    assert response.status_code == 409
