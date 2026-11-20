# CicloLima

Aplicación académica para consultar ciclovías de Lima, registrar incidencias y localizar estacionamientos para bicicletas. Proyecto Final de Carrera III, Práctica Calificada 2.

## Proyecto

- [Backlog y sprints en Jira](https://josephchombo.atlassian.net/jira/software/projects/PCC/boards/34/backlog)
- [Cronograma en Jira](https://josephchombo.atlassian.net/jira/software/projects/PCC/boards/34/timeline)
- [Repositorio](https://github.com/JosephChomboM/caso-ciclistas-pfc3)
- [Aplicación en producción](https://ciclolima-web-production-ay79.onrender.com)

## Arquitectura

Monolito modular en capas, siguiendo la organización de Ayni: React y TypeScript → API FastAPI → servicios de negocio → repositorios SQLAlchemy → PostgreSQL. Los módulos son usuarios, ciclovías, reportes y estacionamientos. Los datos de demostración no acreditan condiciones reales de seguridad.

```text
backend/
  app/core/             configuración, base de datos y seguridad
  app/modules/users/    registro, sesiones y perfil
  app/modules/cycleways/ mapa, filtros y detalle de tramos
  app/modules/reports/  incidencias y moderación
  app/modules/parking/  estacionamientos y favoritos
  migrations/           esquema versionado con Alembic
  tests/                reglas y flujos HTTP
frontend/
  src/api/              cliente HTTP tipado
  src/components/       mapa, cuenta y formularios
  src/App.tsx           composición del explorador
docs/                   arquitectura, Scrum, seguridad y evidencias
.github/workflows/      CI y despliegue
```

Cada módulo tiene `router.py`, `schemas.py`, `service.py`, `repository.py` y `models.py`. Los cruces entre módulos usan la interfaz pública del servicio.

## Ejecutar en local

Requisitos: Python 3.12, uv y Node 24. SQLite permite probar sin Docker; PostgreSQL se comprueba en CI y se utiliza en la nube.

```bash
cd backend
cp .env.example .env
# Escribe en .env un JWT_SECRET generado con openssl rand -hex 32
uv sync --frozen
uv run alembic upgrade head
uv run python -m app.cli seed-demo
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

En otra terminal:

```bash
cd frontend
npm ci
npm run dev
```

La web usa el proxy de Vite hacia `127.0.0.1:8000`. En Render, `VITE_API_URL` debe apuntar a la API del mismo ambiente.

## Pruebas y moderación

```bash
cd backend
uv run pytest -q
uv run ruff check .
uv run ruff format --check .
cd ../frontend
npm test
npm run build
```

No hay contraseñas predeterminadas. Registra una cuenta desde la aplicación. Para habilitar moderación, un operador con acceso a la base ejecuta `uv run python -m app.cli promote-moderator correo@example.com` en el entorno correspondiente. El usuario debe volver a iniciar sesión.

## Funcionalidades adicionales

- Sugerencias por distrito y distancia objetivo, con razones explícitas y selección del tramo en el mapa. Su afinidad no es una garantía de seguridad.
- Planes de demostración con suscripción persistida, comprobantes privados y exportación CSV de favoritos con Plus. No hay cobros ni tarjetas.
- Footer con navegación al mapa, planes y GitHub de Joseph; la fuente académica se consulta en cada lugar y en Datos y alcance.

`uv run python -m app.cli seed-showcase` amplía los datos académicos sin duplicarlos. Después de migrar, `uv run python -m app.cli seed-billing-demo` inicializa únicamente suscripciones sintéticas faltantes. Las tablas están en el esquema privado **ciclolima** de Supabase, no en public. Ver [datos](docs/showcase.md), [sugerencias](docs/recommendations.md) y [billing](docs/billing.md).

## Entornos de pruebas

- [Web de pruebas](https://ciclolima-web-test.onrender.com)
- [API de pruebas](https://ciclolima-api-test.onrender.com/docs)
- [Pipeline y ejecuciones](https://github.com/JosephChomboM/caso-ciclistas-pfc3/actions)
- [Arquitectura](docs/architecture.md), [Scrum](docs/scrum.md) y [DevSecOps](docs/devsecops.md).

## Estrategia de ramas

Las ramas `joseph/…` abren PR directamente hacia `main`. Tras aprobar controles y fusionar el PR, el push a `main` despliega automáticamente a **stage**. **Producción requiere aprobación manual** en GitHub Environments y solo queda habilitada cuando stage se verificó. La rama `test` queda disponible para pruebas y como evidencia de la rúbrica, sin ser un paso obligatorio hacia main ni disparar despliegues.

Los PR enlazan las historias PCC correspondientes. Los commits usan la identidad de Joseph, sin coautorías automáticas.

## Entrega

El informe debe incluir evidencias de Jira, cuatro sprints, burndown, Gantt, arquitectura, pipeline y despliegue. Un pipeline configurado no acredita una ejecución satisfactoria ni una aplicación desplegada: esas evidencias se añaden al verificarlas.
