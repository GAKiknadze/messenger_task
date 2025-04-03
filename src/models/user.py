from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from . import Base

if TYPE_CHECKING:
    from .file import File


class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True)
    username: str = Column(String(50), unique=True, nullable=False)
    phone_number: str = Column(String(20))
    deleted_at: datetime = Column(DateTime)
    profile_photos: List["UserProfilePhoto"] = relationship(
        "UserProfilePhoto", back_populates="user"
    )


class UserProfilePhoto(Base):
    __tablename__ = "user_profile_photos"

    id: int = Column(Integer, primary_key=True)
    user_id: int = Column(Integer, ForeignKey("users.id"))
    file_id: str = Column(String(100), ForeignKey("files.id"))
    added_at: datetime = Column(DateTime, default=datetime.utcnow)

    user: "User" = relationship("User", back_populates="profile_photos")
    file: "File" = relationship("File")
