# Reglas del proyecto

- La rúbrica de la Práctica Calificada 2 es el criterio de aceptación principal. Ayni es una referencia técnica; cualquier adaptación debe cumplir primero los requisitos del enunciado y mostrar evidencia verificable.
- Las ramas de trabajo usan exclusivamente el prefijo `joseph/`.
- Los commits usan la identidad Git configurada de Joseph. No añadir agentes como autores ni coautores; no incluir trailers automáticos de coautoría.
- Código, nombres y commits en inglés; interfaz y documentación académica en español.
- Mantener frontend React y backend FastAPI como proyectos separados dentro del monorepo.
- Cada módulo de negocio conserva router, schemas, service, repository y models. Otros módulos consumen solo su service público.
- Secretos únicamente en variables de entorno y archivos locales ignorados. No incluir claves, contraseñas ni deploy hooks en código, capturas o documentación.
- Los datos sintéticos deben identificarse como demostración. No certificar seguridad vial ni presentar la falta de reportes como seguridad.
- Toda simulación Scrum debe identificarse como tal; no fabricar historial o evidencias de Jira.
- Incluir pruebas relevantes con cada comportamiento. Ejecutar pytest y Ruff en backend; Vitest y build en frontend.
- Aplicar cambios de esquema con Alembic. Las bases de pruebas y producción son independientes; no usar bases de Ayni.
