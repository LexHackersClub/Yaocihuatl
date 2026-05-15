# Despliegue

## Fase 1: infraestructura minima en Render

Esta fase prepara una base operativa de despliegue con dos servicios web
dockerizados y sin logica sensible del dominio.

### Servicios incluidos

- `yaocihuatl-backend` (FastAPI minima)
- `yaocihuatl-frontend` (Next.js minima en `frontend/apps/dashboard`)

### Servicios fuera de alcance en esta fase

- PostgreSQL
- Redis
- Workers/Celery
- Integraciones externas reales
- Logica institucional sensible de `tlachia`, `machiyotl`, `chimalli`

## Contrato tecnico minimo

### Backend

- Puerto: `8000`
- Ruta de salud: `GET /health`
- Ruta raiz: `GET /`
- Variables:
  - `APP_ENV` (ej. `staging`, `production`)
  - `PORT` (default esperado: `8000`)

### Frontend

- Puerto: `3000`
- Ruta de salud: `GET /`
- Variables:
  - `PORT` (default esperado: `3000`)
  - `NEXT_PUBLIC_API_URL` (URL publica del backend en Render)

## Verificacion esperada

1. Backend responde `200` en `/health`.
2. Frontend responde `200` en `/`.
3. Frontend tiene configurada `NEXT_PUBLIC_API_URL`.

## Notas de seguridad para esta fase

- No versionar secretos ni tokens.
- No subir datos reales o sensibles al repositorio.
- Mantener esta fase como entorno base de infraestructura, no como entorno
  productivo de atencion de casos.
