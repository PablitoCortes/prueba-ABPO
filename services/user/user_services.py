from sqlalchemy.orm import Session
from models.user_model import User
from schemas.user_schema import UserCreate
from core.security import get_password_hash, verify_password
from core.auth import create_access_token
from fastapi import HTTPException

def register_user(db: Session, data: UserCreate):
    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")
    hashed_password = get_password_hash(data.password)
    new_user = User(username=data.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
