# Todo App

A simple Todo application built with **FastAPI** as a learning project.

🔗 **Live Demo:** https://todoapp-xyuf.onrender.com/

## Features

* User registration and login
* JWT authentication
* Create, read, update, and delete Todos
* SQLite database
* SQLAlchemy ORM
* Alembic migrations
* Basic API testing with Pytest

## Tech Stack

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* JWT
* Pytest
* HTML / CSS / JavaScript

## Run Locally

```bash
git clone "https://github.com/saeidrznr/TodoApp"
cd TodoApp

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

uvicorn main:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## Purpose

This project was built to learn and practice **FastAPI, authentication, databases, SQLAlchemy, and testing**.
