# Machiyotl

Módulo futuro de sellado forense, hashes SHA-256, preservación de evidencia, generación de PDFs y verificación.

Debe priorizar cadena de custodia, integridad, mínimos datos necesarios y operación offline-first para la PWA.

## Services

- **Audit:** `app/services/machiyotl/audit_service.py` — writes traceable `AuditLog` rows for evidence lifecycle actions (create, update, seal, note, custody, hash verify). Metadata sanitization strips sensitive fields and truncates hashes to prefixes.
## Governance

- Module charter: `docs/product/machiyotl-module-charter.md`
- Task execution plan (MCH-001): `docs/product/machiyotl-mch-001-execution-plan.md`
- API contract (v0): `docs/technical/api-contracts.md#machiyotl-mvp`
