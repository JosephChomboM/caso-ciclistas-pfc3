from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.cycleways import repository
from app.modules.cycleways.schemas import CyclewayOut


def list_cycleways(db: Session, district: str | None, condition: str | None) -> list[CyclewayOut]:
    return [
        CyclewayOut.model_validate(x) for x in repository.list_cycleways(db, district, condition)
    ]


def get(db: Session, cycleway_id: int) -> CyclewayOut:
    row = repository.get(db, cycleway_id)
    if row is None:
        raise HTTPException(404, "No se encontró ese tramo")
    return CyclewayOut.model_validate(row)
