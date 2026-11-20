import { useEffect, useRef, useState } from 'react'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import type { Cycleway, Parking } from '../api/client'

export default function MapCanvas({ cycleways, parking, selected, onSelect }: {
  cycleways: Cycleway[]; parking: Parking[]; selected: number | null; onSelect: (id: number) => void
}) {
  const element = useRef<HTMLDivElement>(null)
  const map = useRef<L.Map | null>(null)
  const [tileError, setTileError] = useState(false)
  useEffect(() => {
    if (!element.current) return
    const instance = L.map(element.current, { zoomControl: false }).setView([-12.122, -77.031], 13)
    map.current = instance
    L.control.zoom({ position: 'bottomright' }).addTo(instance)
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      maxZoom: 19,
    }).on('tileerror', () => setTileError(true)).addTo(instance)
    const observer = new ResizeObserver(() => instance.invalidateSize())
    observer.observe(element.current)
    return () => { observer.disconnect(); instance.remove(); map.current = null }
  }, [])
  useEffect(() => {
    if (!map.current) return
    const layer = L.layerGroup().addTo(map.current)
    for (const row of cycleways) {
      const line = L.polyline(row.geometry, { color: selected === row.id ? '#a04320' : '#217257',
        weight: selected === row.id ? 8 : 5, opacity: .95 }).addTo(layer)
      const label = document.createElement('span'); label.textContent = row.name
      line.bindTooltip(label).on('click', () => onSelect(row.id))
    }
    for (const row of parking) {
      const marker = L.circleMarker([row.latitude, row.longitude], { color: '#fff',
        fillColor: selected === row.id ? '#a04320' : '#245e96', radius: 10, fillOpacity: 1, weight: 3 }).addTo(layer)
      const label = document.createElement('span'); label.textContent = row.name
      marker.bindTooltip(label).on('click', () => onSelect(row.id))
    }
    const route = cycleways.find(x => x.id === selected)
    const place = parking.find(x => x.id === selected)
    if (route) map.current.fitBounds(L.latLngBounds(route.geometry), { padding: [65, 65], maxZoom: 15 })
    else if (place) map.current.setView([place.latitude, place.longitude], 15)
    return () => { layer.remove() }
  }, [cycleways, parking, selected, onSelect])
  return <div className="map-frame"><div ref={element} className="map" role="region" aria-label="Mapa de ciclovías y estacionamientos" />
    {tileError && <p className="map-message">El mapa base no está disponible. Puedes seguir usando la lista.</p>}
    <div className="map-legend"><span className="line-key" /> Ciclovía de demostración <span className="dot-key" /> Estacionamiento</div>
  </div>
}
