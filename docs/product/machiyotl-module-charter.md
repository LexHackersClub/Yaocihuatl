# Machiyotl Module Charter

## 1) Purpose

Machiyotl is the Yaocihuatl module responsible for assistive forensic evidence handling in a privacy-first, audit-friendly, human-supervised workflow. In the current project phase, Machiyotl provides documentation and demo-safe behavior for local evidence handling, metadata consistency, hash identity representation, and custody traceability patterns.

This module must never be implemented as an autonomous legal-decision system or as a mechanism for mass surveillance.

## 2) Current Maturity and Operating Context

Machiyotl is in scaffold/demo maturity. The repository includes:

- conceptual module definition,
- PostgreSQL structural foundation for evidence-related records,
- synthetic seed records,
- and demo UI flows.

The repository does not authorize production handling of real victim evidence in this phase.

## 3) In-Scope Responsibilities (Current Phase)

Machiyotl is authorized to define and support:

- evidence metadata structure for synthetic/demo records,
- local-first evidence status semantics,
- SHA-256 hash identity fields and hash verification placeholders,
- chain-of-custody event vocabulary and timeline representation,
- step-based user flows for safe capture/review concepts,
- clear distinction between local state and submitted state,
- documentation and controls that keep human review mandatory.

## 4) Explicit Non-Goals and Prohibitions

Machiyotl must not:

- upload evidence automatically,
- perform autonomous legal qualification or jurisdictional decisions,
- claim legal validity without human authority review,
- process real victim data or real case files in demo environments,
- ingest private communications through invasive mechanisms,
- implement mass monitoring or censorship behavior,
- collapse boundaries with Tlachia or Chimalli.

## 5) Actor and Decision Model

### Protected Woman (Mujer Protegida)

- controls evidence capture context,
- reviews before any submission action,
- can pause and continue later where flow supports it.

### Institutional Reviewer Roles

- review evidence and custody trace,
- make final decisions outside Machiyotl automation.

### System Responsibilities

- preserve integrity metadata,
- present status clearly,
- keep audit-friendly records,
- avoid deterministic legal conclusions.

### Decision Rights

- system may assist and structure,
- humans decide legal and institutional outcomes.

## 6) Data Boundaries and Minimization

Machiyotl data handling in this phase must follow minimization:

- collect only fields needed for evidence identity and traceability,
- prefer synthetic placeholders for demo artifacts,
- separate metadata from sensitive content where possible,
- avoid storing unnecessary personal attributes,
- maintain clear labels for local-only status.

Prohibited repository content includes:

- real evidence,
- personal data of victims/aggressors/witnesses,
- private captures,
- secrets and credentials.

## 7) Evidence Lifecycle Boundary

Machiyotl lifecycle vocabulary in this phase uses controlled states aligned to design and demo flows:

- `draft`
- `sealed-local`
- `ready`
- `submitted`
- `error`

State transitions must be explicit and reviewable. No transition may imply legal confirmation by the system.

## 8) Chain of Custody Boundary

Machiyotl may maintain structured custody events for traceability. Custody events must:

- include event type and event label,
- include occurred timestamp,
- include actor context where available,
- include safe metadata with no unnecessary sensitive payload.

Custody events are assistive integrity records, not legal verdict artifacts by themselves.

## 9) Cross-Module Interface Contracts

### Machiyotl -> Chimalli

Allowed:

- evidence hashes,
- evidence status indicators,
- minimal metadata required for guided orientation context.

Not allowed:

- implicit legal conclusion transfer,
- unrestricted payload sharing without scope justification.

### Tlachia -> Machiyotl

Allowed:

- contextual references that support evidence organization in synthetic/demo flows.

Not allowed:

- automatic conversion of detection signals into confirmed legal outcomes.

### Core Principle

Module boundaries remain strict. Each module owns its domain behavior and exposes only minimal required interfaces.

## 10) Privacy, Safety, and UX Rules

Machiyotl implementations must preserve:

- explicit local-vs-submitted state communication,
- non-sensational language,
- sensitive preview protection by default,
- safe exit behavior in sensitive flows,
- clear human-review notices for assistive outputs.

## 11) Security and Auditability Rules

Machiyotl implementations must:

- support auditable records of sensitive actions,
- avoid exposing secrets or raw sensitive payloads in logs,
- preserve integrity fields for evidence identity,
- remain compatible with future encryption/retention controls.

## 12) Demo vs Production Boundary

In this repository phase, Machiyotl operates under demo-safe assumptions:

- synthetic data only,
- reversible/simulated actions where full workflows are not production-ready,
- mandatory human review,
- no final legal determination.

Any production-grade expansion requires explicit security, legal, institutional, and operational approval documentation.

## 13) Compliance Checklist for Future Changes

Any Machiyotl change must answer yes to all checks:

- Is the change within this charter scope?
- Does it preserve module separation?
- Does it avoid real sensitive data in demo context?
- Does it keep AI/system behavior assistive only?
- Does it preserve auditability and privacy labels?
- Does it avoid legal overclaim?

If any answer is no, the change must be redesigned or rejected.

## 14) Open Questions and Follow-ups

Pending definitions to be addressed in later tasks:

- canonical API contract versioning for Machiyotl endpoints,
- retention windows and deletion policies by environment,
- production-grade cryptographic and storage hardening controls,
- explicit approval workflow artifacts for institutional deployment.

## 15) Traceability Map (Source Alignment)

- Module boundaries and mandatory rules: `AGENTS.md`
- Conceptual architecture and module role: `ARCHITECTURE.md`
- Security and prohibited data baseline: `SECURITY.md`
- UX safety, privacy labels, and Machiyotl flow behavior: `DESIGN.md`
- Demo boundaries and non-goals: `docs/product/frontend-demo-spec.md`
- Current demo implementation status: `frontend/apps/demo/README.md`
- Module placeholder definition: `backend/modules/machiyotl/README.md`
- Existing data structures in repository: `backend/app/db/models.py`
- Existing migration foundation: `backend/migrations/versions/20260515_0001_platform_foundation.py`
