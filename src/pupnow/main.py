from fastapi import FastAPI
from pyrsistent import v

app = FastAPI()

@app.get("/")
def read_root():
  return {"Hello": "World"}

@app.get("/catalogue")
def open_catalogue():
  return v({"item_name": "aaa"}).append({"item_name": "bbb"}).tolist()