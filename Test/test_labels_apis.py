def test_add_label(client,user_data,login_data,label_data):
    response = client.post('/user/register',json=user_data)
    assert response.status_code == 201

    response = client.post('/user/login',json=login_data)
    assert response.status_code == 200
    header = {'authorization':response.json()['access_token']}

    response = client.post('/labels/add', headers=header, json=label_data)
    assert response.status_code == 201


def test_update_label(client,user_data,login_data,label_data,update_label_data):
    response = client.post('/user/register',json=user_data)
    assert response.status_code == 201

    response = client.post('/user/login',json=login_data)
    assert response.status_code == 200
    header = {'authorization':response.json()['access_token']}

    response = client.post('/labels/add',json=label_data,headers=header)
    assert response.status_code == 201

    response = client.put('/labels/update/1', headers=header, json=update_label_data)
    assert response.status_code == 200


def test_get_all_labels_of_user(client,user_data,login_data,label_data):
    response = client.post('/user/register',json=user_data)
    assert response.status_code == 201

    response = client.post('/user/login',json=login_data)
    assert response.status_code == 200
    header = {'authorization':response.json()['access_token']}

    response = client.post('/labels/add',json=label_data,headers=header)
    assert response.status_code == 201

    response = client.get('/labels/get_all', headers=header)
    assert response.status_code == 200


def test_del_label(client,user_data,login_data,label_data):
    response = client.post('/user/register',json=user_data)
    assert response.status_code == 201

    response = client.post('/user/login',json=login_data)
    assert response.status_code == 200
    header = {'authorization':response.json()['access_token']}

    response = client.post('/labels/add',json=label_data,headers=header)
    assert response.status_code == 201

    resource = client.delete(f'/labels/del/1', headers=header)
    assert resource.status_code == 200
