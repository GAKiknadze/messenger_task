from datetime import datetime

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


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    photo_id = Column(String(100), ForeignKey("files.id"))
    allow_forwarding = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    deleted_at = Column(DateTime)

    members = relationship("ChatMember", back_populates="chat")
    messages = relationship("Message", back_populates="chat")
    invite_links = relationship("InviteLink", back_populates="chat")
    permissions = relationship("ChatPermissions", uselist=False, back_populates="chat")
    photo = relationship("File")


class ChatPermissions(Base):
    __tablename__ = "chat_permissions"

    chat_id = Column(Integer, ForeignKey("chats.id"), primary_key=True)
    can_send_messages = Column(Boolean, default=True)
    can_send_media = Column(Boolean, default=True)
    can_add_users = Column(Boolean, default=True)
    can_pin_messages = Column(Boolean, default=False)

    chat = relationship("Chat", back_populates="permissions")


class ChatMember(Base):
    __tablename__ = "chat_members"
    __table_args__ = (
        UniqueConstraint("chat_id", "user_id", name="unique_chat_member"),
    )

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(Enum(Role), default=Role.MEMBER)
    joined_at = Column(DateTime, default=datetime.utcnow)
    deleted_at = Column(DateTime)
    restrictions = Column(JSON)

    chat = relationship("Chat", back_populates="members")
    user = relationship("User")
