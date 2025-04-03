from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from . import Base
from .enums import Role

if TYPE_CHECKING:
    from .file import File
    from .invite import InviteLink
    from .message import Message
    from .user import User


class Chat(Base):
    __tablename__ = "chats"

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(100), nullable=False)
    description: str = Column(Text)
    photo_id: str = Column(String(100), ForeignKey("files.id"))
    allow_forwarding: bool = Column(Boolean, default=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    deleted_at: datetime = Column(DateTime)

    members: List["ChatMember"] = relationship("ChatMember", back_populates="chat")
    messages: List["Message"] = relationship("Message", back_populates="chat")
    invite_links: List["InviteLink"] = relationship("InviteLink", back_populates="chat")
    permissions: List["ChatPermissions"] = relationship(
        "ChatPermissions", uselist=False, back_populates="chat"
    )
    photo: "File" = relationship("File")


class ChatPermissions(Base):
    __tablename__ = "chat_permissions"

    chat_id: int = Column(Integer, ForeignKey("chats.id"), primary_key=True)
    can_send_messages: bool = Column(Boolean, default=True)
    can_send_media: bool = Column(Boolean, default=True)
    can_add_users: bool = Column(Boolean, default=True)
    can_pin_messages: bool = Column(Boolean, default=False)

    chat: "Chat" = relationship("Chat", back_populates="permissions")


class ChatMember(Base):
    __tablename__ = "chat_members"
    __table_args__ = (
        UniqueConstraint("chat_id", "user_id", name="unique_chat_member"),
    )

    id: int = Column(Integer, primary_key=True)
    chat_id: int = Column(Integer, ForeignKey("chats.id"), nullable=False)
    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    role: Role = Column(Enum(Role), default=Role.MEMBER)
    joined_at: datetime = Column(DateTime, default=datetime.utcnow)
    deleted_at: datetime = Column(DateTime)
    restrictions: Dict[str, Any] = Column(JSON)

    chat: "Chat" = relationship("Chat", back_populates="members")
    user: "User" = relationship("User")
