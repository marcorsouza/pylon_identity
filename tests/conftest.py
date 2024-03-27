import pytest
from fastapi.testclient import TestClient
from pylon.config.helpers import get_session
from pylon.utils.encryption_utils import encrypt_value
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from pylon_identity.api.admin.models import Application, Base, Role, Task, User
from pylon_identity.app import app


@pytest.fixture
def user_data():
    return {
        'name': 'Testando Usuário',
        'username': 'teste',
        'email': 'novo@email.com',
        'password': 'teste123',
    }


@pytest.fixture
def application_data():
    return {'name': 'Aplicação Teste', 'acronym': 'teste'}


@pytest.fixture
def role_data(application):
    return {'name': 'Admin', 'application_id': application.id}


@pytest.fixture
def task_data():
    return {
        'name': 'Task 1',
        'tag_name': 'TSK1',
        'icon': '',
        'show_in_menu': '',
        'menu_title': '',
        'actions': [
            {'name': 'ACTION 1'},
            {'name': 'ACTION 2'},
            {'name': 'ACTION 3'},
        ],
    }


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(engine)
    yield Session()
    Base.metadata.drop_all(engine)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def user(session):
    password = 'teste123'
    user = User(
        name='Testando Usuário',
        username='teste',
        email='novo@email.com',
        password=encrypt_value(password),
        is_locked_out=False,
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'teste123'

    return user


@pytest.fixture
def user_blocked(session):
    password = 'teste123'
    user = User(
        name='Testando Usuário',
        username='teste',
        email='novo@email.com',
        password=encrypt_value(password),
        is_locked_out=True,
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'teste123'

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/login',
        data={'username': user.username, 'password': user.clean_password},
    )
    return response.json()['access_token']


@pytest.fixture
def application(session):
    application = Application(name='Aplicação Teste', acronym='teste')
    session.add(application)
    session.commit()
    session.refresh(application)

    return application


@pytest.fixture
def role(session, application):
    role = Role(name='Admin', application_id=application.id)
    session.add(role)
    session.commit()
    session.refresh(role)

    return role


@pytest.fixture
def task(session):
    task = Task(
        name='Task 1', tag_name='TSK1', icon='', show_in_menu='', menu_title=''
    )
    session.add(task)
    session.commit()
    session.refresh(task)

    return task
