from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from . import Base
from .enums import PollType


class Poll(Base):
    __tablename__ = "polls"

    id = Column(Integer, primary_key=True)
    question = Column(String(300))
    type = Column(Enum(PollType))
    is_closed = Column(Boolean, default=False)
    is_anonymous = Column(Boolean, default=True)
    message_id = Column(Integer, ForeignKey("messages.id"))
    options = relationship("PollOption", cascade="all, delete-orphan")


class PollOption(Base):
    __tablename__ = "poll_options"

    id = Column(Integer, primary_key=True)
    poll_id = Column(Integer, ForeignKey("polls.id"))
    text = Column(String(200))
    voter_count = Column(Integer, default=0)
