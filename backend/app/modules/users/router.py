from fastapi import APIRouter, Response

from app.modules.users import service
from app.modules.users.schemas import Credentials, ProfileUpdate, Register, TokenOut, UserOut
from app.modules.users.service import CurrentActor, Db

router = APIRouter(prefix="/api/users", tags=["Usuarios"])


@router.post("/register", response_model=UserOut, status_code=201)
def register(data: Register, db: Db):
    return service.register(db, data)


@router.post("/login", response_model=TokenOut)
def login(data: Credentials, db: Db):
    return TokenOut(access_token=service.login(db, data))


@router.get("/me", response_model=UserOut)
def me(db: Db, actor: CurrentActor):
    return service.profile(db, actor)


@router.patch("/me", response_model=UserOut)
def update(data: ProfileUpdate, db: Db, actor: CurrentActor):
    return service.update_profile(db, actor, data)


@router.post("/logout", status_code=204)
def logout(db: Db, actor: CurrentActor):
    service.logout(db, actor)
    return Response(status_code=204)
