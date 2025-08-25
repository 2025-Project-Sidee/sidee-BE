from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate,UserUpdate
from jose import JWTError, jwt
import bcrypt
import os
from datetime import datetime, timedelta

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def get_password_hash(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_user(db: Session, user: UserCreate):
    hashed_pw = get_password_hash(user.password)
    db_user = User(
        userid=user.userid,
        username=user.username,
        password_hash=hashed_pw
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, userid: str, password: str):
    user = db.query(User).filter(User.userid == userid).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user


def update_user(db:Session, userid: str, user_update: UserUpdate):
    db_user = db.query(User).filter(User.userid == userid).first()

    if not db_user:
        return None

    for field, value in user_update.dict(exclude_unset=True).items(): #안들어온 값은 뺌
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user