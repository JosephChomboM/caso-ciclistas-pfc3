"""Figuras del escenario académico; no representan historial exportado de Jira."""

import json
from datetime import datetime, timedelta
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "figures"
OUT.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
green, orange = "#164c3d", "#a04320"
sprints = [
    {"name": "Sprint 1", "stories": ["PCC-5", "PCC-6", "PCC-8"],
     "points": [3, 5, 5], "done_days": [2, 4, 5]},
    {"name": "Sprint 2", "stories": ["PCC-9", "PCC-10", "PCC-11"],
     "points": [3, 5, 5], "done_days": [1, 3, 5]},
    {"name": "Sprint 3", "stories": ["PCC-13", "PCC-12", "PCC-14"],
     "points": [5, 3, 5], "done_days": [3, 4, 5]},
    {"name": "Sprint 4", "stories": ["PCC-7", "PCC-15", "PCC-16"],
     "points": [5, 3, 5], "done_days": [2, 3, 5]},
]
fig, axes = plt.subplots(2, 2, figsize=(10, 6.8), constrained_layout=True)
for ax, sprint in zip(axes.flat, sprints):
    counts = [sum(day < done for done in sprint["done_days"]) for day in range(6)]
    points = [sum(p for p, done in zip(sprint["points"], sprint["done_days"]) if day < done)
              for day in range(6)]
    sprint["remaining_stories"], sprint["remaining_points"] = counts, points
    ax.plot(range(6), [3 * (1 - d / 5) for d in range(6)], "--", color="#77827b", label="Ideal")
    ax.step(range(6), counts, where="post", color=green, linewidth=2, label="Escenario simulado")
    ax.scatter(range(6), counts, color=green, s=22)
    ax.set(title=sprint["name"] + " · 13 SP simulados aceptados", xlabel="Día", ylabel="Historias pendientes",
           xticks=range(6), yticks=range(4), ylim=(-.15, 3.25))
    ax.grid(axis="y", alpha=.18)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(fontsize=8)
fig.suptitle("Burndown de historias · simulación académica", fontsize=15, fontweight="bold")
fig.savefig(OUT / "burndowns-simulados.png", dpi=180)
plt.close(fig)
(OUT / "sprint-simulation.json").write_text(json.dumps({
    "kind": "escenario_academico_no_historial_jira", "days": list(range(6)), "sprints": sprints,
}, ensure_ascii=False, indent=2) + "\n")

tasks = [
    ("PCC-5 Registro", "2026-11-23", "2026-11-24", green),
    ("PCC-6 Sesión", "2026-11-25", "2026-11-27", green),
    ("PCC-8 Mapa", "2026-11-23", "2026-11-27", "#326d98"),
    ("PCC-9 Filtros", "2026-11-30", "2026-12-01", "#326d98"),
    ("PCC-10 Detalle tramo", "2026-11-30", "2026-12-02", "#326d98"),
    ("PCC-11 Reporte", "2026-12-03", "2026-12-04", orange),
    ("PCC-13 Moderación", "2026-12-07", "2026-12-09", orange),
    ("PCC-12 Consulta reportes", "2026-12-10", "2026-12-11", orange),
    ("PCC-14 Estacionamientos", "2026-12-07", "2026-12-09", "#706198"),
    ("PCC-7 Perfil", "2026-12-14", "2026-12-16", green),
    ("PCC-15 Detalle lugar", "2026-12-14", "2026-12-16", "#706198"),
    ("PCC-16 Favoritos", "2026-12-17", "2026-12-18", "#706198"),
]
fig, ax = plt.subplots(figsize=(10, 6.2), constrained_layout=True)
for i, (name, start, end, color) in enumerate(tasks):
    a, b = [datetime.fromisoformat(x) for x in (start, end)]
    ax.barh(i, (b - a).days + 1, left=mdates.date2num(a), height=.55, color=color)
for previous, following in [(0, 1), (2, 3), (2, 4), (1, 5), (4, 5), (5, 6), (6, 7), (8, 10), (8, 11), (1, 11)]:
    end = mdates.date2num(datetime.fromisoformat(tasks[previous][2])) + 1
    start = mdates.date2num(datetime.fromisoformat(tasks[following][1]))
    middle = (end + start) / 2
    ax.plot([end, middle, middle, start], [previous, previous, following, following],
            color="#8a928e", linewidth=.65)
    ax.annotate("", (start, following), (start, following - .25),
                arrowprops={"arrowstyle": "->", "color": "#8a928e", "lw": .65})
for date in ["2026-11-27", "2026-12-04", "2026-12-11", "2026-12-18"]:
    ax.axvline(mdates.date2num(datetime.fromisoformat(date)) + .85, color="#a5aea8", linestyle=":", lw=.8)
ax.set_yticks(range(len(tasks)), [x[0] for x in tasks])
ax.invert_yaxis()
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
ax.set(title="Gantt propuesto · fechas y dependencias académicas", xlabel="Hitos al cierre de cada sprint: 27 nov, 4 dic, 11 dic y 18 dic de 2026")
ax.spines[["top", "right"]].set_visible(False)
fig.savefig(OUT / "gantt-planificado.png", dpi=180)
plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 5.8), constrained_layout=True)
ax.set(xlim=(0, 10), ylim=(0, 7)); ax.axis("off")
def box(x, y, w, label, color="#e4eddd"):
    ax.add_patch(Rectangle((x, y), w, .8, facecolor=color, edgecolor=green, lw=1))
    ax.text(x + w / 2, y + .4, label, ha="center", va="center", fontsize=10)
def arrow(a, b, label=""):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="->", mutation_scale=12, color=green, lw=1.2))
    if label: ax.text((a[0]+b[0])/2+.08, (a[1]+b[1])/2, label, fontsize=8)
box(3.2, 6.0, 3.6, "Ciclista o moderador")
box(3.2, 4.8, 3.6, "Frontend React y TypeScript")
box(.1, 4.8, 2.3, "Teselas OpenStreetMap", "#e3edf5")
box(3.2, 3.6, 3.6, "API FastAPI · JWT y permisos")
arrow((5, 6), (5, 5.6)); arrow((5, 4.8), (5, 4.4), "HTTPS JSON")
arrow((3.2, 5.2), (2.4, 5.2))
for x, label in [(0, "Usuarios"), (2.55, "Ciclovías"), (5.1, "Reportes"), (7.65, "Estacionamientos")]:
    box(x, 2.1, 2.3, label)
    arrow((5, 3.6), (x + 1.15, 2.9))
    arrow((x + 1.15, 2.1), (5, 1.2))
box(2.1, .4, 5.8, "PostgreSQL · esquema privado ciclolima\nSupabase separado para stage y producción", "#e3edf5")
ax.set_title("Arquitectura lógica de CicloLima", fontsize=15, fontweight="bold", pad=14)
fig.savefig(OUT / "arquitectura.png", dpi=180)
plt.close(fig)
print("Se generaron burndowns, Gantt, arquitectura y series del escenario académico.")
