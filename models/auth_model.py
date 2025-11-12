from datetime import date
from sqlalchemy import Column, String,DateTime
from db.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=date.now(), nullable=False)
    updated_at = Column(DateTime, default=date.now(), nullable=False)

    def __repr__(self):
        return f"<Login(username={self.username})>"


