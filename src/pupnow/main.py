from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from .database import get_db
from . import models

Breed = models.Breed

app = FastAPI()

@app.get("/")
def read_root():
  return {"Hello": "World"}

@app.get("/catalogue")
def open_catalogue(db: Session = Depends(get_db)):
  return db.execute(select(Breed)).scalars().all()