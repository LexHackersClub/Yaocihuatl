# Instrucciones para Claude Code y Coding Agents

Yaocíhuatl es una plataforma institucional orientada a detección, certificación forense y canalización legal de VPMRG digital. Este repositorio está en fase de scaffolding: la prioridad es mantener estructura, documentación y límites claros antes de escribir lógica sensible.

## Contexto del Proyecto

La plataforma está organizada en tres módulos:

- `tlachia`: monitoreo, ingesta controlada, clasificación asistida, detección de coordinación y alertas.
- `machiyotl`: PWA offline-first, sellado forense, hash SHA-256, preservación de evidencia, PDFs y verificación.
- `chimalli`: RAG legal, extracción de entidades, test VPMRG, orientación jurisdiccional y generación de expediente.

## Arquitectura Esperada

El repositorio está pensado como monorepo full-stack:

- `frontend/`: aplicaciones web, PWA e interfaces institucionales.
- `backend/`: API, servicios de dominio, workers, pipelines NLP, RAG y expedientes.
- `docs/`: documentación institucional, técnica, legal, ética y de demo.
- `infra/`: despliegue, observabilidad y ambientes.
- `datasets/`: datos demo, sintéticos o anonimizados.
- `legal-corpus/`: corpus jurídico versionado para funciones RAG.
- `prompts/`: prompts versionados con propósito, entradas, salidas y restricciones.
- `tests/`: pruebas futuras.

## Reglas para Tareas Futuras

- Respetar el scaffolding actual.
- No generar lógica avanzada hasta que exista especificación explícita.
- No conectar APIs reales sin autorización, documentación y configuración segura.
- No crear endpoints definitivos, modelos finales ni autenticación todavía.
- No implementar IA, scraping ni conexión real a redes sociales en esta fase.
- Mantener cada implementación modular, testeable y documentada.
- Cualquier cambio legal debe citar fuente, versión, fecha y ubicación en `legal-corpus/`.
- Cualquier flujo de evidencia debe preservar cadena de custodia y auditabilidad.
