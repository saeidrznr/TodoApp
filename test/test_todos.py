from ..router.todos import get_db, get_current_user
from .utils import *
from starlette import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_authenticated(test_todo):
    response = client.get("/todos/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"title": "Start to coding!",
                                "description": "This is a description",
                                "complete": False,
                                "priority": 5,
                                "owner_id": 1,
                                "id": 1}]


def test_read_one_authenticated(test_todo):
    response = client.get("/todos/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"title": "Start to coding!",
                               "description": "This is a description",
                               "complete": False,
                               "priority": 5,
                               "owner_id": 1,
                               "id": 1}


def test_read_not_found_authenticated():
    response = client.get("/todos/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found."}


def test_add_authenticated(test_todo):
    request_data = {"title": "New title",
                    "description": "This is a new description",
                    "complete": False,
                    "priority": 5,
                    "owner_id": 1,
                    }
    response = client.post("/todos/todo/", json=request_data)

    assert response.status_code == status.HTTP_201_CREATED
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == "New title"
    assert model.description == "This is a new description"
    assert model.title == "New title"
    assert model.description == "This is a new description"
    assert model.complete == False
    assert model.priority == 5
    assert model.owner_id == 1


def test_update_todo(test_todo):
    request_data = {"title": "title changed", "description": "This is a description", "complete": False,
                    "priority": 5, "owner_id": 1}
    response = client.put("/todos/todo/1", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == "title changed"


def test_update_todo_not_found(test_todo):
    request_data = {"title": "title changed", "description": "This is a description", "complete": False,
                    "priority": 5, "owner_id": 1}
    response = client.put("/todos/todo/99", json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found."}


def test_delete_todo(test_todo):
    response = client.delete("/todos/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_delete_todo_not_found(test_todo):
    response = client.delete("/todos/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found."}
