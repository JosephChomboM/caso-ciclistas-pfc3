from dataclasses import dataclass
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import decode_token, hash_password, issue_token, verify_password
from app.modules.users import repository
from app.modules.users.schemas import Credentials, ProfileUpdate, Register, UserOut

bearer = HTTPBearer(auto_error=False)
dummy_hash = hash_password("unused-dummy-password-for-timing")
Db = Annotated[Session, Depends(get_db)]


@dataclass(frozen=True)
class Actor:
    id: int
    role: str


def register(db: Session, data: Register) -> UserOut:
    try:
        return UserOut.model_validate(
            repository.create(
                db,
                email=str(data.email).lower(),
                password_hash=hash_password(data.password),
                alias=data.alias,
            )
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "No se pudo registrar ese correo") from None


def login(db: Session, data: Credentials) -> str:
    user = repository.find_by_email(db, str(data.email))
    valid = verify_password(data.password, user.password_hash if user else dummy_hash)
    if not user or not valid:
        raise HTTPException(401, "Correo o contraseña incorrectos")
    return issue_token(user.id, user.token_version)


def current_actor(
    db: Db,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
) -> Actor:
    try:
        if credentials is None:
            raise ValueError("missing")
        payload = decode_token(credentials.credentials)
        user = repository.find_by_id(db, int(payload["sub"]))
        if user is None or user.token_version != payload["ver"]:
            raise ValueError("revoked")
        return Actor(user.id, user.role)
    except (jwt.InvalidTokenError, ValueError, KeyError, TypeError):
        raise HTTPException(401, "Inicia sesión para continuar") from None


CurrentActor = Annotated[Actor, Depends(current_actor)]


def moderator(actor: CurrentActor) -> Actor:
    if actor.role != "moderator":
        raise HTTPException(403, "Esta acción requiere un moderador")
    return actor


Moderator = Annotated[Actor, Depends(moderator)]


def profile(db: Session, actor: Actor) -> UserOut:
    return UserOut.model_validate(repository.find_by_id(db, actor.id))


def update_profile(db: Session, actor: Actor, data: ProfileUpdate) -> UserOut:
    user = repository.find_by_id(db, actor.id)
    user.alias, user.district = data.alias, data.district
    db.commit()
    return UserOut.model_validate(user)


def logout(db: Session, actor: Actor) -> None:
    user = repository.find_by_id(db, actor.id)
    user.token_version += 1
    db.commit()
