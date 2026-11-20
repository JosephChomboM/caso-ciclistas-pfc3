from app.modules.reports.models import Report
from app.showcase import seed_showcase


def test_recommendations_explain_results_and_ignore_private_reports(client, db):
    seed_showcase(db)
    url = "/api/cycleways/recommendations?district=Miraflores&target_km=2.4"
    before = client.get(url).json()
    assert len(before) == 3
    assert all(x["cycleway"]["district"] == "Miraflores" for x in before)
    assert [x["match_score"] for x in before] == sorted(
        [x["match_score"] for x in before], reverse=True
    )
    winner = before[0]["cycleway"]["id"]
    report = Report(
        user_id=1,
        cycleway_id=winner,
        category="Obstáculo",
        status="pending",
        description="Información pendiente que no puede afectar sugerencias públicas",
        latitude=-12.1,
        longitude=-77,
    )
    db.add(report)
    db.commit()
    assert client.get(url).json() == before
    report.status = "published"
    db.commit()
    after = client.get(url).json()
    match = next(x for x in after if x["cycleway"]["id"] == winner)
    assert match["published_reports"] == before[0]["published_reports"] + 1
    assert match["match_score"] < before[0]["match_score"]
    assert any("académico" in text for text in match["reasons"])
    assert "user_id" not in str(after)
    assert client.get("/api/cycleways/recommendations?target_km=nan").status_code == 422
    assert client.get("/api/cycleways/recommendations?target_km=0").status_code == 422
    assert client.get("/api/cycleways/recommendations?district=Otro").json() == []
