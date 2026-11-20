import { useCallback, useEffect, useState } from 'react'
import { ArrowUpRight, Bike, MapPin, ParkingSquare, Route, Search } from 'lucide-react'
import { api, type Cycleway, type Parking } from './api/client'
import MapCanvas from './components/MapCanvas'

export default function App() {
  const [view, setView] = useState<'cycleways' | 'parking'>('cycleways')
  const [district, setDistrict] = useState('')
  const [condition, setCondition] = useState('')
  const [query, setQuery] = useState('')
  const [cycleways, setCycleways] = useState<Cycleway[]>([])
  const [parking, setParking] = useState<Parking[]>([])
  const [selected, setSelected] = useState<number | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [attempt, setAttempt] = useState(0)
  const select = useCallback((id: number) => setSelected(id), [])
  useEffect(() => {
    let active = true
    setLoading(true); setError(''); setSelected(null)
    Promise.all([api<Cycleway[]>('/cycleways'), api<Parking[]>('/parking')])
      .then(([routes, places]) => { if (active) { setCycleways(routes); setParking(places) } })
      .catch(e => { if (active) setError(e.message) })
      .finally(() => { if (active) setLoading(false) })
    return () => { active = false }
  }, [attempt])
  const routes = cycleways.filter(x => (!district || x.district === district)
    && (!condition || x.condition === condition) && x.name.toLowerCase().includes(query.toLowerCase()))
  const places = parking.filter(x => (!district || x.district === district)
    && x.name.toLowerCase().includes(query.toLowerCase()))
  const rows = view === 'cycleways' ? routes : places
  const hasDemo = [...cycleways, ...parking].some(x => x.is_demo)
  return <>
    <a className="skip-link" href="#main">Saltar al contenido</a>
    <header className="topbar"><a href="/" className="brand"><Bike size={30} strokeWidth={2} />CicloLima</a>
      <span className="brand-note">Tu ciudad, en bicicleta.</span><a className="text-link" href="https://github.com/JosephChomboM/caso-ciclistas-pfc3" target="_blank" rel="noreferrer">Sobre el proyecto <ArrowUpRight size={15} /></a>
    </header>
    <main id="main">
      <section className="intro"><div><h1>Encuentra tu próximo recorrido.</h1><p>Explora ciclovías y lugares para dejar tu bici. Consulta la información antes de salir.</p></div>
        <div className="city-label"><MapPin size={18} /> Lima, Perú</div>
      </section>
      {hasDemo && <p className="demo-note">Estás explorando datos de demostración. Los trazados y ubicaciones son ilustrativos y no acreditan condiciones reales.</p>}
      <div className="workspace">
        <section className="explorer" aria-label="Explorar lugares">
          <nav className="tabs" aria-label="Tipo de consulta">
            <button aria-pressed={view === 'cycleways'} onClick={() => { setView('cycleways'); setSelected(null) }}><Route size={18} />Ciclovías</button>
            <button aria-pressed={view === 'parking'} onClick={() => { setView('parking'); setSelected(null) }}><ParkingSquare size={18} />Estacionamientos</button>
          </nav>
          <div className="filters"><label className="search"><Search size={18} /><span className="sr-only">Buscar por nombre</span><input placeholder="Busca un lugar o recorrido" value={query} onChange={e => setQuery(e.target.value)} /></label>
            <div className="filter-row"><label>Distrito<select value={district} onChange={e => { setDistrict(e.target.value); setSelected(null) }}><option value="">Todos los distritos</option>{['Miraflores', 'San Isidro', 'Barranco'].map(x => <option key={x}>{x}</option>)}</select></label>
              {view === 'cycleways' && <label>Condición<select value={condition} onChange={e => setCondition(e.target.value)}><option value="">Todas</option><option>Sin verificar</option></select></label>}
            </div>
          </div>
          <div className="result-heading"><h2>{view === 'cycleways' ? 'Ciclovías' : 'Estacionamientos'}</h2><span>{rows.length} resultados</span></div>
          {loading ? <p role="status" className="state">Cargando lugares…</p> : error ? <div role="alert" className="state"><p>{error}</p><button onClick={() => setAttempt(x => x + 1)}>Reintentar</button></div> : rows.length === 0 ? <div className="state"><h3>No encontramos coincidencias</h3><p>Prueba otro distrito o borra los filtros.</p><button onClick={() => { setDistrict(''); setCondition(''); setQuery('') }}>Limpiar filtros</button></div> :
            <ul className="results">{rows.map(row => <li key={row.id} className={selected === row.id ? 'selected' : ''}>
              <button className="result-button" onClick={() => setSelected(row.id)} aria-expanded={selected === row.id}>
                <span className="result-icon">{view === 'cycleways' ? <Route size={21} /> : <ParkingSquare size={21} />}</span><span><strong>{row.name}</strong><small>{row.district}{'length_km' in row ? ` · ${row.length_km.toLocaleString('es-PE')} km` : ' · Estacionamiento'}</small></span><ArrowUpRight size={18} />
              </button>
              {selected === row.id && <div className="detail"><p>{'condition' in row ? `Condición: ${row.condition}. Sin información suficiente para asegurar la seguridad del recorrido.` : `${row.address}. Horario: ${row.hours}. Sujeción: ${row.rack_type}.`}</p><p className="source">{row.source}<br />Actualizado: {new Date(row.updated_at).toLocaleDateString('es-PE')}</p></div>}
            </li>)}</ul>}
          <p className="list-foot">La ausencia de reportes no significa que un tramo sea seguro.</p>
        </section>
        <MapCanvas cycleways={view === 'cycleways' ? routes : []} parking={view === 'parking' ? places : []} selected={selected} onSelect={select} />
      </div>
    </main>
    <footer><span>CicloLima · Proyecto académico</span><span>Consulta. Planifica. Pedalea.</span></footer>
  </>
}
