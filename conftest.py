import pytest
from api_client import ApiClient


@pytest.fixture
def client():
    return ApiClient()


@pytest.fixture
def token(client):

    response = client.auth()

    assert response.status_code == 201

    return response.json()["token"]