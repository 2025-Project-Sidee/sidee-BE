from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, UserUpdate
from app.services import authService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(authService.User).filter(authService.User.userid == user.userid).first()
    if db_user:
        raise HTTPException(status_code=400, detail="이미 존재하는 아이디입니다.") #이미 아이디가 존재할 때
    return authService.create_user(db, user)

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    auth_user = authService.authenticate_user(db, user.userid, user.password)
    if not auth_user:
        raise HTTPException(status_code=401, detail="존재하지 않는 유저입니다.") #존재하지 않는 유저일 때
    token = authService.create_access_token({"sub": auth_user.userid})
    return {"access_token": token, "token_type": "bearer"}

@router.put("/{userid}", response_model=UserResponse)
def edit_user(userid: str, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = authService.update_user(db, userid, user_update)
    if not db_user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return db_user

@router.get("/{userid}",response_model=UserResponse)
def getuser(userid:str, db: Session = Depends(get_db)):
    db_user = db.query(authService.User).filter(authService.User.userid == userid).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return UserResponse.from_orm(db_user)
