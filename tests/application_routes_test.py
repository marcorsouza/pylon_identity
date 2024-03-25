def test_create_application(client, application_data):
    # Criar usuário
    response = client.post(
        '/admin/applications',
        json=application_data,
    )
    assert response.status_code == 201
    result = response.json()
    assert result['name'] == 'Aplicação Teste'
    assert result['acronym'] == 'teste'


def test_create_application_with_existing_acronym(
    client, application, application_data
):
    # Criar usuário
    response = client.post(
        '/admin/applications',
        json=application_data,
    )
    assert response.status_code == 400


def test_read_applications(client):
    response = client.get('/admin/applications/')
    assert response.status_code == 200
    assert response.json() == {'applications': []}


def test_read_application_with_applications(client, application):
    # user_schema = UserPublic.model_validate(user).model_dump(exclude_unset=True)
    response = client.get('/admin/applications/')
    assert response.status_code == 200
    result = response.json()['applications']
    assert result[0]['name'] == 'Aplicação Teste'
    assert result[0]['acronym'] == 'teste'


def test_read_application(client, application):
    response = client.get('/admin/applications/1')
    assert response.status_code == 200
    result = response.json()
    assert result['name'] == 'Aplicação Teste'
    assert result['acronym'] == 'teste'


def test_get_nonexistent_application(client):
    response = client.get('/admin/applications/999')
    assert response.status_code == 404


def test_update_application(client, application, token):
    response = client.put(
        '/admin/applications/1',
        # headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Atualizar Nome da Aplicação', 'acronym': 'Teste1'},
    )
    assert response.status_code == 200
    result = response.json()
    assert result['name'] == 'Atualizar Nome da Aplicação'
    assert result['acronym'] == 'Teste1'


def test_update_application_nonexistent_application(client):
    response = client.put(
        '/admin/applications/99',
        json={'name': 'Atualizar Nome da Aplicação', 'acronym': 'Teste1'},
    )
    assert response.status_code == 404


def test_delete_application(client, application, token):
    response = client.delete(
        f'/admin/applications/{application.id}',
        # headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert response.json() == {'message': 'Application deleted'}


def test_delete_application_nonexistent_application(client):
    response = client.delete('/admin/applications/99')
    assert response.status_code == 404
