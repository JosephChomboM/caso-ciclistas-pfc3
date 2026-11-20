# Sugerencias explicables

PCC-19 incorpora un recomendador por contenido, sin entrenamiento ML ni servicios externos. La API compara la longitud del tramo con la distancia objetivo y descuenta por reportes publicados. La afinidad no es una probabilidad de seguridad.

Puntaje = máximo de cero y 100 menos penalización por distancia (hasta 90) menos 10 por reporte publicado (hasta 30). El servidor valida entre 0.5 y 20 km, filtra por distrito y devuelve tres sugerencias con los factores empleados. Los reportes privados no alteran la consulta pública.

El usuario puede seleccionar una sugerencia para abrir su tramo en el mapa. Cada registro conserva su fuente; los ejemplos académicos se identifican dentro de la explicación. La ausencia de reportes nunca se presenta como garantía de seguridad.

Verificación: prueba HTTP de orden, privacidad y validación; tests de selección de mapa y recuperación ante error de red en frontend. Rollback: retirar endpoint, servicio y panel de sugerencias, sin modificar catálogo ni reportes.
