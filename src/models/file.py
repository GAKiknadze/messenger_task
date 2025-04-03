from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, LargeBinary, String

from . import Base


class File(Base):
    __tablename__ = "files"

    id = Column(String(100), primary_key=True)
    file_path = Column(String(200))
    file_size = Column(Integer)
    mime_type = Column(String(50))
    content = Column(LargeBinary)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
