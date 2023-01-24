from fastapi import status
from .test_conf import client, Base, engine
from .test_crud import crud_public_id, auth, confirmation_token_expires


def test_create_user_201():
    response = client.post(
        "/signup/",
        json={"firstname": "TestFirstname",
              "lastname": "TestLastname",
              "username": "testname",
              "email": "testmail@email.com",
              "password": "Testpassword1."})
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
              "password": "Testpassword1."})
    assert response.status_code == 409
    assert response.json() == {
        "detail": "You have already had an account with the email."
    }


def test_user_sign_up_422():
    response = client.post(
        "/signup/",
        json={"firstname": "Joe",
              "lastname": "Doe",
              "username": "testname",
              "email": "testmailtest@email.com",
              "password": "any8.Any"},
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": "Choose a different username."
    }


def test_user_confirm_401():
    response = client.post(
        "/confirmation/",
        json={
            "confirmationToken":
            "yKTB6h6fpv_CcyOHLzfo1HOvRbfFGaqGBesXzR8XKHM"
        })
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Could not validate credentials"}


def test_user_confirmation_202():
    response = client.post(
        "/signup/",
        json={"firstname": "Confirmation",
              "lastname": "Confirmation",
              "username": "Confirmation",
              "email": "Confirmation@email.com",
              "password": "Confirmation."})
    assert response.status_code == status.HTTP_201_CREATED, response.text
    data = response.json()
    assert data["detail"]
    assert data["detail"] == "Please Confirm your mail " \
        "with the token was sent by mail."
    test_public_id = crud_public_id(email="Confirmation@email.com")
    confirmation_token = auth.create_access_token(
        data={"sub": test_public_id},
        expires_delta=confirmation_token_expires)
    resp = client.post(
        "/confirmation/",
        json={
            "confirmationToken": confirmation_token
        })
    assert resp.status_code == status.HTTP_202_ACCEPTED, resp.text
    data = resp.json()
    assert data["detail"]
    assert data["detail"] == "Confirmation's email "\
        "Confirmation@email.com is confirmed."


def test_user_confirmation_501():
    test_public_id = crud_public_id(email="Confirmation@email.com")
    confirmation_token = auth.create_access_token(
        data={"sub": test_public_id},
        expires_delta=confirmation_token_expires)
    resp = client.post(
        "/confirmation/",
        json={
            "confirmationToken": confirmation_token
        },
        headers={"X-Token": "coneofsilence"})
    assert resp.status_code == status.HTTP_501_NOT_IMPLEMENTED, resp.text
    data = resp.json()
    assert data["detail"]
    assert data["detail"] == "Confirmation's email "\
        "Confirmation@email.com has already confirmed."


def test_token_401():
    response = client.post(
        "/token/",
        data={"username": "johndoe", "password": "secret",
              "grant_type": "password"},
        headers={"content-type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Incorrect username or password"}


def test_token_202():
    response = client.post(
        "/token/",
        data={"username": "Confirmation",
              "password": "Confirmation.",
              "grant_type": "password"},
        headers={"content-type": "application/x-www-form-urlencoded"})
    assert response.status_code == status.HTTP_200_OK
    res = response.json()
    assert res['access_token']


def test_user_update_401():
    response = client.put("/user-update/",
                          json={"firstname": "1",
                                "lastname": "2"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_user_update_202():
    response = client.post("/token/",
                           data={"username": "Confirmation",
                                 "password": "Confirmation.",
                                 "grant_type": "password"},
                           headers={"content-type":
                                    "application/x-www-form-urlencoded"})
    assert response.status_code == status.HTTP_200_OK
    res = response.json()
    assert res['access_token']
    access_token = res['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.put("/user-update",
                          json={"firstname": "123412",
                                "lastname": "2123123"}, headers=headers)
    assert response.status_code == status.HTTP_202_ACCEPTED


Base.metadata.drop_all(bind=engine)
