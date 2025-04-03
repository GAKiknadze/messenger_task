from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class InviteLink(Base):
    __tablename__ = "invite_links"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    link = Column(String(200), unique=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    is_revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expire_date = Column(DateTime)
    member_limit = Column(Integer)

    chat = relationship("Chat", back_populates="invite_links")
    creator = relationship("User")
