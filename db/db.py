from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
import os 

base_url = os.getenv("BASE_URL")

engine = create_engine(base_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)