import csv
from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.orm import MappedColumn, mapped_column, Session
from .config import PROJ_ROOT
from .database import Base, engine, SessionLocal, with_session

class Breed(Base):
  __tablename__ = "breed"
  id: MappedColumn[str] = mapped_column(primary_key=True)
  umbrella_id: MappedColumn[str] = mapped_column(index=True)
  readable_name: MappedColumn[str] = mapped_column()
  img_link: MappedColumn[str] = mapped_column()


Base.metadata.create_all(engine)

@with_session
def get_count_in_db(session: Optional[Session] = None):
  if session:
    return session.execute(select(func.count()).select_from(Breed)).scalar()

def __populate_db():
  DATA_SOURCE_PATH = PROJ_ROOT / "pup-db.csv"
  with open(DATA_SOURCE_PATH, mode="r", newline="") as f:
    session = SessionLocal()
    reader = csv.DictReader(f)
    for row in reader:
      breed_record = Breed(id=row['id'], umbrella_id=row['umbrella_id'], readable_name=row['readable_name'], img_link=row['img_link'])
      try:
        session.add(breed_record)
        session.commit()
        print("DB POPULATED!")
      except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    session.close()

if get_count_in_db() == 0:
  __populate_db()
else:
  print("DB is already populated. We're good to go.")
