import csv
from datetime import UTC, datetime
from io import StringIO

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.modules.billing import repository
from app.modules.billing.models import Invoice, Subscription
from app.modules.billing.schemas import InvoiceOut, SubscriptionOut
from app.modules.parking import service as parking

PLANS = [
    {
        "code": "free",
        "name": "Comunidad",
        "amount_centavos": 0,
        "features": ["Mapa y consulta de lugares", "Reportes comunitarios", "Favoritos personales"],
    },
    {
        "code": "plus",
        "name": "CicloLima Plus",
        "amount_centavos": 990,
        "features": [
            "Todo lo de Comunidad",
            "Exportación de favoritos en CSV",
            "Comprobantes simulados",
        ],
    },
]


def subscription(db: Session, user_id: int) -> SubscriptionOut:
    row = repository.subscription(db, user_id)
    return (
        SubscriptionOut(plan_code=row.plan_code, updated_at=row.updated_at)
        if row
        else SubscriptionOut(plan_code="free")
    )


def change_plan(db: Session, user_id: int, plan_code: str) -> SubscriptionOut:
    if plan_code not in {"free", "plus"}:
        raise HTTPException(422, "Elige un plan disponible")
    row = repository.subscription(db, user_id, lock=True)
    if row and row.plan_code == plan_code:
        return subscription(db, user_id)
    if row is None:
        row = Subscription(user_id=user_id, plan_code=plan_code)
        db.add(row)
    else:
        row.plan_code = plan_code
        row.updated_at = datetime.now(UTC)
    amount = 990 if plan_code == "plus" else 0
    db.add(Invoice(user_id=user_id, plan_code=plan_code, amount_centavos=amount))
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            409, "El plan cambió en otra solicitud. Actualiza e inténtalo de nuevo."
        ) from None
    return subscription(db, user_id)


def invoices(db: Session, user_id: int) -> list[InvoiceOut]:
    return [InvoiceOut.model_validate(row) for row in repository.invoices(db, user_id)]


def export_favorites(db: Session, user_id: int) -> str:
    if subscription(db, user_id).plan_code != "plus":
        raise HTTPException(403, "Activa el plan Plus de demostración para exportar")
    output = StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(["Nombre", "Distrito", "Dirección referencial", "Fuente"])
    for place in parking.favorites(db, user_id):
        values = [place.name, place.district, place.address, place.source]
        # Evitar fórmulas al abrir datos de catálogo en una hoja de cálculo.
        writer.writerow(
            ["'" + x if x.lstrip().startswith(("=", "+", "-", "@")) else x for x in values]
        )
    return "\ufeff" + output.getvalue()
