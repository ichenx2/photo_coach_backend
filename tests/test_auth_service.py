import pytest
from fastapi import HTTPException
from app.services.auth_service import register_user, authenticate_user, get_current_user
from app.schemas.user_schema import UserCreate
from unittest.mock import MagicMock
from fastapi.security import HTTPAuthorizationCredentials

def mock_get_user_by_username(db, username):
    return None

def mock_create_user(db, username, email, password):
    return MagicMock(username=username, email=email, password=password)

def mock_create_access_token(data):
    return "mocked_token"

def mock_get_user_by_email(db, email):
    if email == "existing_user@example.com":
        return MagicMock(username="existing_user", email=email, hashed_password="hashed_password")
    return None

def mock_verify_password(plain_password, hashed_password):
    return plain_password == "correct_password" and hashed_password == "hashed_password"

def mock_verify_token(token):
    if token == "valid_token":
        return {"sub": 1}
    return None

def mock_get_user_by_id(db, user_id):
    if user_id == 1:
        return MagicMock(username="existing_user")
    return None


# Fixtures for common mocks
@pytest.fixture
def user():
    return UserCreate(username="new_user", email="new_user@example.com", password="correct_password")

@pytest.fixture
def mock_dependencies(monkeypatch):
    monkeypatch.setattr("app.services.auth_service.get_user_by_username", mock_get_user_by_username)
    monkeypatch.setattr("app.services.auth_service.create_user", mock_create_user)
    monkeypatch.setattr("app.services.auth_service.create_access_token", mock_create_access_token)
    monkeypatch.setattr("app.services.auth_service.get_user_by_email", mock_get_user_by_email)
    monkeypatch.setattr("app.services.auth_service.verify_password", mock_verify_password)
    monkeypatch.setattr("app.services.auth_service.verify_token", mock_verify_token)
    monkeypatch.setattr("app.services.auth_service.get_user_by_id", mock_get_user_by_id)

# Tests
def test_register_user(user, mock_dependencies):
    token = register_user(user)
    assert token == "mocked_token"

def test_authenticate_user(mock_dependencies):
    user = UserCreate(username="existing_user", email="existing_user@example.com", password="correct_password")
    token = authenticate_user(user)
    assert token == "mocked_token"

def test_authenticate_user_invalid_password(mock_dependencies):
    user = UserCreate(username="existing_user", email="existing_user@example.com", password="wrong_password")
    token = authenticate_user(user)
    assert token is None

def test_authenticate_user_not_found(mock_dependencies):
    user = UserCreate(username="nonexistent_user", email="nonexistent_user@example.com", password="correct_password")
    token = authenticate_user(user)
    assert token is None

def test_get_current_user(mock_dependencies):
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="valid_token")
    user = get_current_user(credentials)
    assert user.username == "existing_user"

def test_get_current_user_invalid_token(mock_dependencies):
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="invalid_token")
    with pytest.raises(HTTPException) as excinfo:
        get_current_user(credentials)
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Invalid token"
