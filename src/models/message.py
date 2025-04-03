from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict

from sqlalchemy import JSON, Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from . import Base
from .enums import ContentType, DeletionType

if TYPE_CHECKING:
    from .chat import Chat
    from .file import File
    from .poll import Poll
    from .user import User


class Message(Base):
    __tablename__ = "messages"

    id: int = Column(Integer, primary_key=True)
    chat_id: int = Column(Integer, ForeignKey("chats.id"), nullable=False)
    sender_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    content: str = Column(Text)
    content_type: ContentType = Column(Enum(ContentType), default=ContentType.TEXT)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    edited_at: datetime = Column(DateTime)
    deleted_at: datetime = Column(DateTime)
    original_message_id: int = Column(Integer, ForeignKey("messages.id"))
    file_id: str = Column(String(100), ForeignKey("files.id"))
    location_data: Dict[str, Any] = Column(JSON)
    venue_data: Dict[str, Any] = Column(JSON)
    contact_data: Dict[str, Any] = Column(JSON)
    poll: "Poll" = relationship("Poll", uselist=False, backref="message")

    chat: "Chat" = relationship("Chat", back_populates="messages")
    sender: "User" = relationship("User")
    forwarded_from: "Message" = relationship("Message", remote_side=[id])
    file: "File" = relationship("File")


class DeletedMessage(Base):
    __tablename__ = "deleted_messages"

    id: int = Column(Integer, primary_key=True)
    message_id: int = Column(Integer, nullable=False)
    deleted_at: datetime = Column(DateTime, default=datetime.utcnow)
    deletion_type: DeletionType = Column(Enum(DeletionType))
