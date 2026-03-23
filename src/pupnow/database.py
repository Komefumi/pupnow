from typing import Generator
from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from .config import PROJ_ROOT

DB_PATH = PROJ_ROOT / "data.db"
DB_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False}, echo=True)
SessionLocal = sessionmaker(bind=engine)
class Base(DeclarativeBase):
  pass

def with_session(f):
  @wraps(f)
  def wrapper(*args, **kwargs):
    with SessionLocal() as session:
      return f(session, *args, **kwargs)
  return wrapper

def get_db() -> Generator[Session, None, None]:
  with SessionLocal() as session:
    yield session