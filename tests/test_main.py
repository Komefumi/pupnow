from fastapi.testclient import TestClient
from pupnow.main import app


def test_read_main(get):
  assert get("/") == {"Hello": "World"}

def test_get_catalogue(get):
  isinstance(get("/catalogue"), list)