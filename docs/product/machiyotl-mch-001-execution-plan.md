# MCH-001 Execution Plan - Machiyotl Module Charter

## Task Identifier

- Task: `MCH-001`
- Name: Machiyotl Module Charter
- Module: `machiyotl`
- Status: in progress

## Objective

Create and approve a formal module charter for Machiyotl that defines exact responsibilities, boundaries, controls, and interfaces so implementation decisions are consistent across product, backend, frontend, legal/ethics, and security review.

## Why This Task Exists

The repository already has partial implementation signals for Machiyotl (schema, seed records, UI demo screens), but the module still lacks a single authoritative charter that answers:

- what Machiyotl is allowed to do in this phase,
- what Machiyotl must never do,
- what data it can handle,
- how it interfaces with Tlachia and Chimalli,
- and what controls are mandatory before adding real logic.

Without this charter, teams can implement conflicting behavior and violate scope, privacy, and governance constraints.

## Scope

### In Scope

- Create the module charter document under `docs/product/`.
- Define module purpose, non-goals, actor boundaries, and decision rights.
- Define data boundaries and prohibited data handling in this phase.
- Define state vocabulary and lifecycle constraints for evidence records.
- Define cross-module interfaces and prohibited coupling.
- Add acceptance criteria and traceability links to authoritative repository sources.
- Link the charter from `backend/modules/machiyotl/README.md`.

### Out of Scope

- Implementing new API routes or business logic.
- Implementing cryptographic pipeline changes.
- Implementing production auth or legal decision workflows.
- Editing contracts for Chimalli or Tlachia beyond boundary references.

## Inputs and Sources

The charter must be aligned to these sources:

- `AGENTS.md`
- `ARCHITECTURE.md`
- `SECURITY.md`
- `DESIGN.md`
- `docs/product/frontend-demo-spec.md`
- `frontend/apps/demo/README.md`
- `backend/modules/machiyotl/README.md`
- `backend/app/db/models.py`
- `backend/migrations/versions/20260515_0001_platform_foundation.py`

## Deliverables

1. `docs/product/machiyotl-module-charter.md`
2. README reference update in `backend/modules/machiyotl/README.md`
3. Optional cross-reference update in central docs indexes (if required by reviewers)

## Workstreams and Detailed Steps

### Workstream A - Constraint Consolidation

1. Extract all mandatory constraints affecting Machiyotl.
2. Group constraints by category:
   - module boundary,
   - privacy and security,
   - evidence integrity,
   - UX/safety,
   - data governance,
   - demo-vs-production restrictions.
3. Build a source-to-rule map to prevent missing constraints.

Completion signal:
- Every charter rule can be traced to at least one existing repository source.

### Workstream B - Charter Authoring

1. Create a full charter structure with fixed section headings.
2. Fill each section with implementation-oriented language (`must`, `must not`, `allowed`, `prohibited`).
3. Define explicit interface boundaries for inbound and outbound module interactions.
4. Add decision-rights model (human decision, system support, prohibited automation).
5. Add phased maturity statement (current demo-scaffold reality).

Completion signal:
- Another engineer can decide whether a proposed feature belongs in Machiyotl by reading the charter only.

### Workstream C - Governance and Review Readiness

1. Add a checklist section for module acceptance and ongoing compliance.
2. Add traceability matrix that links key statements to sources.
3. Add open-questions section for unresolved decisions and ownership.
4. Ensure language does not invent legal framework or policy outside repository evidence.

Completion signal:
- Product, engineering, and security reviewers can review with explicit pass/fail checks.

### Workstream D - Documentation Integration

1. Update module README to point to the charter as the governing document.
2. Ensure relative links resolve from both GitHub and local markdown previews.

Completion signal:
- Developers entering the module can immediately find the authoritative charter.

## Acceptance Criteria for MCH-001

- A complete charter exists at `docs/product/machiyotl-module-charter.md`.
- Charter has explicit in-scope and out-of-scope boundaries.
- Charter includes data minimization and prohibited data guidance.
- Charter defines cross-module interfaces and prohibited couplings.
- Charter includes a lifecycle/state boundary section for evidence handling.
- Charter includes a demo-vs-production boundary statement.
- Charter includes traceability references to repository sources.
- `backend/modules/machiyotl/README.md` links to the charter.

## Quality Gate Checklist

- No invented legal criteria or jurisdictional rules.
- No language that implies automatic legal determination.
- No language that permits use of real victim/case data in demo context.
- No contradictions with `AGENTS.md`, `ARCHITECTURE.md`, `SECURITY.md`, or `DESIGN.md`.
- All requirements are actionable and testable by reviewers.

## Review Protocol

- Reviewer group 1: backend and frontend maintainers (boundary clarity).
- Reviewer group 2: product owner (scope and execution alignment).
- Reviewer group 3: security/privacy reviewer (controls and prohibited behavior).

Resolution protocol:

1. Collect comments into one revision pass.
2. Resolve contradictions first, style comments second.
3. Update traceability table when language changes.
4. Mark charter as approved only when all blocking comments are closed.

## Completion Evidence

Task `MCH-001` is complete when:

- charter document merged in branch,
- module README points to it,
- acceptance criteria checklist passes,
- and review sign-off is recorded in PR discussion.
