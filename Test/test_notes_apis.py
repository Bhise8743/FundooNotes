def test_add_notes(client, user_data, login_data, notes_data):
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201

    response = client.post('/user/login', json=login_data)
    assert response.status_code == 200
    header_token = response.json()['access_token']
    header = {'authorization': header_token}

    response = client.post('/notes/add', headers=header, json=notes_data)
    assert response.status_code == 201


def test_get_all_notes(client, user_data, notes_data, login_data, new_notes_data):
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201

    response = client.post('/user/login', json=login_data)
    assert response.status_code == 200

    header = {'authorization': response.json()['access_token']}
    response = client.post('/notes/add', json=notes_data, headers=header)
    assert response.status_code == 201

    response = client.post('/notes/add', json=new_notes_data, headers=header)
    assert response.status_code == 201

    response = client.get('/notes/get', headers=header)
    assert response.status_code == 200


def test_update_notes(client, user_data, login_data, notes_data, update_notes_data, new_notes_data):
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201

    response = client.post('/user/login', json=login_data)
    assert response.status_code == 200
    header = {'authorization': response.json()['access_token']}

    response = client.post('/notes/add', json=notes_data, headers=header)
    assert response.status_code == 201

    response = client.post('/notes/add', json=new_notes_data, headers=header)
    assert response.status_code == 201

    response = client.patch('/notes/update/1', headers=header, json=update_notes_data)
    assert response.status_code == 200


def test_del_user_note(client, user_data, login_data, notes_data, new_notes_data):
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201

    response = client.post('/user/login', json=login_data)
    assert response.status_code == 200
    header = {'authorization': response.json()['access_token']}

    response = client.post('/notes/add', json=notes_data, headers=header)
    assert response.status_code == 201

    response = client.post('/notes/add', json=new_notes_data, headers=header)
    assert response.status_code == 201

    response = client.delete('/notes/del/1', headers=header)
    assert response.status_code == 200


def test_del_all_notes_of_user(client, user_data, login_data, notes_data, new_notes_data):
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201

    response = client.post('/user/login', json=login_data)
    assert response.status_code == 200
    header = {'authorization': response.json()['access_token']}

    response = client.post('/notes/add', json=notes_data, headers=header)
    assert response.status_code == 201

    response = client.post('/notes/add', json=new_notes_data, headers=header)
    assert response.status_code == 201

    response = client.delete('/notes/del_all', headers=header)
    assert response.status_code == 200
