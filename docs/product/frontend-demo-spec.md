# Frontend Demo Specification

This document defines the scope and boundaries for the initial Yaocihuatl frontend demo.

## Purpose

Build a navigable, mock-only product experience for hackathon demonstration. The demo shows how Yaocihuatl could support institutional monitoring, local evidence sealing, guided orientation, review, and public aggregate transparency.

## Scope

- A Next.js App Router demo application under `frontend/apps/demo`.
- Mock data only, centralized in frontend code.
- Visual flows for Tlachia, Machiyotl, Chimalli, institutional review, public verification, privacy settings, and safe exit.
- Reusable UI components aligned to `DESIGN.md`.
- Static and client-side simulated interactions only.

## Explicit Non-Goals

- No backend integration.
- No authentication or authorization.
- No real AI, RAG, entity extraction, classification, scraping, or surveillance.
- No legal determination, jurisdictional decision, or official routing.
- No real file upload, hash generation, PDF generation, or evidence submission.
- No real data from protected women, personal accounts, public figures, or case files.

## Assumptions

- Product roles, module boundaries, and conceptual flow are based on existing repository documentation.
- All names, platforms, hashes, timestamps, municipalities, accounts, alerts, and cases are fictitious and anonymized.
- UI labels prefer Spanish because the demo is user-facing and institution-facing.
- AI content is always framed as assistive and pending human review.

## Inputs

- Synthetic role selections.
- Synthetic evidence metadata.
- Synthetic alerts and cases.
- Mock chat replies.
- Mock public aggregate metrics.

## Outputs

- Visual navigation states.
- Mock evidence cards, hash blocks, timelines, charts, and review panels.
- Simulated export, send, copy, and verification states.

## Risks and Mitigations

- Risk: The demo could be misunderstood as a real complaint or legal determination system.
  Mitigation: The UI repeatedly labels actions as demo, simulated, assistive, and requiring human review.

- Risk: Sensitive evidence could appear exposed in a demo.
  Mitigation: Evidence thumbnails are blurred or represented with neutral placeholders.

- Risk: AI suggestions could be interpreted as final decisions.
  Mitigation: AI badges, warnings, and review panels state that the authority must validate.

- Risk: Public dashboards could expose small groups.
  Mitigation: Public views show only aggregated, anonymized metrics and explain k-anonymity in plain language.

## Module Boundaries

- Tlachia screens display institutional monitoring and explainability mocks only.
- Machiyotl screens display local evidence capture and sealing mocks only.
- Chimalli screens display guided orientation and routing suggestions only.
- Cross-module views such as evidence kit and case review present copied mock data without shared backend state.
