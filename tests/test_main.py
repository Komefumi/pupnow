from fastapi.testclient import TestClient
from pupnow.main import app

client = TestClient(app)

def test_read_main():
  # 1. Arrange & Act
  response = client.get("/")

  # 2. Assert
  assert response.status_code == 200
  assert response.json() == {"Hello": "World"}