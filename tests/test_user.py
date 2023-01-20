from fastapi import status
from .test_conf import client, Base, engine


def test_create_user_201():
    response = client.post(
        "/signup/",
        json={"firstname": "TestFirstname",
              "lastname": "TestLastname",
              "username": "testname",
              "email": "testmail@email.com",
              "password": "Testpassword1."},
        headers={"X-Token": "coneofsilence"})
    assert response.status_code == status.HTTP_201_CREATED, response.text
    data = response.json()
    assert data["detail"]
    assert data["detail"] == "Please Confirm your mail " \
        "with the token was sent by mail."


def test_user_signup_409():
    response = client.post(
        "/signup/",
        json={"firstname": "Joe",
              "lastname": "Doe",
              "username": "joedoe34",
              "email": "testmail@email.com",
              "password": "Testpassword1."},
        headers={"X-Token": "coneofsilence"})
    assert response.status_code == 409
    assert response.json() == {
        "detail": "You have already had an account with the email."
    }


def test_user_sign_up_422():
    response = client.post(
        "/signup/",
        headers={"X-Token": "coneofsilence"},
        json={
            "firstname": "Joe",
            "lastname": "Doe",
            "username": "testname",
            "email": "testmailtest@email.com",
            "password": "any8.Any"
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": "Choose a different username."
    }


Base.metadata.drop_all(bind=engine)
