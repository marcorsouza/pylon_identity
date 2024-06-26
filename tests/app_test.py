from fastapi.testclient import TestClient

from pylon_identity.app import app


def test_index():
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Welcome to Pylon Identity API'}
