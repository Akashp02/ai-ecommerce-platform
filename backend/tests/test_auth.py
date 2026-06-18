def test_register_user(client):

    payload = {
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@gmail.com",
        "password": "Password@123"
    }

    response = client.post(
        "/users",
        json=payload
    )

    assert response.status_code == 200


def test_duplicate_register(client):

    payload = {
        "first_name": "Test",
        "last_name": "User",
        "email": "duplicate@gmail.com",
        "password": "Password@123"
    }

    client.post(
        "/users",
        json=payload
    )

    response = client.post(
        "/users",
        json=payload
    )

    assert response.status_code == 400


def test_login(client):

    # create user first

    user_payload = {
        "first_name": "Login",
        "last_name": "User",
        "email": "loginuser@gmail.com",
        "password": "Password@123"
    }

    client.post(
        "/users",
        json=user_payload
    )

    # oauth2 login form

    login_payload = {
        "username": "loginuser@gmail.com",
        "password": "Password@123"
    }

    response = client.post(
        "/auth/login",
        data=login_payload
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data