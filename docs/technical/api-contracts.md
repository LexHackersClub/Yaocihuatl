# Contratos API

Los contratos deberán versionarse, documentar permisos, errores, auditoría y límites de datos.

## Chimalli MVP

Base path: `/api/v1/chimalli`

Estos endpoints son contratos preliminares para hackathón. No son contratos finales de producción.

### `POST /chat`

Entrada:

```json
{
  "message": "Narrativa sintética o autorizada",
  "case_id": null,
  "integration": {
    "tlachia_alert_id": "mock-alert-001",
    "source_platform": "X",
    "risk_level": "high",
    "machiyotl_evidence_hashes": ["sha256:mocked-evidence-hash"],
    "evidence_status": "sealed_mock"
  }
}
```

Salida: caso Chimalli estructurado, respuesta asistiva y respuestas rápidas.

### `POST /extract`

Extrae entidades explícitas desde narrativa. No completa datos faltantes por inferencia externa.

### `POST /vpmrg-test`

Aplica test asistivo de tres elementos. No es decisión jurídica.

### `POST /jurisdiction`

Sugiere ruta preliminar de canalización. Requiere validación humana.

### `POST /expediente`

Genera HTML imprimible como borrador para revisión humana. No constituye denuncia automática.

### `GET /cases/{case_id}`

Consulta caso en memoria del proceso actual. No es persistencia productiva.

### `POST /rag/index`

Indexa documentos disponibles en `rag_documents/` o ruta indicada.

### `POST /rag/search`

Busca chunks por intención y colección.

Intenciones soportadas:

- `tipificacion`
- `procedimiento`
- `canalizacion`
- `medidas`
- `seguridad`
- `privacidad`
- `contexto`

## Machiyotl MVP

Base path: `/api/v1/machiyotl`

Estos endpoints son contratos preliminares de demo. No son contratos finales de producción. Machiyotl opera bajo datos sintéticos, acciones reversibles/simuladas y revisión humana obligatoria. No se permite ingesta de evidencia real, capturas privadas ni decisiones legales automáticas en esta fase.

### Gobernanza del Contrato

- Versión actual del contrato: `v0` (cambios compatibles aditivos permitidos; cambios que rompan compatibilidad requieren `v1`).
- Toda ruta de escritura debe emitir auditoría con actor, acción, entidad, resultado, timestamp y metadatos seguros (sin payload sensible).
- Las respuestas de error deben usar el modelo unificado definido abajo.
- Los límites de datos (longitudes, paginación, formatos de hash) deben validarse en el servidor antes de cualquier operación de base de datos.

### Vocabulario Canónico de Estados

Estados de evidencia alineados al Machiyotl Module Charter y DESIGN.md:

- `draft` — registrada pero sin sellar localmente.
- `sealed-local` — sellada con hash local; no enviada.
- `ready` — lista para revisión; aún no enviada a autoridad.
- `submitted` — enviada a revisión institucional.
- `error` — requiere atención; el sello o los metadatos están incompletos.

Estados de privacidad mínimos para demo:

- `local-only` — solo en este dispositivo.
- `not-submitted` — no enviada a autoridad.
- `ready-for-review` — preparada para revisión.
- `submitted-to-authority` — enviada a autoridad.

Tipos de evento de custodia canónicos:

- `capture_started`
- `sealed_local`
- `metadata_reviewed`
- `ready_for_review`
- `submitted_to_review`
- `received_by_authority`

### Modelo de Error Unificado

Cada respuesta de error debe incluir:

```json
{
  "code": "CONFLICT_STATE_TRANSITION",
  "message": "La evidencia en estado 'submitted' no puede volver a 'draft'.",
  "details": [
    {
      "field": "status",
      "reason": "transition from submitted to draft is not allowed"
    }
  ],
  "trace_id": "mch-a1b2c3d4"
}
```

Códigos de error definidos:

