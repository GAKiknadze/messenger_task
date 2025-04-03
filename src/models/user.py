from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    phone_number = Column(String(20))
    deleted_at = Column(DateTime)
    profile_photos = relationship("UserProfilePhoto", back_populates="user")


class UserProfilePhoto(Base):
    __tablename__ = "user_profile_photos"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    file_id = Column(String(100), ForeignKey("files.id"))
    added_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="profile_photos")
    file = relationship("File")
