from pupnow.models import get_count_in_db


def test_read_main(get):
  assert get("/") == {"Hello": "World"}

def test_get_catalogue(get):
  data = get("/catalogue")
  isinstance(data, list)
  assert len(data) == get_count_in_db()
