import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

DB_URL = "sqlite:///:memory:"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False}, echo=True)
SessionLocal = sessionmaker(bind=engine)
class Base(DeclarativeBase):
  pass


def get_db() -> Generator[Session, None, None]:
  with SessionLocal() as session:
    yield session