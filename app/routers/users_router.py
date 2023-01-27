from sqlalchemy.orm import Session
from ..database.database import get_db
from ..crud.crud import Crud
from ..schemas.schemas import (UserCreateSchema, SignupResponse,
                               ConfirmationResponse, UserConfirm,
                               Token, UserUpdateSchema,
                               UpdateResponse, UserUpdateUsernameSchema,
                               ForgetPasswordResponse, ForgetPasswordForm,
                               ForgetPasswordTokenResponse, ForgetToken)
from fastapi import (APIRouter, Depends,
                     HTTPException, status)
from decouple import config
from ..auth import authentication
from ..email.sendEmail import email
from datetime import timedelta
from fastapi.security import (OAuth2PasswordRequestForm)
from ..models.users import Users


CONFIRMATION_TOKEN_EXPIRE_MINUSTES = int(config(
    "CONFIRMATION_TOKEN_EXPIRE_MINUSTES"))
router = APIRouter()
auth = authentication.Authentication()


@router.post("/signup/", tags=["signup"], response_model=SignupResponse)
def signup(user: UserCreateSchema,
           db: Session = Depends(get_db)):
    print(user)
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


@router.post("/confirmation/", tags=["signup"],
             response_model=ConfirmationResponse)
def confirmation(user: UserConfirm, db: Session = Depends(get_db)):
    current_user = auth.get_confirmation(user.confirmationToken)
    user_ = Crud.get_user_by_public_id(db, current_user.public_id)
    if not user_.confirmed:
        Crud.confirm_account(db, current_user.public_id)
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED,
            detail=f"{user_.username}'s email {user_.email} is confirmed.",
            headers={"WWW-Authenticate": "Bearer"})
    else:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=f"{user_.username}'s email {user_.email}"
            " has already confirmed.",
            headers={"WWW-Authenticate": "Bearer"})


@router.post("/token/", tags=["login"], response_model=Token)
async def token(login_form: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(get_db)):
    user = Crud.get_user_by_username(db=db, username=login_form.username)
    user = auth.authenticate_user(user, login_form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"})
    else:
        access_token_expires = timedelta(
            minutes=CONFIRMATION_TOKEN_EXPIRE_MINUSTES)
        access_token_ = auth.create_access_token(
            data={"sub": user.public_id}, expires_delta=access_token_expires)
        return {"access_token": access_token_, "token_type": "bearer"}


@router.put("/update/user/information", tags=["update/user"],
            response_model=UpdateResponse)
async def update_user_detail(payload: UserUpdateSchema,
                             db: Session = Depends(get_db),
                             current_user: Users =
                             Depends(auth.get_current_user)):
    Crud.update_user(current_user=current_user,
                     db=db, payload=payload)
    raise HTTPException(
        status_code=status.HTTP_202_ACCEPTED,
        detail="Your data was proceded.")


@router.put("/update/user/username", tags=["update/user"],
            response_model=UpdateResponse)
async def update_user_username(payload: UserUpdateUsernameSchema,
                               db: Session = Depends(get_db),
                               current_user: Users =
                               Depends(auth.get_current_user)):
    if Crud.get_user_by_username(db=db, username=payload.username):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Choose a different username.",
            headers={"WWW-Authenticate": "Bearer"})
    Crud.update_username(current_user=current_user,
                         db=db, payload=payload)
    raise HTTPException(
        status_code=status.HTTP_202_ACCEPTED,
        detail="Your data was proceded.")


@router.post("/user/password/forget", tags=["forget/password"],
             response_model=ForgetPasswordResponse)
def forget_password(form: ForgetPasswordForm, db: Session = Depends(get_db)):
    user = Crud.get_user_by_email(db=db, email=form.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="We couldn't find your email in the database.",
            headers={"WWW-Authenticate": "Bearer"})
    if user:
        public_id = user.public_id
        confirmation_token_expires = timedelta(
            minutes=CONFIRMATION_TOKEN_EXPIRE_MINUSTES)
        password_reset_token = auth.create_access_token(
            data={"sub": public_id}, expires_delta=confirmation_token_expires
        )
        email.passwordforgetMail(
            to=user.email, body=password_reset_token, userName=user.username)
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="We sent you a token by email.",
            headers={"WWW-Authenticate": "Bearer"})


@router.put("/user/password/forget/token", tags=["forget/password"],
            response_model=ForgetPasswordTokenResponse)
def forget_password_token(user: ForgetToken, db: Session = Depends(get_db)):
    if not user.new_password == user.new_password_again:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Passwords are not match.",
            headers={"WWW-Authenticate": "Bearer"})
    current_user = auth.get_confirmation(user.forget_token)
    user_ = Crud.get_user_by_public_id(db, current_user.public_id)
    if user_:
        password = auth.get_password_hash(user.new_password)
        Crud.update_password(current_user=user_, db=db, password=password)
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Your password is changed successfully.",
            headers={"WWW-Authenticate": "Bearer"})
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There is a problem.",
            headers={"WWW-Authenticate": "Bearer"})
