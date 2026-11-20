from fastapi import APIRouter

from app.modules.reports import service
from app.modules.reports.schemas import Decision, ReportIn, ReportOut
from app.modules.users.service import CurrentActor, Db, Moderator

router = APIRouter(prefix="/api/reports", tags=["Reportes"])


@router.get("", response_model=list[ReportOut])
def index(db: Db, cycleway_id: int | None = None):
    return service.list_reports(db, "published", cycleway_id)


@router.post("", response_model=ReportOut, status_code=201)
def create(data: ReportIn, db: Db, actor: CurrentActor):
    return service.create(db, actor.id, data)


@router.get("/pending", response_model=list[ReportOut])
def pending(db: Db, actor: Moderator):
    return service.list_reports(db, "pending")


@router.patch("/{report_id}/moderate", response_model=ReportOut)
def moderate(report_id: int, data: Decision, db: Db, actor: Moderator):
    return service.moderate(db, report_id, actor.id, data.status)
