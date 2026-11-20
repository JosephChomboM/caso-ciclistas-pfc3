---
name: CicloLima
description: Consulta de ciclovías y estacionamientos de Lima con lista y mapa vinculados.
colors:
  green: "#164c3d"
  ink: "#173c31"
  muted: "#526b61"
  line: "#dce5dd"
  surface: "#fff"
  background: "#f3f6f2"
  accent: "#d4ec7a"
  focus: "#a04320"
  hover: "#eaf0e9"
  field-border: "#a2b5a8"
  placeholder: "#65766d"
  scrollbar: "#a1b3a6"
  header-muted: "#d8e9de"
  demo-ink: "#605322"
  demo-background: "#f3edce"
  tab-background: "#e4eddd"
  tab-ink: "#24583d"
  selected-background: "#edf4e9"
  icon-background: "#e8f0e5"
  icon-ink: "#387051"
  selected-icon: "#cfe6b6"
  map-background: "#e0e7df"
  route: "#217257"
  parking: "#245e96"
  account-border: "#68917e"
  account-hover: "#306451"
  primary-hover: "#22664f"
  notice-background: "#e3eddd"
  report-border: "#cddcc9"
typography:
  headline:
    fontFamily: '"Public Sans", system-ui, sans-serif'
    fontSize: "clamp(26px, 3vw, 38px)"
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: "-0.03em"
  brand:
    fontFamily: '"Public Sans", system-ui, sans-serif'
    fontSize: "25px"
    fontWeight: 800
    letterSpacing: "-0.03em"
  body:
    fontFamily: '"Public Sans", system-ui, sans-serif'
    fontSize: "14px"
    lineHeight: 1.6
  result-title:
    fontFamily: '"Public Sans", system-ui, sans-serif'
    fontSize: "13px"
    lineHeight: 1.5
  field-label:
    fontFamily: '"Public Sans", system-ui, sans-serif'
    fontSize: "13px"
    fontWeight: 600
rounded:
  field: "7px"
  button: "8px"
  result-icon: "10px"
  workspace: "14px"
  result-row: "0"
spacing:
  gap-small: "8px"
  gap-controls: "12px"
  gap-coordinates: "16px"
  inset-explorer: "20px"
  gap-intro: "24px"
components:
  button-default:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.green}"
    rounded: "{rounded.button}"
    padding: "10px 14px"
  button-primary:
    backgroundColor: "{colors.green}"
    textColor: "{colors.surface}"
    rounded: "{rounded.button}"
    padding: "10px 14px"
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.field}"
    padding: "10px"
  tab-selected:
    backgroundColor: "{colors.tab-background}"
    textColor: "{colors.tab-ink}"
    rounded: "{rounded.button}"
    padding: "11px 5px"
  result-row:
    rounded: "{rounded.result-row}"
    padding: "17px 20px"
  demo-notice:
    backgroundColor: "{colors.demo-background}"
    textColor: "{colors.demo-ink}"
    rounded: "{rounded.field}"
    padding: "12px 16px"
---

# Design System: CicloLima

## Overview

**Creative North Star: «Señalización de parques urbanos de Lima».**

La identidad implementada combina verde profundo, superficies claras y Public Sans. La interfaz de consulta tiene una densidad funcional: controles compactos, nombres legibles y metadatos secundarios. El amarillo verdoso distingue la marca y el acceso a la cuenta.

Este documento describe el código de `frontend/src/styles.css`, `App.tsx` y `components/MapCanvas.tsx`, conforme a la dirección registrada en `.impeccable/surfaces/explorer.md`. Es una captura del sistema implementado; no existe un comp aprobado ni rasters de producto que actúen como referencia visual.

**Key Characteristics:**

- Cabecera verde y área de trabajo blanca sobre fondo verde pálido.
- Jerarquía tipográfica de una sola familia y profundidad mínima.
- Selección enlazada entre resultados y geometrías del mapa.
- Procedencia, fecha y advertencia de demostración visibles.

## Colors

Los colores primitivos del frontmatter conservan los valores reales del código; `green`, `muted`, `line`, `surface` y `accent` corresponden a variables CSS existentes. Los demás son valores literales extraídos, no nuevas variables de aplicación.

- **Verde profundo (`green`)**: cabecera, botones primarios, texto de controles y caret.
- **Amarillo verdoso (`accent`)**: icono de marca, acceso final de la cabecera y selección de texto.
- **Tinta (`ink`), texto secundario (`muted`), superficie, fondo y líneas**: jerarquía de contenido y separación de regiones.
- **Aviso de demostración**: fondo crema y texto oliva; los avisos de acción usan `notice-background`.
- **Selección de lista**: `selected-background`; pestaña activa con `tab-background` y `tab-ink`.
- **Mapa**: ciclovías verdes y estacionamientos azules; geometría seleccionada en `focus`. El mismo terracota define el contorno de foco del teclado.

## Typography

Public Sans se importa de Google Fonts con pesos 400, 500, 600, 700 y 800; la alternativa es `system-ui, sans-serif`. No hay una segunda familia de display o monoespaciada.