| Código | HTTP | Cuándo se usa |
|---|---|---|
| `VALIDATION_ERROR` | 422 | Payload inválido o restricción de campo incumplida. |
| `NOT_FOUND` | 404 | Recurso no existe con el identificador proporcionado. |
| `CONFLICT_STATE_TRANSITION` | 409 | Transición de estado no permitida según la máquina de estados. |
| `UNAUTHORIZED` | 401 | Token de acceso ausente, expirado o inválido. |
| `FORBIDDEN` | 403 | El rol autenticado no tiene permiso sobre el recurso. |
| `HASH_MISMATCH` | 422 | El hash enviado no coincide con el hash almacenado. |
| `DEMO_BOUNDARY` | 422 | La operación solicitada excede los límites del entorno demo. |

### `POST /evidence`

Crea un registro de evidencia solo con metadatos. No acepta carga binaria en v0.

Entrada:

```json
{
  "case_id": "uuid-opcional",
  "evidence_type": "screenshot_placeholder",
  "platform": "Plataforma demo A",
  "source_url": "https://example.invalid/demo/evidence-001",
  "original_filename": "captura-demo.png",
  "mime_type": "image/png",
  "size_bytes": 204800,
  "sha256_hash": "9f2a7cd8e18b40a3c6f5e2d1b8a9c0d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0",
  "short_hash": "9f2a7c...d18b40",
  "status": "draft",
  "privacy_state": "local-only",
  "captured_at": "2026-05-15T14:30:00Z"
}
```

Campos requeridos: `evidence_type`, `sha256_hash`, `short_hash`, `status`, `privacy_state`, `captured_at`.

Validaciones:
- `sha256_hash`: máximo 128 caracteres, formato hexadecimal o `sha256:<hex>`.
- `short_hash`: máximo 24 caracteres.
- `status`: debe ser uno de los valores canónicos.
- `privacy_state`: debe ser uno de los valores canónicos.
- `captured_at`: no puede ser futuro.

Salida: recurso `EvidenceItem` completo con `id`, `evidence_code`, `created_at`, `sealed_at` (nulo si el estado no es `sealed-local` o posterior).

Auditoría: `machiyotl.evidence.create`, `outcome: success|failure`.

### `GET /evidence`

Lista evidencias con filtros. Requiere autenticación demo.

Query params:

| Parámetro | Tipo | Requerido | Descripción |
|---|---|---|---|
| `owner_user_id` | UUID | No | Filtrar por persona propietaria. |
| `case_id` | UUID | No | Filtrar por expediente transversal. |
| `status` | string | No | Estado canónico de evidencia. |
| `platform` | string | No | Plataforma de origen. |
| `from` | ISO 8601 | No | `captured_at` desde. |
| `to` | ISO 8601 | No | `captured_at` hasta. |
| `limit` | integer | No | Máximo de resultados (default: 50, máximo: 200). |
| `offset` | integer | No | Desplazamiento para paginación (default: 0). |

Respuesta:

```json
{
  "items": ["EvidenceItem", "..."],
  "total": 14,
  "limit": 50,
  "offset": 0
}
```

### `GET /evidence/{evidence_id}`

Devuelve un recurso `EvidenceItem` completo con su resumen actual.

Parámetro de ruta: `evidence_id` (UUID).

Errores:
- `NOT_FOUND` si el identificador no existe.

### `PATCH /evidence/{evidence_id}`

Actualización controlada de campos permitidos. No permite cambios arbitrarios de estado.

Parámetro de ruta: `evidence_id` (UUID).

Entrada (todos los campos opcionales; solo se aplican los enviados):

```json
{
  "status": "sealed-local",
  "privacy_state": "local-only",
  "sealed_at": "2026-05-15T14:35:00Z",
  "source_url": "https://example.invalid/demo/updated",
  "platform": "Plataforma demo B"
}
```

Reglas de transición:
- `draft` → `sealed-local`, `ready`, `error`.
- `sealed-local` → `ready`, `error`.
- `ready` → `submitted`, `error`.
- `submitted` → terminal (no reversible en v0).
- `error` → `draft`, `sealed-local` (recuperación explícita).

Cualquier transición no listada debe devolver `CONFLICT_STATE_TRANSITION`.

