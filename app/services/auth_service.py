from __future__ import annotations

from datetime import timedelta
from typing import Optional
from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate


def register_user(db: Session, user_create: UserCreate) -> User:
    user = User(email=user_create.email, hashed_password=get_password_hash(user_create.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_user_token(user: User) -> str:
    return create_access_token(subject=str(user.id), expires_delta=timedelta(minutes=60))
