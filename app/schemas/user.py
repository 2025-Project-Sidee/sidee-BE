from pydantic import BaseModel, constr, HttpUrl, ConfigDict
from typing import Optional, List
from enum import Enum
from app.models.user import positionEnum


# 회원가입 요청 스키마
class UserCreate(BaseModel):
    userid: constr(min_length=3, max_length=255)
    username: constr(min_length=1, max_length=50)
    password: constr(min_length=8)
    # bio: Optional[str] = None   
    # portfolio_links: Optional[List[HttpUrl]] = None  # URL 형식 검사
    # profile_image: Optional[HttpUrl] = None
    # position: positionEnum  = None

class UserLogin(BaseModel):
    userid: str
    password: str

class UserUpdate(BaseModel):
    username: Optional[constr(min_length=1, max_length=50)] = None
    password: Optional[constr(min_length=8)] = None
    bio: Optional[str] = None
    portfolio_links: Optional[List[HttpUrl]] = None
    profile_image: Optional[HttpUrl] = None
    position: Optional[positionEnum] = None

    # 링크 개수 검증
    @classmethod
    def check_linklength(cls, v):
        if v and len(v) > 3:
            raise ValueError("url은 최대 3개까지 추가할 수 있습니다.")

class UserResponse(BaseModel):
    userid: str
    username: str
    bio: Optional[str] = None
    position: Optional[str] = None
    portfolio_links: Optional[str] = None  # 문자열로 받음 (콤마 구분 등)
    profile_image: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class Config:
        from_attributes = True
