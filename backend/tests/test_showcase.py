from sqlalchemy import func, select

from app.modules.cycleways.models import Cycleway
from app.modules.parking.models import Favorite, Parking
from app.modules.reports.models import ModerationAction, Report
from app.modules.users.models import User
from app.showcase import seed_showcase


def test_showcase_is_additive_idempotent_and_keeps_pending_private(db, client):
    seed_showcase(db)
    models = [Cycleway, Parking, User, Favorite, Report, ModerationAction]
    first = [db.scalar(select(func.count()).select_from(model)) for model in models]
    assert first == [12, 9, 4, 6, 9, 7]
    row = db.scalar(select(Cycleway).limit(1))
    row.source = "Fuente conservada"
    db.commit()
    seed_showcase(db)
    assert [db.scalar(select(func.count()).select_from(m)) for m in models] == first
    assert row.source == "Fuente conservada"
    reports = client.get("/api/reports", params={"cycleway_id": row.id})
    assert reports.status_code == 200
    assert all(r["status"] == "published" for r in reports.json())
    assert all(r["description"].startswith("[Ejemplo académico") for r in reports.json())
