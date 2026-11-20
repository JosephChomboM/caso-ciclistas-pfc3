# Verificación por unidad de trabajo

## Base del proyecto

`backend/.venv/bin/pytest -q tests/test_settings.py`: 3 pruebas aprobadas. Verifica secreto, CORS y configuración de producción. No existe aún frontera HTTP en esta unidad. Rollback: retirar core, configuración de dependencias, compose y arquitectura sin cambiar el README inicial.

## Usuarios

Pruebas HTTP con TestClient: registro, correo duplicado, rechazo de escalada de rol, sesión, actualización del perfil propio y cierre de sesión con invalidación persistente. Pruebas incluidas junto con la implementación. El hash nunca forma parte de las respuestas. Rollback: retirar el módulo users y su router, tests y dependencias de autenticación; mantener core.

## MVP ampliado: pruebas y despliegue

La versión funcional `7b67304c7d026c103a0043783ce6cb97539e60fe` pasó controles y despliegues de [GitHub Actions 44676252423](https://github.com/JosephChomboM/caso-ciclistas-pfc3/actions/runs/44676252423). La API `/ready` y la web `/version.json` de producción devolvieron ese mismo commit.

- Backend: 12 pruebas pytest y Ruff; autenticación, propiedad de datos, moderación, reportes, sugerencias y billing.
- Frontend: 10 pruebas Vitest, formato, TypeScript y build.
- PostgreSQL real en CI: migración, carga, cuenta, favoritos, logout, cambio repetido de plan sin comprobante duplicado y exportación CSV propia.
- Seguridad: CodeQL, auditorías de dependencias, Gitleaks y construcción del contenedor. Los despliegues esperan los controles; producción conserva su aprobación manual.

## Comprobación funcional

En navegador local y stage se comprobó registro, regreso al panel solicitado tras login, selección mapa/lista, sugerencias, favorito, plan Plus, comprobante simulado, descarga CSV y reporte pendiente. Un usuario normal no muestra moderación. La publicación positiva se probó con un moderador local y mediante pruebas HTTP; no se otorgó ese rol al usuario de QA de la nube.

El CSV descargado desde stage se leyó del disco y contenía únicamente el estacionamiento de esa cuenta. Quedaron registros identificados como verificación. No se utilizaron tarjetas ni cobros reales.

En producción también se verificaron en navegador el registro, sugerencias y su selección en el mapa, plan Plus persistente, comprobante simulado, favorito, exportación CSV y envío de un reporte sintético a revisión. El CSV de producción se abrió desde disco y contenía exactamente el único favorito de la cuenta QA. Las capturas `billing-production-functional.jpg` y `report-production-functional.jpg` registran estos resultados. El usuario QA conserva rol normal y su reporte no se publicó automáticamente.

## Persistencia

Los ambientes usan bases independientes y el esquema privado `ciclolima`. Los comandos aditivos e idempotentes `seed-showcase` y `seed-billing-demo` cargan datos sintéticos. Antes del QA de producción se verificaron users (4), cycleways (12), parking (9), reports (9), moderation_actions (7), favorites (6), billing_subscriptions (4) y billing_invoices (4). Existe además la tabla técnica de versión Alembic. Las verificaciones pueden agregar registros de QA. El asesor de seguridad de Supabase no devolvió alertas en esta comprobación.

Las sugerencias son reglas explicables, no un modelo entrenado ni una certificación de seguridad vial. Billing es simulado. Para revertir billing en backend se deben revisar primero los datos persistentes y su migración; una reversión visual no justifica borrar tablas.

Las capturas e historial Scrum están en `docs/evidence/`. La entrega final incluye el informe actualizado, ZIP de código, diagramas draw.io y capturas originales. El cierre del sprint 4 y el acceso del docente se comprobaron el 20 de noviembre de 2026.
