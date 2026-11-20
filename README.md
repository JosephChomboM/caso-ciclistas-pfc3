# CicloLima

Aplicación académica para consultar ciclovías de Lima, registrar incidencias y localizar estacionamientos para bicicletas. Proyecto Final de Carrera III, Práctica Calificada 2.

## Proyecto

- [Backlog y sprints en Jira](https://josephchombo.atlassian.net/jira/software/projects/PCC/boards/34/backlog)
- [Cronograma en Jira](https://josephchombo.atlassian.net/jira/software/projects/PCC/boards/34/timeline)
- [Repositorio](https://github.com/JosephChomboM/caso-ciclistas-pfc3)

## Arquitectura

Monolito modular en capas, siguiendo la organización de Ayni: React y TypeScript → API FastAPI → servicios de negocio → repositorios SQLAlchemy → PostgreSQL. Los módulos son usuarios, ciclovías, reportes y estacionamientos. Los datos de demostración no acreditan condiciones reales de seguridad.

## Estrategia de ramas

`main` contiene versiones revisadas; `test` integra el trabajo para pruebas; las ramas `codex/…` agrupan cambios revisables. Los PR enlazan las historias PCC correspondientes y deben pasar pruebas y controles de seguridad. El nombre de una rama no determina la autoría de sus commits.

## Entrega

El informe debe incluir evidencias de Jira, cuatro sprints, burndown, Gantt, arquitectura, pipeline y despliegue. Un pipeline configurado no acredita una ejecución satisfactoria ni una aplicación desplegada: esas evidencias se añaden al verificarlas.
