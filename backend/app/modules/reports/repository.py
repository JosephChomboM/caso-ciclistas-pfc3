from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.reports.models import Report


def list_reports(db: Session, status: str, cycleway_id: int | None = None) -> list[Report]:
    query = (
        select(Report).where(Report.status == status).order_by(Report.created_at.desc()).limit(200)
    )
    if cycleway_id is not None:
        query = query.where(Report.cycleway_id == cycleway_id)
    return list(db.scalars(query))


def get(db: Session, report_id: int) -> Report | None:
    return db.get(Report, report_id)
