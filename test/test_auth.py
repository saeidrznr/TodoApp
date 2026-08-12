from fastapi import HTTPException
from starlette import status

from .utils import *
from ..router.auth import (get_db, authenticate_user, create_access_token,
                           ALGORITHM, SECRET_KEY, get_current_user)
from datetime import timedelta
from jose import jwt
import pytest

app.dependency_overrides[get_db] = get_db


def test_authenticate_user(test_user):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(test_user.username, "test1234!", db)
    assert authenticated_user is not None

    none_exist_authenticated_user = authenticate_user("Unknown_user", "test1234!", db)
    assert none_exist_authenticated_user is False

    wrong_password_user = authenticate_user(test_user.username, "wrong_pass", db)
    assert wrong_password_user is False


def test_create_access_token():
    username = "test_user"
    user_id = 1
    role = "user"
    delta_time = timedelta(days=1)
    token = create_access_token(username, user_id, role, delta_time)

    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_format": False})
    assert decoded_token["sub"] == username
    assert decoded_token["id"] == user_id
    assert decoded_token["role"] == role


@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    username = "test_user"
    user_id = 1
    role = "user"
    token = jwt.encode({"sub": username, "id": user_id, 'role': role}, SECRET_KEY, algorithm=ALGORITHM)
    user = await get_current_user(token)
    assert user == {'username': username, 'id': user_id, 'role': role}



@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    encode = {"role": "user"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as exinfo:
        await get_current_user(token)

    assert exinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exinfo.value.detail == "Could not validate user"
