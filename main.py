from fastapi import FastAPI
from typing import Union

app = FastAPI()
app.title = 'mi first app with fast-api'

@app.get("/")
def read_root():
    return {"Hello": "World"}
