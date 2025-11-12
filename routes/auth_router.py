from fastapi import APIRouter
from schemas.auth_schema import UserOut

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=UserOut)
def login(data: LoginSchema, db: Session = Depends(get_db)):
    return auth_services.login(data, db)

@router.post("/register", response_model=UserOut)
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    return auth_services.register(data, db)


