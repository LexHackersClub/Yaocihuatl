# Machiyotl

Módulo futuro de sellado forense, hashes SHA-256, preservación de evidencia, generación de PDFs y verificación.

Debe priorizar cadena de custodia, integridad, mínimos datos necesarios y operación offline-first para la PWA.

## Services

- **Audit:** `app/services/machiyotl/audit_service.py` — writes traceable `AuditLog` rows for evidence lifecycle actions (create, update, seal, note, custody, hash verify). Metadata sanitization strips sensitive fields and truncates hashes to prefixes.
- **Repository:** `app/services/machiyotl/repository.py` — centralized query layer for all Machiyotl reads. Enforces module boundaries (no cross-schema joins), pagination caps, and index-aware query patterns.

## Query Patterns

| Method | DB Table | Index Used | Order | Notes |
|---|---|---|---|---|
| `get_evidence_by_id` | `evidence_items` | PK (`id`) | N/A | Single-row lookup |
| `get_evidence_by_code` | `evidence_items` | Unique (`evidence_code`) | N/A | Human-readable lookup |
| `list_evidence` (owner+status) | `evidence_items` | `ix_machiyotl_evidence_owner_status` | `captured_at DESC` | Primary dashboard query |
| `list_evidence` (case+status) | `evidence_items` | `ix_machiyotl_evidence_case_status` | `captured_at DESC` | Case-scoped query |
| `get_evidence_notes` | `evidence_notes` | FK (`evidence_id`) | `created_at DESC` | Paginated |
| `get_custody_timeline` | `custody_events` | `ix_machiyotl_custody_evidence_time` | `occurred_at ASC` | Full timeline |
| `list_hash_verifications` | `hash_verifications` | FK (`evidence_id`) | `verified_at DESC` | Paginated |

All queries are constrained to the `machiyotl` schema. No cross-module joins.

## Governance

- Module charter: `docs/product/machiyotl-module-charter.md`
- Task execution plan (MCH-001): `docs/product/machiyotl-mch-001-execution-plan.md`
- API contract (v0): `docs/technical/api-contracts.md#machiyotl-mvp`
