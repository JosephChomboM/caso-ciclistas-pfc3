import { useEffect, useState, type FormEvent } from "react";
import { api, type Cycleway, type Report } from "../api/client";

export function ReportForm({ cycleways }: { cycleways: Cycleway[] }) {
  const [selected, setSelected] = useState(String(cycleways[0]?.id || ""));
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");
  const route = cycleways.find((x) => String(x.id) === selected);
  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setBusy(true);
    setMessage("");
    const form = new FormData(event.currentTarget);
    try {
      await api("/reports", {
        method: "POST",
        body: JSON.stringify({
          cycleway_id: Number(selected),
          category: form.get("category"),
          description: form.get("description"),
          latitude: Number(form.get("latitude")),
          longitude: Number(form.get("longitude")),
        }),
      });
      setMessage(
        "Recibimos tu reporte. Se publicará después de la revisión de un moderador.",
      );
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "No se pudo enviar.");
    } finally {
      setBusy(false);
    }
  }
  return (
    <section className="form-panel">
      <h2>Comparte lo que encontraste</h2>
      <p>
        Describe el problema sin incluir datos personales. El reporte pasará por
        revisión antes de aparecer públicamente.
      </p>
      <form onSubmit={submit}>
        <label>
          Tramo
          <select
            required
            value={selected}
            onChange={(e) => setSelected(e.target.value)}
          >
            {cycleways.map((x) => (
              <option key={x.id} value={x.id}>
                {x.name}
              </option>
            ))}
          </select>
        </label>
        <label>
          Categoría
          <select name="category">
            {["Obstáculo", "Vía deteriorada", "Incidente", "Señalización"].map(
              (x) => (
                <option key={x}>{x}</option>
              ),
            )}
          </select>
        </label>
        <label>
          Qué ocurrió
          <textarea
            name="description"
            required
            minLength={10}
            maxLength={1000}
            rows={4}
            placeholder="Cuéntanos qué ocurrió y en qué parte del tramo."
          />
        </label>
        <div className="coordinate-fields" key={selected}>
          <label>
            Latitud
            <input
              name="latitude"
              type="number"
              step="any"
              min={-12.5}
              max={-11.5}
              required
              defaultValue={route?.geometry[0]?.[0]}
            />
          </label>
          <label>
            Longitud
            <input
              name="longitude"
              type="number"
              step="any"
              min={-77.5}
              max={-76.5}
              required
              defaultValue={route?.geometry[0]?.[1]}
            />
          </label>
        </div>
        <small>
          Las coordenadas iniciales corresponden al primer punto del tramo.
          Ajústalas a la ubicación del incidente.
        </small>
        {message && (
          <p role="status" className="form-message">
            {message}
          </p>
        )}
        <button className="primary" disabled={busy || !selected}>
          {busy ? "Enviando…" : "Enviar a revisión"}
        </button>
      </form>
    </section>
  );
}

export function ReportsList({ cyclewayId }: { cyclewayId: number }) {
  const [rows, setRows] = useState<Report[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    let active = true;
    api<Report[]>(`/reports?cycleway_id=${cyclewayId}`)
      .then((x) => {
        if (active) setRows(x);
      })
      .catch((e) => {
        if (active) setError(e.message);
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [cyclewayId]);
  return (
    <section className="public-reports">
      <h3>Reportes publicados</h3>
      {loading ? (
        <p role="status">Consultando reportes…</p>
      ) : error ? (
        <p role="alert">{error}</p>
      ) : rows.length ? (
        rows.map((x) => (
          <article key={x.id}>
            <strong>{x.category}</strong>
            <p>{x.description}</p>
            <small>
              {new Date(x.created_at).toLocaleDateString("es-PE")} · Aporte
              ciudadano
            </small>
          </article>
        ))
      ) : (
        <p>Aún no hay reportes publicados para este tramo.</p>
      )}
    </section>
  );
}

export function Moderation() {
  const [rows, setRows] = useState<Report[]>([]);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [loading, setLoading] = useState(true);
  const [attempt, setAttempt] = useState(0);
  useEffect(() => {
    let active = true;
    setLoading(true);
    setError("");
    api<Report[]>("/reports/pending")
      .then((x) => {
        if (active) setRows(x);
      })
      .catch((e) => {
        if (active) setError(e.message);
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [attempt]);
  async function decide(id: number, status: string) {
    setBusy(true);
    setError("");
    try {
      await api(`/reports/${id}/moderate`, {
        method: "PATCH",
        body: JSON.stringify({ status }),
      });
      setRows(rows.filter((x) => x.id !== id));
    } catch (e) {
      setError(e instanceof Error ? e.message : "No se pudo revisar.");
    } finally {
      setBusy(false);
    }
  }
  return (
    <section className="form-panel">
      <h2>Reportes por revisar</h2>
      <p>
        Publicar un reporte lo hace visible como aporte ciudadano; no lo
        certifica como información oficial.
      </p>
      {error && (
        <div role="alert">
          <p>{error}</p>
          <button onClick={() => setAttempt((x) => x + 1)}>
            Reintentar consulta
          </button>
        </div>
      )}
      {loading ? (
        <p role="status">Cargando reportes…</p>
      ) : rows.length === 0 && !error ? (
        <p>No hay reportes pendientes.</p>
      ) : (
        rows.map((x) => (
          <article className="review-report" key={x.id}>
            <h3>{x.category}</h3>
            <p>{x.description}</p>
            <p>
              Tramo {x.cycleway_id} · {x.latitude}, {x.longitude}
            </p>
            <div className="actions">
              <button disabled={busy} onClick={() => decide(x.id, "published")}>
                Publicar
              </button>
              <button disabled={busy} onClick={() => decide(x.id, "rejected")}>
                Rechazar
              </button>
            </div>
          </article>
        ))
      )}
    </section>
  );
}
