from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.cycleways import service as cycleways
from app.modules.reports import repository
from app.modules.reports.models import ModerationAction, Report
from app.modules.reports.schemas import ReportIn, ReportOut


def create(db: Session, user_id: int, data: ReportIn) -> ReportOut:
    cycleways.get(db, data.cycleway_id)
    row = Report(user_id=user_id, **data.model_dump())
    db.add(row)
    db.commit()
    return ReportOut.model_validate(row)


def list_reports(db: Session, status: str, cycleway_id: int | None = None) -> list[ReportOut]:
    return [ReportOut.model_validate(x) for x in repository.list_reports(db, status, cycleway_id)]


def moderate(db: Session, report_id: int, moderator_id: int, decision: str) -> ReportOut:
    row = repository.get(db, report_id)
    if not row:
        raise HTTPException(404, "No se encontró ese reporte")
    if row.status != "pending":
        raise HTTPException(409, "El reporte ya fue revisado")
    row.status = decision
    db.add(ModerationAction(report_id=row.id, moderator_id=moderator_id, decision=decision))
    db.commit()
    return ReportOut.model_validate(row)


def published_counts(db):
    """Estadística pública: nunca incluye reportes pendientes ni identidad del autor."""
    return repository.published_counts(db)
