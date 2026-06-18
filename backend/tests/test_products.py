from tests.conftest import create_admin_user


def test_create_category(client):

    # create admin user

    create_admin_user()


    # login admin

    login_payload = {
        "username": "admin@test.com",
        "password": "Password@123"
    }

    login_response = client.post(
        "/auth/login",
        data=login_payload
    )

    token = login_response.json()["access_token"]


    # auth header

    headers = {
        "Authorization": f"Bearer {token}"
    }


    # create category

    payload = {
        "name": "Tablet",
        "description": "Tablet category"
    }

    response = client.post(
        "/categories",
        json=payload,
        headers=headers
    )

    assert response.status_code == 200