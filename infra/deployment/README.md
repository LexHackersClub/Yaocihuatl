# Deployment

## Objetivo de esta fase

Preparar una base de despliegue en Render con dos servicios Docker:

- Backend (FastAPI minima)
- Frontend (Next.js minima)

Sin base de datos, Redis ni workers en esta etapa.

## Flujo recomendado

1. Mantener `render.yaml` como fuente declarativa de infraestructura.
2. Desplegar ambos servicios web desde el repositorio.
3. Configurar variables de entorno minimas por servicio.
4. Verificar health checks y conectividad frontend -> backend.

## Smoke tests post-deploy

1. Backend: `GET /health` responde `200`.
2. Frontend: `GET /` responde `200`.
3. Frontend tiene `NEXT_PUBLIC_API_URL` apuntando al backend publico.

## Troubleshooting basico

- Si backend no inicia: revisar `PORT` y comando de arranque.
- Si frontend no inicia: revisar build/start de Next.js y `PORT`.
- Si frontend no ve backend: validar `NEXT_PUBLIC_API_URL` y redeploy.

## Seguridad minima

- No incluir secretos en archivos versionados.
- Rotar cualquier token previamente expuesto.
- Usar solo datos demo/sinteticos para pruebas.
