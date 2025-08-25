from sqlalchemy import Column, Integer, String, Enum, JSON, Text
from app.core.database import Base
import enum

class positionEnum(str, enum.Enum):
    frontend_developer = "frontend developer"
    backend_developer = "backend developer"
    designer = "designer"
    planner = "planner"

class User(Base):
    __tablename__ = "users"

    userid = Column(String(255), primary_key=True, unique=True, nullable=False)
    username = Column(String(50), nullable=False)
    password_hash = Column(String(255), nullable=False)
    bio = Column(Text, nullable=True)
    portfolio_links = Column(JSON, nullable=True)
    position = Column(Enum(positionEnum), nullable=True)
    profile_image = Column(String(255),nullable=True)