Auditoría: `machiyotl.evidence.update`, `outcome: success|failure`, con `from_status` y `to_status` en metadatos.

### `POST /evidence/{evidence_id}/notes`

Agrega una nota a la evidencia.

Entrada:

```json
{
  "note": "Nota demo: evidencia sintética revisable antes de cualquier envío."
}
```

Validaciones:
- `note`: entre 1 y 4000 caracteres.
- `evidence_id` debe existir (`NOT_FOUND` si no).

Salida: recurso `EvidenceNote` con `id`, `evidence_id`, `author_user_id`, `note`, `created_at`.

Auditoría: `machiyotl.note.create`.

### `GET /evidence/{evidence_id}/notes`

Lista notas de una evidencia ordenadas por `created_at` descendente.

Query params: `limit` (default: 50, máximo: 100), `offset` (default: 0).

### `POST /evidence/{evidence_id}/custody-events`

Registra un evento de cadena de custodia.

Entrada:

```json
{
  "event_type": "sealed_local",
  "event_label": "Evidencia sellada localmente",
  "event_hash": "9f2a7cd8e18b40a3c6f5e2d1b8a9c0d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0",
  "occurred_at": "2026-05-15T14:35:00Z",
  "metadata": {
    "demo": true,
    "device_scope": "local"
  }
}
```

Validaciones:
- `event_type`: debe ser uno de los tipos canónicos.
- `event_label`: entre 1 y 160 caracteres.
- `event_hash`: opcional, máximo 128 caracteres.
- `occurred_at`: no puede ser futuro.
- `metadata`: JSON object arbitrario, máximo 4 KB serializado.

Salida: recurso `CustodyEvent` completo con `id`, `actor_user_id`, `created_at`.

Auditoría: `machiyotl.custody.create`.

### `GET /evidence/{evidence_id}/custody-events`

Devuelve la línea de tiempo de custodia ordenada por `occurred_at` ascendente.

Respuesta:

```json
{
  "events": ["CustodyEvent", "..."],
  "evidence_id": "uuid",
  "chain_length": 5
}
```

### `POST /hash/verify`

Verifica un hash enviado contra el hash almacenado de una evidencia.

Entrada:

```json
{
  "evidence_id": "uuid-opcional",
  "submitted_hash": "9f2a7cd8e18b40a3c6f5e2d1b8a9c0d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0"
}
```

Validaciones:
- `submitted_hash`: máximo 128 caracteres.
- Si se proporciona `evidence_id`, debe existir.

Comportamiento demo-safe:
- Si `evidence_id` existe, comparar contra el `sha256_hash` almacenado.
- Si `evidence_id` es nulo, buscar en toda la tabla (modo verificación pública simulada).
- El resultado nunca implica validez legal; es solo una verificación criptográfica de integridad de datos sintéticos.

Respuesta:

```json
{
  "evidence_id": "uuid-o-null",
  "submitted_hash": "9f2a7c...",
  "stored_hash": "9f2a7c...",
  "result": "match",
  "verified_at": "2026-05-15T14:40:00Z",
  "warning": "Verificacion criptografica de datos sinteticos. No constituye validez legal."
}
```

Resultados posibles: `match`, `mismatch`, `evidence_not_found`.

Auditoría: `machiyotl.hash.verify`.

### `GET /hash/verifications`

Consulta historial de verificaciones de hash.

Query params:

| Parámetro | Tipo | Requerido | Descripción |
|---|---|---|---|
| `evidence_id` | UUID | No | Filtrar por evidencia. |
| `from` | ISO 8601 | No | `verified_at` desde. |
| `to` | ISO 8601 | No | `verified_at` hasta. |
| `limit` | integer | No | Default: 50, máximo: 200. |
| `offset` | integer | No | Default: 0. |

### Contratos de Recursos (Schemas de Respuesta)

#### EvidenceItem

