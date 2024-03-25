def test_create_role(client, role_data):
    # Criar usuário
    response = client.post(
        '/admin/roles',
        json=role_data,
    )
    assert response.status_code == 201
    result = response.json()
    assert result['name'] == 'Admin'


def test_read_roles(client):
    response = client.get('/admin/roles/')
    assert response.status_code == 200
    assert response.json() == {'roles': []}


def test_read_role_with_roles(client, role):
    # user_schema = UserPublic.model_validate(user).model_dump(exclude_unset=True)
    response = client.get('/admin/roles/')
    assert response.status_code == 200
    result = response.json()['roles']
    assert result[0]['name'] == 'Admin'


def test_read_role(client, role):
    response = client.get('/admin/roles/1')
    assert response.status_code == 200
    result = response.json()
    assert result['name'] == 'Admin'


def test_get_nonexistent_role(client):
    response = client.get('/admin/roles/999')
    assert response.status_code == 404


def test_update_role(client, role, token):
    response = client.put(
        '/admin/roles/1',
        # headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Guest', 'application_id': role.application_id},
    )
    assert response.status_code == 200
    result = response.json()
    assert result['name'] == 'Guest'


def test_update_role_nonexistent_role(client):
    response = client.put(
        '/admin/roles/99',
        json={'name': 'Guest', 'application_id': 1},
    )
    assert response.status_code == 404


def test_delete_role(client, role, token):
    response = client.delete(
        f'/admin/roles/{role.id}',
        # headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert response.json() == {'message': 'Role deleted'}


def test_delete_role_nonexistent_role(client):
    response = client.delete('/admin/roles/99')
    assert response.status_code == 404
