from typing import Union
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

    class Config:
        schema_extra = {
            "example": {
                "confirmationToken": "string"
            }
        }


class UserCreateSchema(BaseModel):
    firstname: str = Field(min_length=2, max_length=30)
    lastname: str = Field(min_length=2, max_length=30)
    username: str = Field(min_length=8, max_length=20)
    email: EmailStr = Field(...)
    password: str = Field(...)


class UserUpdateSchema(BaseModel):
    firstname: str = Field(min_length=2, max_length=30)
    lastname: str = Field(min_length=2, max_length=30)


class UpdateResponse(BaseModel):
    detail: str


class UserUpdateUsernameSchema(BaseModel):
    username: str = Field(min_length=8, max_length=20)


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


class ConfirmationResponse(BaseModel):
    detail: str


class ForgetPasswordResponse(BaseModel):
    detail: str


class ForgetPasswordForm(BaseModel):
    email: EmailStr = Field(...)


class ForgetPasswordTokenResponse(BaseModel):
    detail: str


class ForgetToken(BaseModel):
    forget_token: str
    new_password: str
    new_password_again: str