```json
{
  "id": "uuid",
  "case_id": "uuid-o-null",
  "owner_user_id": "uuid-o-null",
  "evidence_code": "EVD-2026-DEMO-001",
  "evidence_type": "screenshot_placeholder",
  "platform": "Plataforma demo A",
  "source_url": "https://example.invalid/demo/evidence-001",
  "local_file_path": "/storage/demo/evidence-demo-captura.txt",
  "original_filename": "captura-demo.png",
  "mime_type": "image/png",
  "size_bytes": 204800,
  "sha256_hash": "9f2a7cd8...f7a8b9c0",
  "short_hash": "9f2a7c...d18b40",
  "status": "sealed-local",
  "privacy_state": "local-only",
  "captured_at": "2026-05-15T14:30:00Z",
  "sealed_at": "2026-05-15T14:35:00Z",
  "created_at": "2026-05-15T14:30:00Z"
}
```

#### EvidenceNote

```json
{
  "id": "uuid",
  "evidence_id": "uuid",
  "author_user_id": "uuid-o-null",
  "note": "Nota demo: evidencia sintética revisable antes de cualquier envío.",
  "created_at": "2026-05-15T14:32:00Z"
}
```

#### CustodyEvent

```json
{
  "id": "uuid",
  "evidence_id": "uuid",
  "actor_user_id": "uuid-o-null",
  "event_type": "sealed_local",
  "event_label": "Evidencia sellada localmente",
  "event_hash": "9f2a7cd8...f7a8b9c0",
  "occurred_at": "2026-05-15T14:35:00Z",
  "metadata": {
    "demo": true,
    "device_scope": "local"
  },
  "created_at": "2026-05-15T14:35:01Z"
}
```

#### HashVerification

```json
{
  "id": "uuid",
  "evidence_id": "uuid-o-null",
  "submitted_hash": "9f2a7cd8...f7a8b9c0",
  "result": "match",
  "verified_at": "2026-05-15T14:40:00Z"
}
```

### Límites de Datos y Restricciones Demo

- Ningún endpoint acepta carga binaria de archivos en v0.
- `sha256_hash`: máximo 128 caracteres.
- `short_hash`: máximo 24 caracteres.
- `note`: entre 1 y 4000 caracteres.
- `event_label`: entre 1 y 160 caracteres.
- `metadata` (custodia): máximo 4 KB serializado.
- `limit`: máximo 200 por consulta.
- `source_url`, `local_file_path`, `original_filename`: almacenamiento de metadatos solamente; el contenido no se valida ni se accede en el servidor en entorno demo.
- Campos prohibidos en entorno demo: cualquier dato que permita identificar a una persona real, capturas reales, o comunicaciones privadas.

### Requisitos de Auditoría

Cada endpoint de escritura (`POST`, `PATCH`) debe registrar en `audit.audit_log`:

| Campo | Origen |
|---|---|
| `actor_user_id` | Usuario autenticado (vía token demo). |
| `action` | `machiyotl.<recurso>.<operacion>` (ej. `machiyotl.evidence.create`). |
| `entity_schema` | `machiyotl`. |
| `entity_table` | `evidence_items`, `evidence_notes`, `custody_events`, o `hash_verifications`. |
| `entity_id` | UUID del recurso afectado. |
| `outcome` | `success` o `failure`. |
| `metadata_json` | Contexto relevante y seguro (sin payload sensible ni contenido de notas). |

Los endpoints de lectura (`GET`) no requieren auditoría obligatoria en v0, pero deben registrar acceso en logs de aplicación para diagnóstico.

### Seguridad Pendiente Para Producción (Machiyotl)

- Auth/RBAC con alcance fino por rol y por evidencia.
- Cifrado en reposo para `local_file_path` y metadatos sensibles.
- Rate limiting por endpoint y por usuario.
- Retención configurable con política de borrado seguro.
- Firma criptográfica de eventos de custodia (adicional al hash de integridad).
- Validación de `source_url` contra lista de plataformas autorizadas en contexto institucional.

### Seguridad Pendiente Para Producción

- Auth/RBAC.
- Auditoría de accesos y cambios.
- Persistencia cifrada.
- Retención configurable.
- Rate limiting.
- Revisión de corpus legal versionado.
