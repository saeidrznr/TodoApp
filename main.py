from fastapi import FastAPI
from starlette import status

from database import engine
from models import Base
from router import auth, todos, admin, users
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory="TodoApp/templates")

app = FastAPI()

app.mount('/static', StaticFiles(directory="static"), name='static')


@app.get("/")
def test():
    return RedirectResponse("/todos/todo-page", status_code=status.HTTP_302_FOUND)


@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}


Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
