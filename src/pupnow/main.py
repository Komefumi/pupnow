from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
  return {"Hello": "World"}

@app.get("/catalogue")
def open_catalogue():
  return [{"item_name": "aaa"}]