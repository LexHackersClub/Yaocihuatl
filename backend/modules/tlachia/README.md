# Tlachia

Tlachia es el modulo de observacion y alertas. Su responsabilidad es identificar senales publicas o autorizadas que puedan requerir revision institucional por posible VPMRG digital.

## Estado Actual

- Pantallas demo en `frontend/apps/demo/src/app/app/tlachia`.
- Tablas creadas en PostgreSQL bajo el esquema `tlachia`.
- Seed sintetico con alerta, senales, mencion sanitizada y cluster.
- Sin ingesta real ni clasificadores conectados todavia.

## Responsabilidad Tecnica

- Normalizar menciones publicas/autorizadas a un esquema comun.
- Generar alertas con `risk_level` asistivo: `low`, `medium`, `high`, `unclassified`.
- Guardar senales explicables para revision humana.
- Guardar solo fragmentos sanitizados o autorizados.
- Vincular alertas revisadas con `core.cases` cuando corresponda.
- Nunca emitir `confirmed` como resultado de regla o modelo automatico.

## Limites

- No scraping invasivo.
- No vigilancia masiva.
- No comunicaciones privadas.
- No confirmacion automatica de VPMRG.
- No identificacion de agresores por inferencia.
- No almacenar datos reales sin documentar fuente, autorizacion, minimizacion, retencion y controles de acceso.

## Alcance MVP Actual

- Login institucional base con roles reales.
- Sesiones, logout y auditoria.
- Proteccion de endpoints por rol.
- CRUD administrativo minimo de usuarios.
- Configuracion de fuentes Reddit por subreddit y terminos.
- Ingesta manual o programada controlada desde Reddit (API oficial, OAuth).
- Normalizacion de posts/comments publicos a menciones sanitizadas.
- Reglas explicables de riesgo iniciales (sin clasificacion legal definitiva).
- Alertas Tlachia con revision humana.
- Dashboard conectado a endpoints reales.

## Objetivo Futuro (Fase 2)

- OIDC institucional real.
- Firma electronica avanzada.
- MFA.
- APIs de X/Facebook/Instagram/TikTok (si autorizadas).
- Clasificador NLP BETO/DeepSeek para las 19 conductas del Art. 20 Ter.
- Clustering DBSCAN/NetworkX para deteccion de campanas coordinadas.
- Notificacion push real a victimas.
- Apertura automatica de expediente legal.

## Siguiente Implementacion

Antes de escribir logica real se debe documentar:

- fuentes permitidas;
- contratos de adaptadores;
- campos de entrada/salida;
- riesgos de sesgo;
- sanitizacion;
- auditoria;
- revision humana;
- pruebas con datos sinteticos/anonimizados.
