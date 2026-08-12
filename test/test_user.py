from starlette import status

from .utils import *
from ..router.users import get_db, get_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_user] = override_get_current_user

def test_get_user(test_user):
    response = client.get("/users/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'saeid'
    assert response.json()['first_name'] == 'Saeid'
    assert response.json()['last_name'] == 'Rezaei'
    assert response.json()['email'] == 'a@gmail.com'
    assert response.json()['is_active'] == True
    assert response.json()['phone_number'] == '09126578425'
    assert response.json()['role'] == 'admin'


def test_change_password_success(test_user):
    response = client.put("/users/password",json={"password":"test1234!", "new_password":"new_password!"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_failure(test_user):
    response = client.put("/users/password",json={"password":"invalid_pass", "new_password":"new_password!"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_change_phone_number(test_user):
    response = client.put("/users/phonenumber/09189236952")
    assert response.status_code == status.HTTP_204_NO_CONTENT