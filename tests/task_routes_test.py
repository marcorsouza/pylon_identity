def test_create_task(client, task_data):
    # Criar usuário
    response = client.post(
        '/admin/tasks',
        json=task_data,
    )
    assert response.status_code == 201
    result = response.json()
    assert result['name'] == 'Task 1'
    assert result['tag_name'] == 'TSK1'


def test_create_task_with_existing_tag_name(client, task, task_data):
    # Criar usuário
    response = client.post(
        '/admin/tasks',
        json=task_data,
    )
    assert response.status_code == 400


def test_read_tasks(client):
    response = client.get('/admin/tasks/')
    assert response.status_code == 200
    assert response.json() == {'tasks': []}


def test_read_task_with_tasks(client, task):
    # user_schema = UserPublic.model_validate(user).model_dump(exclude_unset=True)
    response = client.get('/admin/tasks/')
    assert response.status_code == 200
    result = response.json()['tasks']
    assert result[0]['name'] == 'Task 1'
    assert result[0]['tag_name'] == 'TSK1'


def test_read_task(client, task):
    response = client.get('/admin/tasks/1')
    assert response.status_code == 200
    result = response.json()
    assert result['name'] == 'Task 1'
    assert result['tag_name'] == 'TSK1'


def test_get_nonexistent_task(client):
    response = client.get('/admin/tasks/999')
    assert response.status_code == 404


def test_update_task(client, task, token):
    response = client.put(
        '/admin/tasks/1',
        # headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'Task 2',
            'tag_name': 'TSK2',
            'icon': '',
            'show_in_menu': '',
            'menu_title': '',
        },
    )
    assert response.status_code == 200
    result = response.json()
    assert result['name'] == 'Task 2'
    assert result['tag_name'] == 'TSK2'


def test_update_task_nonexistent_task(client):
    response = client.put(
        '/admin/tasks/99',
        json={
            'name': 'Task 2',
            'tag_name': 'TSK2',
            'icon': '',
            'show_in_menu': '',
            'menu_title': '',
        },
    )
    assert response.status_code == 404


def test_delete_task(client, task, token):
    response = client.delete(
        f'/admin/tasks/{task.id}',
        # headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert response.json() == {'message': 'Task deleted'}


def test_delete_task_nonexistent_task(client):
    response = client.delete('/admin/tasks/99')
    assert response.status_code == 404
