from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.billing.models import Invoice, Subscription


def subscription(db: Session, user_id: int, *, lock: bool = False) -> Subscription | None:
    query = select(Subscription).where(Subscription.user_id == user_id)
    return db.scalar(query.with_for_update() if lock else query)


def invoices(db: Session, user_id: int) -> list[Invoice]:
    return list(
        db.scalars(
            select(Invoice)
            .where(Invoice.user_id == user_id)
            .order_by(Invoice.created_at.desc(), Invoice.id.desc())
            .limit(50)
        )
    )
