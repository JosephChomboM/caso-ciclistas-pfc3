"""Carga académica aditiva e idempotente; no contiene credenciales utilizables."""

import secrets

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.cycleways.models import Cycleway
from app.modules.parking.models import Favorite, Parking
from app.modules.reports.models import ModerationAction, Report
from app.modules.users.models import User

SOURCE = "Catálogo académico CicloLima · trazado ilustrativo sin verificación de campo"
ROUTES = [
    ("Malecón de Miraflores", "Miraflores", 2.4, -12.1198, -77.038),
    ("Conexión San Isidro", "San Isidro", 1.8, -12.098, -77.035),
    ("Circuito Barranco", "Barranco", 1.3, -12.14, -77.024),
    ("Conexión Parque Kennedy", "Miraflores", 1.1, -12.117, -77.029),
    ("Paseo de los parques", "Miraflores", 3.2, -12.113, -77.041),
    ("Enlace Reducto", "Miraflores", 1.6, -12.126, -77.021),
    ("Recorrido La Aurora", "Miraflores", 2.8, -12.123, -77.009),
    ("Conexión El Olivar", "San Isidro", 2.1, -12.097, -77.033),
    ("Paseo empresarial", "San Isidro", 3.6, -12.091, -77.028),
    ("Enlace Salaverry", "San Isidro", 2.7, -12.099, -77.051),
    ("Paseo de las artes", "Barranco", 1.9, -12.144, -77.019),
    ("Enlace al malecón", "Barranco", 2.5, -12.151, -77.024),
]


def seed_showcase(db: Session) -> dict[str, int]:
    routes = []
    for name, district, length, lat, lon in ROUTES:
        row = db.scalar(select(Cycleway).where(Cycleway.name == name))
        if row is None:
            row = Cycleway(
                name=name,
                district=district,
                length_km=length,
                source=SOURCE,
                is_demo=True,
                geometry=[[lat, lon], [lat - 0.003, lon + 0.001], [lat - 0.006, lon + 0.002]],
            )
            db.add(row)
        routes.append(row)
    places = []
    for i, (name, district, _, lat, lon) in enumerate(ROUTES[:9]):
        parking_name = f"Punto de estacionamiento {chr(65 + i)}"
        row = db.scalar(select(Parking).where(Parking.name == parking_name))
        if row is None:
            row = Parking(
                name=parking_name,
                district=district,
                latitude=lat,
                longitude=lon,
                address=f"Punto ilustrativo próximo a {name}",
                hours="Horario de ejemplo: 07:00 a 21:00",
                rack_type="U invertida (ejemplo)",
                source=SOURCE,
                is_demo=True,
            )
            db.add(row)
        places.append(row)
    people = []
    for name in ["ana", "diego", "lucia", "moderacion"]:
        email = f"ciclolima-demo-{name}@example.com"
        row = db.scalar(select(User).where(User.email == email))
        if row is None:
            row = User(
                email=email,
                alias=f"Ejemplo {name.title()}",
                password_hash=hash_password(secrets.token_urlsafe(48)),
                district="Miraflores",
                role="moderator" if name == "moderacion" else "cyclist",
            )
            db.add(row)
        people.append(row)
    db.flush()
    for i, route in enumerate(routes[:9]):
        description = (
            f"[Ejemplo académico {i + 1:02d}] "
            + [
                "Obstáculo ilustrativo junto al cruce.",
                "Señalización de ejemplo por revisar.",
                "Superficie irregular simulada en este tramo.",
            ][i % 3]
        )
        report = db.scalar(select(Report).where(Report.description == description))
        if report is None:
            status = "published" if i < 6 else "pending" if i < 8 else "rejected"
            report = Report(
                user_id=people[i % 3].id,
                cycleway_id=route.id,
                category=["Obstáculo", "Señalización", "Vía deteriorada"][i % 3],
                description=description,
                latitude=route.geometry[0][0],
                longitude=route.geometry[0][1],
                status=status,
            )
            db.add(report)
            db.flush()
            if status != "pending":
                db.add(
                    ModerationAction(
                        report_id=report.id,
                        moderator_id=people[3].id,
                        decision=status,
                    )
                )
    for i, person in enumerate(people[:3]):
        for place in places[i * 2 : i * 2 + 2]:
            existing = db.scalar(
                select(Favorite).where(
                    Favorite.user_id == person.id,
                    Favorite.parking_id == place.id,
                )
            )
            if existing is None:
                db.add(Favorite(user_id=person.id, parking_id=place.id))
    db.commit()
    return {"catalog_cycleways": len(routes), "catalog_parking": len(places), "demo_users": 4}
