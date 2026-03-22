import pytest
from fastapi.testclient import TestClient
from pupnow.main import app

client = TestClient(app)

@pytest.fixture()
def get():

  def _get(url):
    # 1. Arrange & Act
    response = client.get(url)

    # 2. Assert
    assert response.status_code == 200
    # 3. More testing after
    return response.json()

  return _get