from sqlalchemy.orm import Session
from ..database.database import get_db
from ..crud.crud import Crud
from ..schemas.schemas import UserCreateSchema, SignupResponse
from fastapi import (APIRouter, Depends,
                     HTTPException, status)
from decouple import config
from ..auth import authentication
from ..email.sendEmail import email
from datetime import timedelta


CONFIRMATION_TOKEN_EXPIRE_MINUSTES = int(config(
    "CONFIRMATION_TOKEN_EXPIRE_MINUSTES"))
router = APIRouter()
auth = authentication.Authentication()


@router.post("/signup/", tags=["register"], response_model=SignupResponse)
def signup(user: UserCreateSchema, db: Session = Depends(get_db)):
    if Crud.get_user_by_email(db=db, email=user.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already had an account with the email.",
            headers={"WWW-Authenticate": "Bearer"})
    elif Crud.get_user_by_username(db=db, username=user.username):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Choose a different username.",
            headers={"WWW-Authenticate": "Bearer"})
    else:
        Crud.create_user(db=db, UserCreateSchema=user,
                         hashed_password=auth.get_password_hash(user.password))
        public_id = Crud.get_user_by_username(db, user.username).public_id
        confirmation_token_expires = timedelta(
            minutes=CONFIRMATION_TOKEN_EXPIRE_MINUSTES)
        confirmation_token = auth.create_access_token(
            data={"sub": public_id}, expires_delta=confirmation_token_expires
        )
        email.confirmationMail(
            to=user.email, body=confirmation_token, userName=user.username)
        raise HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail="Please Confirm your mail with the token was sent by mail.",
            headers={"WWW-Authenticate": "Bearer"})
