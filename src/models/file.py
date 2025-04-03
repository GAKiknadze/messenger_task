from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, LargeBinary, String

from . import Base


class File(Base):
    __tablename__ = "files"

    id: str = Column(String(100), primary_key=True)
    file_path: str | None = Column(String(200))
    file_size: int | None = Column(Integer)
    mime_type: str | None = Column(String(50))
    content: bytes | None = Column(LargeBinary)
    uploaded_at: datetime = Column(DateTime, default=datetime.utcnow)
