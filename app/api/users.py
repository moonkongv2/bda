from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.security import hash_password

router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=UserResponse)
def create_user(user: UserCreate, db:Session = Depends(get_db)):
    pw_bytes = user.password.encode("utf-8")
    if len(pw_bytes) > 72:
        raise HTTPException(
            status_code=400, 
            detail="Password too long (bcrypt supports up to 72 bytes). Use a shorter password."
        )
    
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = User(
        email=user.email,
        password_hash = hash_password(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
