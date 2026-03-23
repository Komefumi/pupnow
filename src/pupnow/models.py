import csv
from pathlib import Path
from sqlalchemy import JSON
from sqlalchemy.orm import MappedColumn, mapped_column
from .database import Base, engine, SessionLocal

class Breed(Base):
  __tablename__ = "breed"
  id: MappedColumn[str] = mapped_column(primary_key=True)
  umbrella_id: MappedColumn[str] = mapped_column(index=True)
  readable_name: MappedColumn[str] = mapped_column()
  img_link: MappedColumn[str] = mapped_column()


Base.metadata.create_all(engine)

def __populate_db():
  CURRENT_FILE = Path(__file__).resolve()
  ROOT = CURRENT_FILE.parents[2]
  DATA_SOURCE_PATH = ROOT / "pup-db.csv"
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

__populate_db()