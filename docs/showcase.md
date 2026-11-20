# Catálogo académico ampliado

`uv run python -m app.cli seed-showcase` agrega 12 tramos, 9 estacionamientos, 4 cuentas sintéticas inaccesibles, 9 reportes, 7 decisiones y 6 favoritos si faltan. Conserva los registros existentes y puede repetirse sin duplicarlos. No imprime credenciales: las contraseñas sintéticas son aleatorias y se descartan.

Los reportes de ejemplo se identifican en su descripción y el catálogo conserva fuente académica e indicador is_demo. No son reportes de hechos reales. Solo seis reportes publicados son visibles; los dos pendientes y el rechazado no aparecen en consulta pública.

Verificación de PCC-17: diez pruebas de backend aprobadas, incluida idempotencia y conservación de datos. Rollback del comportamiento: retirar showcase.py, su comando y su test; no eliminar automáticamente datos ya cargados.
