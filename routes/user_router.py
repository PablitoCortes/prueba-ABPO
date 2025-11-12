from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.db import get_db
from schemas.user_schema import UserCreate, UserLogin, Token
from services.user.user_services import register_user, login_user
from core.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserCreate)
def register(data: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, data)

@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, data.username, data.password)

@router.get("/profile")
def get_profile(current_user = Depends(get_current_user)):
    return {"message": f"Welcome {current_user.username}"}
