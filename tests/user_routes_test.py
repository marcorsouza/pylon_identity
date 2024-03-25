def test_create_user(client, user_data):
    # Criar usuário
    response = client.post(
        '/admin/users',
        json=user_data,
    )
    assert response.status_code == 201
    result = response.json()
    assert result['name'] == 'Testando Usuário'
    assert result['username'] == 'teste'
    assert result['email'] == 'novo@email.com'
    assert not result['is_locked_out']


def test_create_user_with_existing_username(client, user, user_data):
    # Criar usuário
    response = client.post(
        '/admin/users',
        json=user_data,
    )
    assert response.status_code == 400


def test_create_user_with_invalid_mail(client):
    # Criar usuário
    response = client.post(
        '/admin/users',
        json={
            'username': 'teste',
            'email': 'novo*email.com',
            'password': 'teste123',
        },
    )
    assert response.status_code == 422


def test_read_users(client):
    response = client.get('/admin/users/')
    assert response.status_code == 200
    assert response.json() == {'users': []}


def test_read_user_with_users(client, user):
    # user_schema = UserPublic.model_validate(user).model_dump(exclude_unset=True)
    response = client.get('/admin/users/')
    assert response.status_code == 200
    result = response.json()['users']
    assert result[0]['name'] == 'Testando Usuário'
    assert result[0]['username'] == 'teste'
    assert result[0]['email'] == 'novo@email.com'
    assert not result[0]['is_locked_out']
    assert not user.is_locked()


def test_read_user(client, user):
    response = client.get('/admin/users/1')
    assert response.status_code == 200
    result = response.json()
    assert result['name'] == 'Testando Usuário'
    assert result['username'] == 'teste'
    assert result['email'] == 'novo@email.com'
    assert not result['is_locked_out']


def test_get_nonexistent_user(client):
    response = client.get('/admin/users/999')
    assert response.status_code == 404


def test_update_user(client, user, token):
    response = client.put(
        '/admin/users/1',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Atualizar Nome do Usuário', 'is_locked_out': True},
    )
    assert response.status_code == 200
    result = response.json()
    assert result['name'] == 'Atualizar Nome do Usuário'
    assert result['username'] == 'teste'
    assert result['email'] == 'novo@email.com'
    assert result['is_locked_out']


def test_update_user_nonexistent_user(client):
    response = client.put(
        '/admin/users/99',
        json={'name': 'Atualizar Nome do Usuário', 'is_locked_out': True},
    )
    assert response.status_code == 401


def test_login_success(client, user):
    # Efetuar login
    response = client.post(
        '/auth/login',
        data={'username': 'teste', 'password': user.clean_password},
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
    )

    # Validar resposta
    token = response.json()
    assert response.status_code == 200
    assert 'access_token' in token
    assert 'token_type' in token
    assert response.json()['token_type'] == 'bearer'


def test_login_error(client, user):
    # Efetuar login
    response = client.post(
        '/auth/login',
        data={'username': 'teste', 'password': 'inicial'},
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
    )

    # Validar resposta
    assert response.status_code == 400
    assert 'Invalid username or password' in response.json()['detail']


def test_login_user_is_locked(client, user_blocked):
    # Efetuar login
    response = client.post(
        '/auth/login',
        data={'username': 'teste', 'password': 'inicial'},
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
    )

    # Validar resposta
    assert response.status_code == 400
    assert (
        'User is locked out. Please contact the administrator.'
        in response.json()['detail']
    )


def test_login_nonexistent_user(client):
    response = client.post(
        '/auth/login',
        data={'username': 'teste1', 'password': 'inicial'},
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
    )
    assert response.status_code == 404


def test_delete_user(client, user, token):
    response = client.delete(
        f'/admin/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_nonexistent_user(client):
    response = client.delete('/admin/users/99')
    assert response.status_code == 401


def test_update_user_with_wrong_user(client, user, token):
    response = client.put(
        '/admin/users/2',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Atualizar Nome do Usuário', 'is_locked_out': True},
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Not enough permissions'}
