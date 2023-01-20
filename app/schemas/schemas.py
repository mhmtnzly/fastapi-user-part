from typing import Union
from ..models.users import Users
from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    username: Union[str, None] = None
    email: Union[str, None] = None
    public_id: Union[str, None] = None
    firstname: Union[str, None] = None
    lastname: Union[str, None] = None
    confirmed: Union[bool, None] = None


class UserConfirm(BaseModel):
    confirmationToken: Union[str, None] = None


class UserCreateSchema(BaseModel):
    firstname: str = Field(min_length=2, max_length=30)
    lastname: str = Field(min_length=2, max_length=30)
    username: str = Field(min_length=8, max_length=20)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "firstname": "Joe",
                "lastname": "Doe",
                "username": "joedoe34",
                "email": "joe@xyz.com",
                "password": "any8.Any"
            }
        }


class UserLoginSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "joedoe34",
                "password": "any8.Any"
            }
        }


class SignupResponse(BaseModel):
    detail: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenConfirm(BaseModel):
    confirmation_token: str


class TokenData(BaseModel):
    public_id: Union[str, None] = None


class UserInDB(Users):
    hashed_password: str


class ConfirmationResponse(BaseModel):
    result: str
