from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..database.database import Base, get_db
from ..app import app
from decouple import config

DB_NAME = config("DB_NAME_TEST")
DB_USER = config("DB_USER")
DB_PASSWORD = config("DB_PASSWORD")
DB_HOST = config('DB_HOST')
DB_PORT = config('DB_PORT')
SQLALCHEMY_DATABASE_URL = "postgresql://" + \
    f"{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        clean_db()
        yield db
    finally:
        db.close()


def clean_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_user():
    response = client.post(
        "/users/",
        json={"email": "deadpool@example.com",
              "password": "chimichangas4life"},
        headers={"X-Token": "coneofsilence"})
    assert response.status_code == status.HTTP_201_CREATED, response.text
    data = response.json()
    assert data["detail"]
    assert data["detail"] == "User was created!"


def test_create_user_invalid():
    response = client.post("/users/",
                           json={"email": "deadpool@gmail.com"},
                           headers={"X-Token": "coneofsilence"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# def test_create_user_400():
#     response = client.post(
#         "/users/",
#         json={"email": "deadpool1@example.com",
#               "password": "chimichangas4life"},
#         headers={"X-Token": "coneofsilence"})
#     response = client.post(
#         "/users/",
#         json={"email": "deadpool1@example.com",
#               "password": "chimichangas4life"},
#         headers={"X-Token": "coneofsilence"})
#     assert response.status_code == 400, response.text
#     # data = response.json()
#     # assert data["detail"] == "Email already registered"
