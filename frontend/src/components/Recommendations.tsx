import { useState, type FormEvent } from "react";
import { ArrowUpRight } from "lucide-react";
import { api, type Cycleway } from "../api/client";

type Suggestion = {
  cycleway: Cycleway;
  match_score: number;
  published_reports: number;
  reasons: string[];
};

export default function Recommendations({
  districts,
  onSelect,
}: {
  districts: string[];
  onSelect: (route: Cycleway) => void;
}) {
  const [results, setResults] = useState<Suggestion[] | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const params = new URLSearchParams({
      target_km: String(form.get("distance")),
    });
    if (form.get("district"))
      params.set("district", String(form.get("district")));
    setBusy(true);
    setError("");
    setResults(null);
    try {
      setResults(
        await api<Suggestion[]>(`/cycleways/recommendations?${params}`),
      );
    } catch (e) {
      setError(
        e instanceof Error
          ? e.message
          : "No se pudo comparar. Inténtalo otra vez.",
      );
    } finally {
      setBusy(false);
    }
  }
  return (
    <section className="form-panel suggestions-panel">
      <h2>Un recorrido a tu medida</h2>
      <p>
        Compara tramos según la distancia que buscas y sus reportes publicados.
        Las sugerencias explican cada criterio; no certifican seguridad vial.
      </p>
      <form onSubmit={submit}>
        <div className="coordinate-fields">
          <label>
            Distrito
            <select name="district">
              <option value="">Todos los distritos</option>
              {districts.map((x) => (
                <option key={x}>{x}</option>
              ))}
            </select>
          </label>
          <label>
            Distancia objetivo en km
            <input
              name="distance"
              type="number"
              min="0.5"
              max="20"
              step="0.1"
              defaultValue="3"
              required
            />
          </label>
        </div>
        <button className="primary" disabled={busy}>
          {busy ? "Comparando recorridos…" : "Encontrar sugerencias"}
        </button>
      </form>
      {error && (
        <p role="alert" className="form-message">
          {error}
        </p>
      )}
      {results?.length === 0 && (
        <p role="status">
          No hay tramos para ese distrito. Prueba con todos los distritos.
        </p>
      )}
      {results && results.length > 0 && (
        <ol className="suggestions">
          {results.map((result) => (
            <li key={result.cycleway.id}>
              <div className="suggestion-heading">
                <h3>{result.cycleway.name}</h3>
                <span>
                  Afinidad {result.match_score.toLocaleString("es-PE")}/100
                </span>
              </div>
              <p>
                {result.cycleway.district} · {result.cycleway.length_km} km
              </p>
              <ul>
                {result.reasons.map((reason) => (
                  <li key={reason}>{reason}</li>
                ))}
              </ul>
              <button onClick={() => onSelect(result.cycleway)}>
                Ver en el mapa <ArrowUpRight size={16} />
              </button>
            </li>
          ))}
        </ol>
      )}
    </section>
  );
}
