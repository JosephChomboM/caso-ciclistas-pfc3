import { useCallback, useEffect, useState } from "react";
import {
  ArrowUpRight,
  Bike,
  MapPin,
  ParkingSquare,
  Route,
  Search,
} from "lucide-react";
import { api, type Cycleway, type Parking, type User } from "./api/client";
import Account from "./components/Account";
import { Moderation, ReportForm, ReportsList } from "./components/Reports";
import MapCanvas from "./components/MapCanvas";
import Recommendations from "./components/Recommendations";

export default function App() {
  const [user, setUser] = useState<User | null>(null);
  const [panel, setPanel] = useState<
    "account" | "report" | "moderation" | "recommendations" | null
  >(null);
  const [favorites, setFavorites] = useState<Parking[]>([]);
  const [onlyFavorites, setOnlyFavorites] = useState(false);
  const [notice, setNotice] = useState("");
  const [favoriteBusy, setFavoriteBusy] = useState(false);
  const [view, setView] = useState<"cycleways" | "parking">("cycleways");
  const [district, setDistrict] = useState("");
  const [condition, setCondition] = useState("");
  const [query, setQuery] = useState("");
  const [cycleways, setCycleways] = useState<Cycleway[]>([]);
  const [parking, setParking] = useState<Parking[]>([]);
  const [selected, setSelected] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [attempt, setAttempt] = useState(0);
  const select = useCallback((id: number) => setSelected(id), []);
  useEffect(() => {
    let active = true;
    if (!user) {
      setFavorites([]);
      setOnlyFavorites(false);
      return;
    }
    api<Parking[]>("/parking/favorites")
      .then((x) => {
        if (active) setFavorites(x);
      })
      .catch((e) => {
        if (active) setNotice(e.message);
      });
    return () => {
      active = false;
    };
  }, [user]);
  async function favorite(id: number) {
    if (!user) {
      setPanel("account");
      return;
    }
    setFavoriteBusy(true);
    setNotice("");
    try {
      const exists = favorites.some((x) => x.id === id);
      await api(`/parking/${id}/favorite`, {
        method: exists ? "DELETE" : "PUT",
      });
      setFavorites(await api<Parking[]>("/parking/favorites"));
      setNotice(
        exists ? "Retirado de tus favoritos." : "Guardado en tus favoritos.",
      );
    } catch (e) {
      setNotice(e instanceof Error ? e.message : "No se pudo guardar.");
    } finally {
      setFavoriteBusy(false);
    }
  }
  useEffect(() => {
    let active = true;
    setLoading(true);
    setError("");
    setSelected(null);
    Promise.all([api<Cycleway[]>("/cycleways"), api<Parking[]>("/parking")])
      .then(([routes, places]) => {
        if (active) {
          setCycleways(routes);
          setParking(places);
        }
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
  const routes = cycleways.filter(
    (x) =>
      (!district || x.district === district) &&
      (!condition || x.condition === condition) &&
      x.name.toLowerCase().includes(query.toLowerCase()),
  );
  const places = (onlyFavorites ? favorites : parking).filter(
    (x) =>
      (!district || x.district === district) &&
      x.name.toLowerCase().includes(query.toLowerCase()),
  );
  const rows = view === "cycleways" ? routes : places;
  return (
    <>
      <a className="skip-link" href="#main">
        Saltar al contenido
      </a>
      <header className="topbar">
        <a href="/" className="brand">
          <Bike size={30} strokeWidth={2} />
          CicloLima
        </a>
        <span className="brand-note">Tu ciudad, en bicicleta.</span>
        <nav className="account-nav" aria-label="Cuenta">
          <button onClick={() => setPanel(user ? "report" : "account")}>
            Reportar incidencia
          </button>
          <button onClick={() => setPanel("recommendations")}>
            Sugerencias
          </button>
          {user?.role === "moderator" && (
            <button onClick={() => setPanel("moderation")}>Moderar</button>
          )}
          <button onClick={() => setPanel("account")}>
            {user?.alias || "Ingresar"}
          </button>
        </nav>
      </header>
      <main id="main">
        <section className="intro">
          <div>
            <h1>Encuentra tu próximo recorrido.</h1>
            <p>
              Explora ciclovías y lugares para dejar tu bici. Consulta la
              información antes de salir.
            </p>
          </div>
          <div className="city-label">
            <MapPin size={18} /> Lima, Perú
          </div>
        </section>
        {notice && (
          <p role="status" className="notice">
            {notice}
          </p>
        )}
        {panel && (
          <div className="panel-wrap">
            <button onClick={() => setPanel(null)}>Volver al mapa</button>
            {panel === "recommendations" ? (
              <Recommendations
                districts={[
                  ...new Set(cycleways.map((x) => x.district)),
                ].sort()}
                onSelect={(route) => {
                  setView("cycleways");
                  setDistrict(route.district);
                  setQuery("");
                  setCondition("");
                  setSelected(route.id);
                  setPanel(null);
                }}
              />
            ) : panel === "account" ? (
              <Account
                user={user}
                onUser={(value) => {
                  setUser(value);
                  if (!user && value) setPanel(null);
                }}
              />
            ) : panel === "report" && user ? (
              <ReportForm cycleways={cycleways} />
            ) : panel === "moderation" && user?.role === "moderator" ? (
              <Moderation />
            ) : (
              <p>Inicia sesión para continuar.</p>
            )}
          </div>
        )}
        <div hidden={panel !== null}>
          <div className="workspace">
            <section className="explorer" aria-label="Explorar lugares">
              <nav className="tabs" aria-label="Tipo de consulta">
                <button
                  aria-pressed={view === "cycleways"}
                  onClick={() => {
                    setView("cycleways");
                    setSelected(null);
                  }}
                >
                  <Route size={18} />
                  Ciclovías
                </button>
                <button
                  aria-pressed={view === "parking"}
                  onClick={() => {
                    setView("parking");
                    setSelected(null);
                  }}
                >
                  <ParkingSquare size={18} />
                  Estacionamientos
                </button>
              </nav>
              <div className="filters">
                <label className="search">
                  <Search size={18} />
                  <span className="sr-only">Buscar por nombre</span>
                  <input
                    placeholder="Busca un lugar o recorrido"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                  />
                </label>
                <div className="filter-row">
                  <label>
                    Distrito
                    <select
                      value={district}
                      onChange={(e) => {
                        setDistrict(e.target.value);
                        setSelected(null);
                      }}
                    >
                      <option value="">Todos los distritos</option>
                      {[
                        ...new Set(
                          [...cycleways, ...parking].map((x) => x.district),
                        ),
                      ]
                        .sort()
                        .map((x) => (
                          <option key={x}>{x}</option>
                        ))}
                    </select>
                  </label>
                  {view === "cycleways" && (
                    <label>
                      Condición
                      <select
                        value={condition}
                        onChange={(e) => setCondition(e.target.value)}
                      >
                        <option value="">Todas</option>
                        {[...new Set(cycleways.map((x) => x.condition))]
                          .sort()
                          .map((x) => (
                            <option key={x}>{x}</option>
                          ))}
                      </select>
                    </label>
                  )}
                </div>
              </div>
              {view === "parking" && user && (
                <label className="favorite-filter">
                  <input
                    type="checkbox"
                    checked={onlyFavorites}
                    onChange={(e) => setOnlyFavorites(e.target.checked)}
                  />
                  Solo mis favoritos
                </label>
              )}
              <div className="result-heading">
                <h2>
                  {view === "cycleways" ? "Ciclovías" : "Estacionamientos"}
                </h2>
                <span>{rows.length} resultados</span>
              </div>
              {loading ? (
                <p role="status" className="state">
                  Cargando lugares…
                </p>
              ) : error ? (
                <div role="alert" className="state">
                  <p>{error}</p>
                  <button onClick={() => setAttempt((x) => x + 1)}>
                    Reintentar
                  </button>
                </div>
              ) : rows.length === 0 ? (
                <div className="state">
                  <h3>No encontramos coincidencias</h3>
                  <p>Prueba otro distrito o borra los filtros.</p>
                  <button
                    onClick={() => {
                      setDistrict("");
                      setCondition("");
                      setQuery("");
                      setOnlyFavorites(false);
                    }}
                  >
                    Limpiar filtros
                  </button>
                </div>
              ) : (
                <ul className="results">
                  {rows.map((row) => (
                    <li
                      key={row.id}
                      className={selected === row.id ? "selected" : ""}
                    >
                      <button
                        className="result-button"
                        onClick={() => setSelected(row.id)}
                        aria-expanded={selected === row.id}
                      >
                        <span className="result-icon">
                          {view === "cycleways" ? (
                            <Route size={21} />
                          ) : (
                            <ParkingSquare size={21} />
                          )}
                        </span>
                        <span>
                          <strong>{row.name}</strong>
                          <small>
                            {row.district}
                            {"length_km" in row
                              ? ` · ${row.length_km.toLocaleString("es-PE")} km`
                              : " · Estacionamiento"}
                          </small>
                        </span>
                        <ArrowUpRight size={18} />
                      </button>
                      {selected === row.id && (
                        <div className="detail">
                          <p>
                            {"condition" in row
                              ? `Condición: ${row.condition}. Sin información suficiente para asegurar la seguridad del recorrido.`
                              : `${row.address}. Horario: ${row.hours}. Sujeción: ${row.rack_type}.`}
                          </p>
                          <p className="source">
                            {row.source}
                            <br />
                            Actualizado:{" "}
                            {new Date(row.updated_at).toLocaleDateString(
                              "es-PE",
                            )}
                          </p>
                          {"condition" in row ? (
                            <ReportsList cyclewayId={row.id} />
                          ) : (
                            <button
                              className="favorite-button"
                              disabled={favoriteBusy}
                              onClick={() => favorite(row.id)}
                            >
                              {favorites.some((x) => x.id === row.id)
                                ? "Quitar de favoritos"
                                : "Guardar en favoritos"}
                            </button>
                          )}
                        </div>
                      )}
                    </li>
                  ))}
                </ul>
              )}
              <p className="list-foot">
                La ausencia de reportes no significa que un tramo sea seguro.
              </p>
            </section>
            <MapCanvas
              cycleways={view === "cycleways" ? routes : []}
              parking={view === "parking" ? places : []}
              selected={selected}
              onSelect={select}
            />
          </div>
        </div>
      </main>
      <footer className="site-footer">
        <div>
          <a href="#main" className="footer-brand">
            <Bike size={24} /> CicloLima
          </a>
          <p>Conoce los recorridos. Comparte lo que encuentras.</p>
          <small>Proyecto académico de Joseph Chombo Morocho.</small>
        </div>
        <nav aria-label="Enlaces del proyecto">
          <a href="#main">Explorar el mapa</a>
          <a
            href="https://github.com/JosephChomboM/caso-ciclistas-pfc3"
            target="_blank"
            rel="noreferrer"
          >
            Código del proyecto <ArrowUpRight size={15} />
          </a>
          <a
            href="https://github.com/JosephChomboM"
            target="_blank"
            rel="noreferrer"
          >
            <ArrowUpRight size={18} /> GitHub de Joseph
          </a>
        </nav>
        <details>
          <summary>Datos y alcance</summary>
          <p>
            El catálogo académico contiene ejemplos ilustrativos. Cada lugar
            muestra su fuente y actualización. Las sugerencias no certifican
            seguridad vial.
          </p>
        </details>
      </footer>
    </>
  );
}
