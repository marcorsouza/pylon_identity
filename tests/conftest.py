import pytest
from fastapi.testclient import TestClient
from pylon.api.models.base import Base
from pylon.config.helpers import get_session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from pylon_identity.app import app

metadata = Base.metadata


def truncate_all_tables(connectable):
    with connectable.connect() as connection:
        Session = sessionmaker(bind=connection)
        session = Session()
        session.execute(text('SET FOREIGN_KEY_CHECKS = 0;'))
        for table in metadata.sorted_tables:
            try:
                session.execute(table.delete())
            except Exception:
                pass
        session.execute(text('SET FOREIGN_KEY_CHECKS = 1;'))
        session.commit()


@pytest.fixture
def session():
    engine = create_engine(
        'mysql://root:1234@localhost:3306/test_meudb',
        # connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # Base.metadata.create_all(engine)
    truncate_all_tables(engine)
    yield Session()
    # Base.metadata.drop_all(engine)
    truncate_all_tables(engine)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()
