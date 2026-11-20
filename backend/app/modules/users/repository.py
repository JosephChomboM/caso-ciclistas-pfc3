from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.users.models import User


def find_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == email.lower()))


def find_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def create(db: Session, **values) -> User:
    user = User(**values)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
