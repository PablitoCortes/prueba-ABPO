
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime,Integer, String
from sqlalchemy.orm import  relationship
from db.db import Base

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    nationality = Column(String, index=True, nullable=True)
    date_of_birth = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at =Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    books = relationship("Book", back_populates="author")

    def __repr__(self):
        return f"<Author(name={self.name})>"
