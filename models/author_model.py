
from sqlalchemy import Column,Integer, String
from sqlalchemy.orm import  relationship
from db.db import Base

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    nationality = Column(String, index=True, nullable=True)
    dob = Column(String, nullable=True)

    books = relationship("Book", back_populates="author")

    def __repr__(self):
        return f"<Author(name={self.name})>"
