# Billing de demostración

PCC-20 implementa dos planes de prueba. Comunidad conserva mapa, reportes y favoritos. Plus agrega exportación privada de favoritos en CSV. El importe de referencia de Plus es S/ 9.90 al mes y cada cambio genera un comprobante simulado. No existe pasarela de pagos, formulario de tarjeta ni cobro real.

La API calcula el importe; el cliente solo envía el código de plan. Suscripciones y comprobantes pertenecen a la cuenta autenticada. Repetir el mismo plan no duplica comprobantes. La exportación requiere Plus y solo contiene favoritos del propietario; se neutralizan valores que podrían interpretarse como fórmulas en una hoja de cálculo.

Alembic agrega billing_subscriptions y billing_invoices en el esquema privado existente. `uv run python -m app.cli seed-billing-demo` inicializa únicamente las cuentas sintéticas conocidas que aún no tienen suscripción, sin cambiar planes existentes. No crea ni publica contraseñas.

Verificación: 12 pruebas backend aprobadas, migración local y alembic check sin diferencias; el smoke de CI comprueba suscripción repetida, comprobante único y CSV con PostgreSQL real. Rollback funcional: retirar router, servicio y UI de billing; no ejecutar downgrade ni eliminar comprobantes automáticamente.
