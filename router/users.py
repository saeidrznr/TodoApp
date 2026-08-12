from typing import Annotated

from fastapi import Depends, HTTPException, Path, APIRouter
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from .auth import get_current_user

from models import Users
from database import SessionLocal


class UserVerificationRequest(BaseModel):
    password: str
    new_password: str = Field(min_length= 6)
router = APIRouter(prefix="/users", tags=["users"])


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency , db: db_dependency):
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user_model


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency , db: db_dependency, userVerificaitonRequest: UserVerificationRequest):
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not bcrypt_context.verify(userVerificaitonRequest.password, user_model.hashed_password):
        raise HTTPException(status_code=401 , detail="Change Password Error")

    user_model.hashed_password = bcrypt_context.hash(userVerificaitonRequest.new_password)
    db.add(user_model)
    db.commit()


@router.put("/phonenumber/{phonenumber}", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency , db: db_dependency,phonenumber: str):
        user_model = db.query(Users).filter(Users.id == user.get('id')).first()
        if user_model is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        user_model.phone_number = phonenumber
        db.add(user_model)
        db.commit()