- El título de introducción usa el rol `headline`; los títulos equilibran líneas con `text-wrap: balance`.
- La marca usa 25px y peso 800 en escritorio; el valor final en móvil es 19px.
- La introducción usa 14px, interlineado 1.6 y ancho máximo 75ch; pasa a 13px en móvil.
- El encabezado de resultados usa 15px; los nombres, 13px con interlineado 1.5 y `overflow-wrap: anywhere`.
- Metadatos y pie de lista usan 11px; fuente y fecha del detalle usan 10px. El contador aplica cifras tabulares.
- Los paneles de formulario usan encabezado de 27px con espaciado -0.02em; etiquetas de 13px y peso 600.

## Layout

El contenido y el pie tienen un máximo de 1600px. El área principal usa `32px 4% 0`; la cabecera mide 82px de alto. La introducción distribuye título y ciudad con un espacio de 24px.

El explorador de escritorio es una cuadrícula de `minmax(330px, 390px) minmax(0, 1fr)`: lista a la izquierda, mapa a la derecha. El conjunto y el mapa tienen un alto mínimo de 560px. La lista desplaza resultados a partir de un máximo de 390px; los filtros tienen 20px de relleno. Los paneles de cuenta, reporte y moderación sustituyen visualmente el explorador, con formulario centrado de hasta 560px.

En `max-width: 760px`, el conjunto se convierte en columna y el mapa va primero con alto mínimo de 320px; la lista deja de tener alto máximo. El principal usa `25px 16px 0`, la cabecera 68px y relleno horizontal de 16px. Se oculta el lema de marca; los botones de cuenta usan 10px y relleno de 8px. El último botón trunca a una línea con máximo de 90px.

## Elevation & Depth

El sistema propio es principalmente plano: bordes finos y fondos tonales separan controles, lista y selección. La leyenda flotante del mapa es la única sombra explícita del CSS de aplicación: `0 4px 16px #173c3118`. Los controles y tooltips de Leaflet conservan su hoja de estilos de biblioteca.

La única transición propia es `background 0.18s ease-out` sobre el icono del resultado, dentro de `prefers-reduced-motion: no-preference`. También dentro de esa condición, el icono seleccionado cambia a `selected-icon`; con movimiento reducido conserva su fondo base.

## Shapes

Los campos y avisos de mapa usan 7px; los botones y avisos de acción, 8px; los iconos de resultado, 10px; y el contenedor del explorador, 14px con recorte del desbordamiento. Las filas son rectas y tienen separadores superiores de 1px. Los estacionamientos del mapa se representan con círculos; la leyenda usa un punto de 8px y una línea de 20 × 4px.

## Components

### Buttons

El botón base tiene borde de 1px en `line`, fondo blanco y relleno de `10px 14px`; al pasar el puntero usa `hover`. El primario elimina el borde, mide al menos 46px de alto y cambia de verde profundo a `primary-hover`. Los botones deshabilitados usan opacidad 0.6 y cursor de espera. No se define un tratamiento propio de `:active`.

### Inputs / Fields

Campos, selectores y áreas de texto tienen alto mínimo de 44px, borde de 1px en `field-border`, relleno de 10px y placeholder en `placeholder`. La búsqueda agrupa icono y campo dentro de un borde común; el input interior queda sin borde y con fondo transparente. El filtro de favoritos usa checkbox nativo de 18px con acento verde.

Botones, enlaces y campos comparten `:focus-visible` con contorno de 3px en `focus` y separación de 3px. El enlace «Saltar al contenido» aparece al recibir foco.

### Navigation

Las dos pestañas del explorador son botones con `aria-pressed`, icono de 18px y texto de 12px; la activa usa fondo tonal y peso 700. La cuenta se alinea a la derecha de la cabecera: acciones transparentes con borde verde claro y último acceso amarillo verdoso. El hover de ambos usa `account-hover` con texto blanco.

### Cards / Containers

La lista usa filas en lugar de tarjetas flotantes. Cada fila tiene botón completo, icono y flecha; al seleccionarla aparece el detalle debajo y cambia el fondo. La selección utiliza `aria-expanded`, muestra fuente y fecha, y permite consultar reportes o guardar un estacionamiento.

Los estados de carga, error y ausencia de resultados ocupan el espacio de la lista con relleno de 20px. El error ofrece reintento. «Limpiar filtros» borra búsqueda, distrito, condición y el filtro de favoritos.

### Map and notices

Leaflet usa teselas de OpenStreetMap y conserva su atribución enlazada. No hay rasters propios de producto. La leyenda blanca flota abajo a la izquierda y los controles de zoom abajo a la derecha. Las líneas tienen grosor 5 y 8 al seleccionar; los estacionamientos tienen radio 10, borde blanco de grosor 3 y relleno azul o terracota seleccionado.

La selección encuadra el recorrido con relleno de 65px y zoom máximo 15; un estacionamiento centra el mapa en zoom 15. Si fallan las teselas, un aviso superior mantiene disponible la consulta por lista. Los datos de demostración se identifican con aviso crema y en la leyenda.

## Do's and Don'ts

### Do:

- **Do** mantener Public Sans, los valores extraídos y la jerarquía de textos secundarios.
- **Do** conservar foco visible y semántica de selección en controles.
- **Do** mantener el mapa arriba de la lista en el breakpoint móvil implementado.
- **Do** mostrar procedencia, fecha y atribución cartográfica.

### Don't:

- **Don't** presentar datos de demostración como infraestructura validada ni deducir seguridad de la ausencia de reportes.
- **Don't** retirar la atribución de OpenStreetMap.
- **Don't** tratar esta documentación del código como un comp aprobado.
