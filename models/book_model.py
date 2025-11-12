
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import  relationship
from datetime import datetime, timezone
from db.db import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    isbn = Column(String, index=True, nullable=False, unique=True)
    published_year = Column(Integer, nullable=True)
    genre = Column(String, index=True, nullable=True)
    is_available = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at =Column(DateTime, default=datetime.now(timezone.utc), nullable=False)


    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    author = relationship("Author", back_populates="books")

    def __repr__(self):
        return f"<Book(title={self.title})>"
