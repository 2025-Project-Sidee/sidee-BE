# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI!"}

@app.get("/ping")
def ping():
    return {"message": "pong!"}  

@app.get("/tiki")
def taka():
    return {"message":"taka"}

