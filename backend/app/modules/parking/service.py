from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.modules.parking import repository
from app.modules.parking.models import Favorite
from app.modules.parking.schemas import ParkingOut


def list_parking(db: Session, district: str | None = None) -> list[ParkingOut]:
    return [ParkingOut.model_validate(x) for x in repository.list_parking(db, district)]


def get(db: Session, parking_id: int) -> ParkingOut:
    row = repository.get(db, parking_id)
    if row is None:
        raise HTTPException(404, "No se encontró ese estacionamiento")
    return ParkingOut.model_validate(row)


def favorites(db: Session, user_id: int) -> list[ParkingOut]:
    return [ParkingOut.model_validate(x) for x in repository.list_favorites(db, user_id)]


def save_favorite(db: Session, user_id: int, parking_id: int) -> None:
    get(db, parking_id)
    if repository.favorite(db, user_id, parking_id) is None:
        db.add(Favorite(user_id=user_id, parking_id=parking_id))
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            if repository.favorite(db, user_id, parking_id) is None:
                raise


def remove_favorite(db: Session, user_id: int, parking_id: int) -> None:
    row = repository.favorite(db, user_id, parking_id)
    if row:
        db.delete(row)
        db.commit()
