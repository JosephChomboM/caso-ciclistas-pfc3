from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.cycleways.models import Cycleway


def list_cycleways(db: Session, district: str | None, condition: str | None) -> list[Cycleway]:
    query = select(Cycleway).order_by(Cycleway.name).limit(200)
    if district:
        query = query.where(Cycleway.district == district)
    if condition:
        query = query.where(Cycleway.condition == condition)
    return list(db.scalars(query))


def get(db: Session, cycleway_id: int) -> Cycleway | None:
    return db.get(Cycleway, cycleway_id)
