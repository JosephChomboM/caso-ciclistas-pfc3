from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.parking.models import Favorite, Parking


def list_parking(db: Session, district: str | None = None) -> list[Parking]:
    query = select(Parking).order_by(Parking.name).limit(200)
    if district:
        query = query.where(Parking.district == district)
    return list(db.scalars(query))


def get(db: Session, parking_id: int) -> Parking | None:
    return db.get(Parking, parking_id)


def favorite(db: Session, user_id: int, parking_id: int) -> Favorite | None:
    return db.scalar(
        select(Favorite).where(Favorite.user_id == user_id, Favorite.parking_id == parking_id)
    )


def list_favorites(db: Session, user_id: int) -> list[Parking]:
    return list(db.scalars(select(Parking).join(Favorite).where(Favorite.user_id == user_id)))
