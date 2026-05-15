# Arquitectura Conceptual

Yaocíhuatl se diseña como monorepo full-stack modular para despliegue institucional, incluyendo escenarios on-premise en producción.

## Capas

- **Presentación:** aplicaciones web, dashboard, PWA y chat legal.
- **Aplicación:** casos de uso, orquestación, validaciones de flujo y contratos API.
- **Dominio:** reglas del negocio institucional, evidencia, expedientes, alertas y clasificación asistida.
- **Datos:** persistencia, auditoría, vectores legales, metadatos y datos demo.
- **Integraciones externas:** conectores futuros a plataformas, servicios de IA, mensajería o sistemas institucionales.

## Módulos

- **Tlachia:** ingesta, normalización, detección asistida, patrones de coordinación y alertas.
- **Machiyotl:** evidencia, hash SHA-256, cadena de custodia, PDFs, verificación y PWA offline-first.
- **Chimalli:** RAG legal, extracción de entidades, rutas de canalización, test VPMRG y expediente.

## Servicios Transversales

- Auth/RBAC.
- Auditoría.
- Notificaciones.
- Verificación de hashes.
- Generación de PDFs.
- RAG legal.

## Despliegue

El sistema debe poder operar en ambientes institucionales controlados. Cualquier dependencia externa debe ser configurable, auditable y reemplazable por alternativas on-premise cuando el contexto lo requiera.
