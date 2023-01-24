from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config
from app.models.users import Users
from app.auth.authentication import Authentication
from datetime import timedelta

CONFIRMATION_TOKEN_EXPIRE_MINUSTES = int(config(
    "CONFIRMATION_TOKEN_EXPIRE_MINUSTES"))
confirmation_token_expires = timedelta(
    minutes=CONFIRMATION_TOKEN_EXPIRE_MINUSTES)
auth = Authentication()

DB_NAME = config("DB_NAME_TEST")
DB_USER = config("DB_USER")
DB_PASSWORD = config("DB_PASSWORD")
DB_HOST = config('DB_HOST')
DB_PORT = config('DB_PORT')
SQLALCHEMY_DATABASE_URL = "postgresql://" + \
    f"{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


db = SessionLocal()


def crud_public_id(email):
    p_id = db.query(Users).filter(Users.email == email).first().public_id
    return p_id
