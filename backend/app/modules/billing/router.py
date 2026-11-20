from fastapi import APIRouter
from fastapi.responses import Response

from app.modules.billing import service
from app.modules.billing.schemas import InvoiceOut, PlanChange, SubscriptionOut
from app.modules.users.service import CurrentActor, Db

router = APIRouter(prefix="/api/billing", tags=["Planes de demostración"])


@router.get("/plans")
def plans():
    return {"mode": "demo", "currency": "PEN", "plans": service.PLANS}


@router.get("/subscription", response_model=SubscriptionOut)
def subscription(db: Db, actor: CurrentActor):
    return service.subscription(db, actor.id)


@router.put("/subscription", response_model=SubscriptionOut)
def change_plan(data: PlanChange, db: Db, actor: CurrentActor):
    return service.change_plan(db, actor.id, data.plan_code)


@router.get("/invoices", response_model=list[InvoiceOut])
def invoices(db: Db, actor: CurrentActor):
    return service.invoices(db, actor.id)


@router.get("/favorites.csv")
def export_favorites(db: Db, actor: CurrentActor):
    return Response(
        service.export_favorites(db, actor.id),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="ciclolima-favoritos.csv"'},
    )
