# DevSecOps y despliegue

El pipeline verifica el cambio antes de solicitar despliegues. Pruebas y producción tienen bases, secretos, API y web separados. El código reutiliza la organización técnica de Ayni, con recursos nuevos de CicloLima.

| Fase | Herramienta | Seguridad y evidencia |
|---|---|---|
| Plan | Jira PCC | Aceptación, prioridad, puntos y límites de privacidad |
| Code | GitHub y ramas joseph/ | Revisión por PR, validaciones y permisos en API |
| Build | uv, npm y Docker | Lockfiles, TypeScript y contenedor sin usuario root |
| Test | pytest, Vitest y PostgreSQL 16 | Sesiones, autorización, favoritos privados y migraciones |
| Release | main y test | Commits descriptivos y checks del PR |
| Deploy | GitHub Actions y Render | Hooks secretos por ambiente; comprobar SHA en API y web |
| Operate | Render y Supabase | Salud, logs sin contenido sensible, migraciones versionadas |
| Monitor | Logs de servicios y Actions | Disponibilidad, fallos de despliegue y alertas de seguridad |

CodeQL analiza Python y TypeScript. Gitleaks busca secretos en el historial. npm audit y pip-audit comprueban dependencias. El build de imagen demuestra que el Dockerfile se construye; no se presenta como escaneo de vulnerabilidades de la imagen. Un análisis satisfactorio no garantiza ausencia de vulnerabilidades.

## Datos y sesiones

Supabase almacena el esquema privado `ciclolima`, fuera de los esquemas de la Data API. El rol de aplicación tiene acceso a ese esquema; las credenciales no se sirven al navegador. CORS acepta orígenes explícitos. Las contraseñas usan Argon2 y las sesiones JWT vencen; cerrar sesión incrementa una versión persistida que invalida los tokens anteriores de la cuenta.

Los reportes se crean pendientes. La API consulta el rol actual en la base antes de permitir moderación y registra la decisión. Las respuestas públicas no exponen el correo ni identificador de quien reportó. La ubicación del reporte no es seguimiento continuo del usuario.

## Configuración en GitHub

En los environments `stage` y `production`, guardar `RENDER_API_DEPLOY_HOOK` y `RENDER_WEB_DEPLOY_HOOK` como secretos, y `API_URL` y `WEB_URL` como variables. Estos valores no van en el repositorio. El environment production exige revisión de Joseph antes de continuar; nombrarlo sin esa regla no sería suficiente.

Las ramas joseph/ abren PR hacia main. Los PR ejecutan build, tests y seguridad sin desplegar. Tras el merge, el push a main repite los controles y despliega a stage. Producción depende del stage verificado y de aprobación manual. La rama test queda para pruebas y evidencia académica, sin disparar despliegues.

El job valida que la configuración exista, solicita los despliegues del SHA exacto y espera a que `/ready` y `/version.json` devuelvan ese SHA. Una respuesta satisfactoria del hook por sí sola no demuestra despliegue completo. Los servicios de stage conservan por ahora los nombres físicos con sufijo -test y usan sus propias bases.

## Operaciones

El contenedor ejecuta Alembic antes de arrancar la API. La carga de datos demo se ejecuta de forma explícita, sin cuentas o contraseñas predeterminadas. `/health` responde sobre el proceso y `/ready` comprueba acceso al esquema migrado. El versionado identifica el commit de cada entrega.

Para revertir una entrega, redeplegar en Render el commit conocido que funcionaba y preparar un PR de reversión. No ejecutar downgrade de una base con datos sin revisar su efecto. El plan gratuito no sustituye una política de respaldos: exportar datos antes de cambios destructivos.

## Referencias

- [Conexión de PostgreSQL y pooler de Supabase](https://supabase.com/docs/guides/database/connecting-to-postgres)
- [JWT en FastAPI](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
