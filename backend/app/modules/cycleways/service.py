from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.cycleways import repository
from app.modules.cycleways.schemas import CyclewayOut, RecommendationOut
from app.modules.reports import service as reports


def list_cycleways(db: Session, district: str | None, condition: str | None) -> list[CyclewayOut]:
    return [
        CyclewayOut.model_validate(x) for x in repository.list_cycleways(db, district, condition)
    ]


def get(db: Session, cycleway_id: int) -> CyclewayOut:
    row = repository.get(db, cycleway_id)
    if row is None:
        raise HTTPException(404, "No se encontró ese tramo")
    return CyclewayOut.model_validate(row)


def recommend(db: Session, district: str | None, target_km: float) -> list[RecommendationOut]:
    counts = reports.published_counts(db)
    suggestions = []
    for route in repository.list_cycleways(db, district, None):
        count = counts.get(route.id, 0)
        distance_penalty = min(abs(route.length_km - target_km) / target_km * 60, 90)
        score = round(max(0, 100 - distance_penalty - min(count * 10, 30)), 1)
        reasons = [
            f"Longitud de {route.length_km:g} km frente a tu objetivo de {target_km:g} km.",
            f"{count} reporte(s) publicados; cada reporte reduce 10 puntos, hasta 30.",
            "Sin reportes no equivale a seguro. Revisa el detalle antes de salir.",
        ]
        if route.is_demo:
            reasons.append("Registro académico ilustrativo, sin verificación de campo.")
        suggestions.append(
            RecommendationOut(
                cycleway=CyclewayOut.model_validate(route),
                match_score=score,
                published_reports=count,
                reasons=reasons,
            )
        )
    return sorted(suggestions, key=lambda x: (-x.match_score, x.cycleway.id))[:3]
