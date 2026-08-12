from sqlalchemy import create_engine, StaticPool, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from ..main import app
import pytest
from ..models import Todos, Users
from ..database import Base
from ..router.users import bcrypt_context

SQLALCHEMY_DATABASE_URI = 'sqlite:///./testdb.db'

engine = create_engine(SQLALCHEMY_DATABASE_URI,
                       connect_args={"check_same_thread": False},
                       poolclass=StaticPool
                       )

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(engine)

client = TestClient(app)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {'username': 'saeid', 'id': 1, 'role': 'admin'}


@pytest.fixture
def test_todo():
    todo = Todos(title="Start to coding!",
                 description="This is a description",
                 complete=False,
                 priority=5, owner_id=1)
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM TODOS;"))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(username="saeid", first_name="Saeid", last_name="Rezaei", email="a@gmail.com",
                 hashed_password=bcrypt_context.hash("test1234!"), is_active=True,
                 phone_number="09126578425", role="admin")
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM USERS;"))
        connection.commit()
