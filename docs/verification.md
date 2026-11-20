# Verificación por unidad de trabajo

## Base del proyecto

`backend/.venv/bin/pytest -q tests/test_settings.py`: 3 pruebas aprobadas. Verifica secreto, CORS y configuración de producción. No existe aún frontera HTTP en esta unidad. Rollback: retirar core, configuración de dependencias, compose y arquitectura sin cambiar el README inicial.

## Usuarios

Pruebas HTTP con TestClient: registro, correo duplicado, rechazo de escalada de rol, sesión, actualización del perfil propio y cierre de sesión con invalidación persistente. Pruebas incluidas junto con la implementación. El hash nunca forma parte de las respuestas. Rollback: retirar el módulo users y su router, tests y dependencias de autenticación; mantener core.

Los resultados adicionales, capturas y ejecuciones de CI se registran tras ejecutarse. Esta documentación no acredita despliegue público.
