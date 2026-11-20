"""Herramientas operativas; nunca se ejecutan al arrancar la API."""

import argparse

from sqlalchemy import select

from app.core.db import SessionLocal
from app.modules.cycleways.models import Cycleway
from app.modules.parking.models import Parking
from app.modules.users.models import User


def seed_demo():
    with SessionLocal() as db:
        if db.scalar(select(Cycleway.id).limit(1)) is not None:
            raise SystemExit("El catálogo ya tiene datos. No se modificó.")
        source = "Datos sintéticos para la práctica académica"
        rows = [
            (
                "Malecón de Miraflores",
                "Miraflores",
                2.4,
                [[-12.1198, -77.038], [-12.1253, -77.0368], [-12.132, -77.034]],
            ),
            (
                "Conexión San Isidro",
                "San Isidro",
                1.8,
                [[-12.098, -77.035], [-12.103, -77.033], [-12.109, -77.032]],
            ),
            (
                "Circuito Barranco",
                "Barranco",
                1.3,
                [[-12.14, -77.024], [-12.145, -77.021], [-12.15, -77.02]],
            ),
            (
                "Conexión Parque Kennedy",
                "Miraflores",
                1.1,
                [[-12.117, -77.029], [-12.121, -77.028], [-12.127, -77.026]],
            ),
        ]
        for name, district, length, geometry in rows:
            db.add(
                Cycleway(
                    name=name,
                    district=district,
                    length_km=length,
                    geometry=geometry,
                    source=source,
                    is_demo=True,
                )
            )
        for name, district, lat, lon in [
            ("Punto de estacionamiento A", "Miraflores", -12.122, -77.031),
            ("Punto de estacionamiento B", "San Isidro", -12.104, -77.034),
            ("Punto de estacionamiento C", "Barranco", -12.146, -77.023),
        ]:
            db.add(
                Parking(
                    name=name,
                    district=district,
                    latitude=lat,
                    longitude=lon,
                    address="Ubicación ilustrativa; no verificada",
                    source=source,
                    is_demo=True,
                )
            )
        db.commit()
    print("Se crearon 4 tramos y 3 estacionamientos de demostración; no hay usuarios de prueba.")


def main():
    parser = argparse.ArgumentParser(description="Operaciones de CicloLima")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("seed-demo")
    sub.add_parser("seed-showcase")
    promote = sub.add_parser("promote-moderator")
    promote.add_argument("email")
    args = parser.parse_args()
    if args.command == "seed-demo":
        seed_demo()
    elif args.command == "seed-showcase":
        from app.showcase import seed_showcase

        with SessionLocal() as db:
            print(seed_showcase(db))
    else:
        with SessionLocal() as db:
            user = db.scalar(select(User).where(User.email == args.email.lower()))
            if user is None:
                raise SystemExit("Primero registra la cuenta desde la aplicación.")
            user.role = "moderator"
            user.token_version += 1
            db.commit()
        print("Rol de moderador asignado. Debe iniciar sesión nuevamente.")


if __name__ == "__main__":
    main()
