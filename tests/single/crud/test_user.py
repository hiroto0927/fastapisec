from unittest.mock import MagicMock
import pytest
from src.cruds.users import get_one_member
from src.models.user import User
from src.utils.exeption import NotUserExistException


def test_get_one_member_exists():
    user_id = 1
    mock_user = User(id=user_id, name="Test User", email="user@example.com", salt="salt", hashedpass="hashedpass")

    def mock_query_first():
        return mock_user

    mock_session = MagicMock()
    mock_session.query().filter().first = mock_query_first

    result = get_one_member(user_id, mock_session)

    assert result.id == user_id
    assert result.name == "Test User"
    assert result.email == "user@example.com"
    assert result.salt == "salt"
    assert result.hashedpass == "hashedpass"


def test_get_one_member_not_exists():
    user_id = 1

    def mock_query_first():
        return None

    mock_session = MagicMock()
    mock_session.query().filter().first = mock_query_first

    with pytest.raises(NotUserExistException):
        get_one_member(user_id, mock_session)
