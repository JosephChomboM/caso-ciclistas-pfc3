from typing import Annotated

from fastapi import APIRouter, Query, Response

from app.modules.parking import service
from app.modules.parking.schemas import ParkingOut
from app.modules.users.service import CurrentActor, Db

router = APIRouter(prefix="/api/parking", tags=["Estacionamientos"])


@router.get("", response_model=list[ParkingOut])
def index(db: Db, district: Annotated[str | None, Query(max_length=80)] = None):
    return service.list_parking(db, district)


@router.get("/favorites", response_model=list[ParkingOut])
def favorites(db: Db, actor: CurrentActor):
    return service.favorites(db, actor.id)


@router.get("/{parking_id}", response_model=ParkingOut)
def detail(parking_id: int, db: Db):
    return service.get(db, parking_id)


@router.put("/{parking_id}/favorite", status_code=204)
def favorite(parking_id: int, db: Db, actor: CurrentActor):
    service.save_favorite(db, actor.id, parking_id)
    return Response(status_code=204)


@router.delete("/{parking_id}/favorite", status_code=204)
def unfavorite(parking_id: int, db: Db, actor: CurrentActor):
    service.remove_favorite(db, actor.id, parking_id)
    return Response(status_code=204)
