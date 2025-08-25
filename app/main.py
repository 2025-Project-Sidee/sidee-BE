from fastapi import FastAPI
from app.routes import auth
from app.core.database import Base, engine
from app.models.user import User

app = FastAPI()

app.include_router(auth.router)

# 앱 시작 시 테이블 생성
Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Hello FastAPI!"}

@app.get("/ping")
def ping():
    return {"message": "pong!"}  

@app.get("/tiki")
def taka():
    return {"message":"taka"}


 