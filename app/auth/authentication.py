from decouple import config
from datetime import datetime, timedelta
from typing import Union
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from ..schemas.schemas import TokenData

SECRET = config("SECRET")
ALGORITHM = config("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Authentication:
    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    def authenticate_user(self, user, password: str):
        if not user:
            return False
        elif not self.verify_password(password, user.password):
            return False
        elif not user.confirmed:
            return False
        return user

    def create_access_token(self, data: dict,
                            expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
        return encoded_jwt

    def get_current_user(self, token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
            public_id: str = payload.get("sub")
            if public_id is None:
                raise credentials_exception
            token_data = TokenData(public_id=public_id)
        except JWTError:
            raise credentials_exception
        return token_data

    def get_confirmation(self, token: str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
            public_id: str = payload.get("sub")
            if public_id is None:
                raise credentials_exception
            token_data = TokenData(public_id=public_id)
        except JWTError:
            raise credentials_exception
        return token_data
