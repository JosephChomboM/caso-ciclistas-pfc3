# CicloLima

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

React y TypeScript, FastAPI y PostgreSQL. El usuario pidió una estructura similar a Ayni y confirmó una pantalla principal de mapa y lista.

## Users

Ciclistas de Lima que consultan tramos y estacionamientos, y aportan incidencias. Un moderador revisa los reportes antes de publicarlos.

## Product Purpose

Hacer consultable la información de ciclovías, incidencias y estacionamientos, mostrando su procedencia y fecha. La práctica requiere backlog, cuatro sprints, DevSecOps y despliegue verificable.

## Capabilities and Constraints

Registro y acceso, mapa, filtros, detalles, reportes moderados, perfil y favoritos. La pantalla principal conserva mapa y lista. El recomendador compara distancia y reportes publicados con razones explícitas. Billing permite probar planes, comprobantes simulados y exportación privada de favoritos; no realiza cobros ni recopila tarjetas. El footer enlaza el GitHub de Joseph. No se afirma que una ruta sea segura ni se calcula navegación entre origen y destino. No hay captura continua de ubicación.

## Evidence on Hand

Enunciado académico y backlog PCC. No se dispone de una base oficial de infraestructura vial validada; los datos iniciales son de demostración, identificados en la interfaz.

## Product Principles

- Mostrar la fuente y antigüedad de la información.
- Distinguir aportes publicados de datos verificados por una autoridad.
- Permitir la consulta sin cuenta; proteger los aportes y preferencias con autenticación.
- Mantener módulos, pruebas y documentación fáciles de explicar en la sustentación.

## Open decisions

Render y Supabase están configurados en recursos exclusivos de CicloLima, separados por ambiente. Permanecen pendientes los datos geográficos oficiales y la fecha real de entrega. El Gantt es una planificación académica; Jira conserva eventos de una simulación comprimida. El usuario mantiene detenidos el ZIP y el material final de presentación.
