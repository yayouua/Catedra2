# ACI606 - Docker Rescue Challenge

Este repositorio contiene una aplicación web multi-servicio que debe ejecutarse mediante Docker Compose.

## Arquitectura general

Frontend (Nginx) -> Backend/API (FastAPI) -> Database (PostgreSQL)

## Situación inicial

El sistema fue recibido desde un equipo anterior y presenta múltiples problemas de construcción, configuración, comunicación y operación. No se informa la cantidad total de fallas ni su ubicación.

Su trabajo consiste en diagnosticar el sistema utilizando evidencia técnica, reparar las incidencias identificadas y demostrar que la solución final puede ejecutarse de forma reproducible.

## Inicio sugerido

```bash
docker compose up --build -d
docker compose ps
docker compose logs
```

No reemplace la aplicación por un proyecto nuevo. Trabaje sobre los archivos suministrados y documente cada modificación en el informe técnico y mediante el historial del repositorio.
