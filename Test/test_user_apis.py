def test_user_registration(client, user_data):
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201


def test_login_user(client, user_data, login_data):
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201

    response = client.post('/user/login', json=login_data)
    assert response.status_code == 200

