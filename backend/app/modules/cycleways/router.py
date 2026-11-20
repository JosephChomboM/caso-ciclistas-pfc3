from typing import Annotated

from fastapi import APIRouter, Query

from app.modules.cycleways import service
from app.modules.cycleways.schemas import CyclewayOut, RecommendationOut
from app.modules.users.service import Db

router = APIRouter(prefix="/api/cycleways", tags=["Ciclovías"])
Filter = Annotated[str | None, Query(max_length=80)]


@router.get("", response_model=list[CyclewayOut])
def index(db: Db, district: Filter = None, condition: Filter = None):
    return service.list_cycleways(db, district, condition)


@router.get("/recommendations", response_model=list[RecommendationOut])
def recommendations(
    db: Db,
    district: Filter = None,
    target_km: Annotated[float, Query(ge=0.5, le=20, allow_inf_nan=False)] = 3,
):
    return service.recommend(db, district, target_km)


@router.get("/{cycleway_id}", response_model=CyclewayOut)
def detail(cycleway_id: int, db: Db):
    return service.get(db, cycleway_id)
