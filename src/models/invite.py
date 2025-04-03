from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from . import Base

if TYPE_CHECKING:
    from .chat import Chat
    from .user import User


class InviteLink(Base):
    __tablename__ = "invite_links"

    id: int = Column(Integer, primary_key=True)
    chat_id: int = Column(Integer, ForeignKey("chats.id"))
    link: str = Column(String(200), unique=True)
    creator_id: int = Column(Integer, ForeignKey("users.id"))
    is_revoked: bool = Column(Boolean, default=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    expire_date: datetime | None = Column(DateTime)
    member_limit: int | None = Column(Integer, default=0)

    chat: "Chat" = relationship("Chat", back_populates="invite_links")
    creator: "User" = relationship("User")
