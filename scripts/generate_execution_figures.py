"""Render observed Jira events; never synthesize or redistribute transitions.

Run with Python 3.11+ and matplotlib installed. Input is a sanitized Jira export.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "docs/evidence/jira-execution.json").read_text())
OUT = ROOT / "docs/figures"
TZ = ZoneInfo("America/Lima")
ISSUES = {item["key"]: item for item in DATA["issues"]}
HISTORY = {item["key"]: item["events"] for item in DATA["histories"]}
COLORS = ["#27664b", "#326e99", "#a35e3f", "#755a93"]


def instant(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(TZ)


def transitions(key):
    return sorted(
        [event for event in HISTORY.get(key, []) if event["field"] == "status"],
        key=lambda event: instant(event["at"]),
    )


def status_at(key, at):
    events = transitions(key)
    state = events[0]["from"] if events else ISSUES[key]["status"]
    for event in events:
        if instant(event["at"]) <= at:
            state = event["to"]
    return state


def observed(sprint_record, use_points=False):
    sprint = sprint_record["sprint"]
    start, end = instant(sprint["startDate"]), instant(sprint["endDate"])
    keys = [key for key in sprint_record["issue_keys"] if status_at(key, start) != "Done"]
    # Scope and estimates were fixed before these windows; preserve that baseline.
    weight = {key: ISSUES[key]["points"] if use_points else 1 for key in keys}
    remaining = sum(weight.values())
    times, values = [start], [remaining]
    events = sorted(
        [(instant(event["at"]), key, event) for key in keys for event in transitions(key)
         if start < instant(event["at"]) <= end], key=lambda item: item[0]
    )
    for at, key, event in events:
        was_done, is_done = event["from"] == "Done", event["to"] == "Done"
        remaining += weight[key] * (int(was_done) - int(is_done))
        if was_done != is_done:
            times.append(at)
            values.append(remaining)
    times.append(end)
    values.append(remaining)
    return times, values


def burndowns():
    fig, axes = plt.subplots(2, 2, figsize=(14, 8), constrained_layout=True)
    velocity = []
    for index, (record, ax) in enumerate(zip(DATA["sprints"], axes.flat)):
        times, values = observed(record)
        ax.plot([times[0], times[-1]], [values[0], 0], color="#a6acb3", label="Ideal")
        ax.step(times, values, where="post", color=COLORS[index], linewidth=2, label="Observado")
        ax.set(title=f"Sprint {index + 1} · {record['sprint']['state']}", ylabel="Historias restantes")
        ax.set_ylim(bottom=0)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M", tz=TZ))
        ax.grid(alpha=0.15)
        ax.legend()
        _, points = observed(record, use_points=True)
        velocity.append(points[0] - points[-1])
    fig.suptitle("CicloLima · curvas derivadas del historial real de Jira\nVentanas académicas de una hora · hora de Lima", fontsize=15)
    fig.savefig(OUT / "burndowns-jira-observados.png", dpi=160)
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(13, 4), constrained_layout=True)
    times, points = observed(DATA["sprints"][3], use_points=True)
    axes[0].plot([times[0], times[-1]], [points[0], 0], color="#a6acb3", label="Ideal")
    axes[0].step(times, points, where="post", color=COLORS[0], label="Observado", linewidth=2)
    axes[0].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M", tz=TZ))
    axes[0].set(title="Sprint 4 · línea base replanificada de 7 SP", ylabel="SP restantes", ylim=(0, 7.5))
    axes[0].legend()
    axes[1].bar(["S1", "S2", "S3", "S4*"], velocity, color=COLORS)
    axes[1].set(title="SP aceptados dentro de cada ventana", ylabel="SP", ylim=(0, 15))
    for index, value in enumerate(velocity):
        axes[1].text(index, value + 0.3, str(value), ha="center")
    fig.suptitle("*Sprint 4 activo: velocidad provisional. Sus 13 SP previos quedan fuera de esta ventana.")
    fig.savefig(OUT / "velocidad-y-sprint4.png", dpi=160)
    plt.close(fig)


def gantt():
    rows = []
    for epic in [item for item in DATA["issues"] if item["type"] == "Epic"]:
        rows.append(epic)
        rows.extend(sorted([item for item in DATA["issues"] if item["parent"] == epic["key"]],
                           key=lambda item: (item["start"], item["key"])))
    fig, ax = plt.subplots(figsize=(15, 12), constrained_layout=True)
    positions = {item["key"]: index for index, item in enumerate(rows)}
    for index, item in enumerate(rows):
        start, end = datetime.fromisoformat(item["start"]), datetime.fromisoformat(item["end"])
        epic_number = int((item["key"] if item["type"] == "Epic" else item["parent"]).split("-")[1])
        color = COLORS[epic_number - 1]
        if item["type"] == "Task":
            ax.scatter(start, index, marker="D", color=color, s=50)
        else:
            ax.barh(index, (end - start).days + 1, left=mdates.date2num(start), color=color,
                    height=0.65 if item["type"] == "Epic" else 0.4, alpha=0.85)
    for source, target in DATA["dependencies"]:
        if source in positions and target in positions:
            end = datetime.fromisoformat(ISSUES[source]["end"]) + timedelta(days=1)
            start = datetime.fromisoformat(ISSUES[target]["start"])
            ax.annotate("", xy=(mdates.date2num(start), positions[target]),
                        xytext=(mdates.date2num(end), positions[source]),
                        arrowprops={"arrowstyle": "->", "color": "#7b8588", "alpha": 0.4, "lw": 0.8})
    ax.set_yticks(range(len(rows)), [f"{item['key']} · {item['title']}" for item in rows], fontsize=8)
    ax.invert_yaxis()
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    ax.grid(axis="x", alpha=0.15)
    ax.set_title("CicloLima · calendario académico propuesto 2026\n4 épicas, 16 historias, 4 hitos (rombos) y dependencias Blocks de Jira")
    fig.savefig(OUT / "gantt-epicas-historias.png", dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    burndowns()
    gantt()
    print("Se generaron tres figuras desde el historial exportado de Jira.")
