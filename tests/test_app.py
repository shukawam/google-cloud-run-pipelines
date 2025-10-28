import pytest

from app import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_greet(client):
    response = client.get("/greet")
    assert response.status_code == 200
    assert response.data == b"Hello world - demo"
