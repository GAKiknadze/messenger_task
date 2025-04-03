from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from . import Base
from .enums import ContentType, DeletionType


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text)
    content_type = Column(Enum(ContentType), default=ContentType.TEXT)
    created_at = Column(DateTime, default=datetime.utcnow)
    edited_at = Column(DateTime)
    deleted_at = Column(DateTime)
    original_message_id = Column(Integer, ForeignKey("messages.id"))
    file_id = Column(String(100), ForeignKey("files.id"))
    location_data = Column(JSON)
    venue_data = Column(JSON)
    contact_data = Column(JSON)
    poll = relationship("Poll", uselist=False, backref="message")

    chat = relationship("Chat", back_populates="messages")
    sender = relationship("User")
    forwarded_from = relationship("Message", remote_side=[id])
    file = relationship("File")


class DeletedMessage(Base):
    __tablename__ = "deleted_messages"

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, nullable=False)
    deleted_at = Column(DateTime, default=datetime.utcnow)
    deletion_type = Column(Enum(DeletionType))
