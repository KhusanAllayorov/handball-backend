from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.models import User
from ..schemas.schemas import LoginRequest, RegisterRequest, TokenResponse, UserOut
from ..auth.jwt import create_token, hash_password, verify_password, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(status_code=400, detail="Bu email allaqachon ro'yxatdan o'tgan")
    user = User(
        email=body.email,
        full_name=body.full_name,
        password_hash=hash_password(body.password),
        password_plain=body.password,
        role_name=body.role_name,
        mode=body.mode,
        clinical=body.clinical,
        emoji=body.emoji,
        role_description=body.role_description,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return TokenResponse(token=create_token(user.id))


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.email).first()
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email yoki parol noto'g'ri")
    return TokenResponse(token=create_token(user.id))


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user
