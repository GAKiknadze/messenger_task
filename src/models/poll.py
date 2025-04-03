from typing import List

from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from . import Base
from .enums import PollType


class Poll(Base):
    __tablename__ = "polls"

    id: int = Column(Integer, primary_key=True)
    question: str = Column(String(300))
    type: PollType = Column(Enum(PollType))
    is_closed: bool = Column(Boolean, default=False)
    is_anonymous: bool = Column(Boolean, default=True)
    message_id: int = Column(Integer, ForeignKey("messages.id"))
    options: List["PollOption"] = relationship(
        "PollOption", cascade="all, delete-orphan"
    )


class PollOption(Base):
    __tablename__ = "poll_options"

    id: int = Column(Integer, primary_key=True)
    poll_id: int = Column(Integer, ForeignKey("polls.id"))
    text: str = Column(String(200))
    voter_count: int = Column(Integer, default=0)
