# AI Agent Instructions

This repository contains the initial scaffolding of Yaocihuatl, an institutional platform to address political violence against women on the basis of gender in digital environments.

## Mandatory Rules

- Do not invent legal frameworks, jurisprudence, protocols, or jurisdictional criteria.
- Do not implement sensitive logic without associated technical, legal, and ethical documentation.
- Do not upload real data of victims, aggressors, personal accounts, sensitive evidence, or real case files.
- Do not create invasive scraping or mass surveillance mechanisms.
- Do not access, infer, or attempt to access private communications.
- Maintain strict separation between the `tlachia`, `machiyotl`, and `chimalli` modules.
- Prioritize privacy, auditability, explainability, and human-in-the-loop.
- Do not turn the platform into a censorship tool.
- All AI classification must be assistive, not decision-making.
- All legal functionality must cite versioned legal corpus.
- All evidence must preserve chain of custody.

## Work Criteria

- Before implementing real logic, document assumptions, risks, inputs, outputs, and limits.
- Separate demo, synthetic, anonymized, and real data.
- Use placeholders when legal, technical, or institutional definitions are missing.
- Keep changes small, reviewable, and testable.
- Add tests only when there is real logic to test.

---

## Project Overview

Yaocihuatl is a civic technology platform for detecting, documenting, preserving, and routing cases of digital political violence against women on the basis of gender (VPMRG). The repo is in scaffolding phase: no business logic, real integrations, final models, authentication, functional AI, or scraping is implemented yet.

### Three Core Modules

| Module | Nahuatl Meaning | Product Role | Backend Dir | Frontend App |
|---|---|---|---|---|
| **Tlachia** | Observe | Monitoring, risk detection, alerts | `backend/modules/tlachia/` | `frontend/apps/dashboard/` |
| **Machiyotl** | Seal/Mark | Forensic evidence capture, SHA-256 sealing, PWA | `backend/modules/machiyotl/` | `frontend/apps/pwa-machiyotl/` |
| **Chimalli** | Shield | Legal RAG, entity extraction, jurisdictional routing | `backend/modules/chimalli/` | `frontend/apps/chimalli-chat/` |

### Repository Structure

```
frontend/
  apps/             # Next.js apps: dashboard, pwa-machiyotl, chimalli-chat
  packages/         # Shared: config, types, ui (shadcn/ui components)
backend/
  app/              # FastAPI core: api/, core/, domain/, services/, workers/, schemas/, integrations/
  modules/          # Domain modules: tlachia/, machiyotl/, chimalli/
  migrations/       # Database migrations
docs/               # Institutional, technical, legal, ethical documentation
infra/              # Deployment, Docker, GitHub Actions, observability
datasets/           # demo/, synthetic/, anonymized/ (NEVER real data)
legal-corpus/       # Versioned legal corpus: federal/, baja-california/, international/, jurisprudence/, protocols/
prompts/            # Versioned prompts: chimalli-system, entity-extraction, expediente-generator, jurisdiction-routing, vpmrg-classifier
tests/              # Future test suite
scripts/            # Utility scripts
```

---

## Planned Tech Stack (Not Yet Installed)

- **Frontend:** Next.js, React, TypeScript, Tailwind CSS, shadcn/ui, Radix UI, Lucide React icons
- **Backend:** Python, FastAPI, Pydantic
- **Database:** PostgreSQL with pgvector
- **Workers:** Celery, Redis
- **AI/NLP:** Transformers, spaCy, sentence-transformers, LangChain/LangGraph
- **PWA/Forensics:** Web Crypto API, IndexedDB, Workbox
- **Infra:** Docker, GitHub Actions

---

## Build / Lint / Test Commands

The project is in scaffolding phase with no dependencies installed yet. Once the stack is initialized, expected commands are:

### Frontend (Next.js monorepo)
```bash
npm install                   # Install dependencies
npm run dev                   # Start dev server
npm run build                 # Production build
npm run lint                  # Run ESLint
npm run typecheck             # Run TypeScript type checking
npm run test                  # Run all tests
npm run test -- --grep "pattern"   # Run tests matching pattern
```

### Backend (FastAPI)
```bash
python -m venv .venv && source .venv/bin/activate   # Create and activate virtualenv
pip install -r requirements.txt                      # Install dependencies
uvicorn app.api:app --reload                        # Start dev server
pytest                                              # Run all tests
pytest tests/test_file.py::test_name                # Run a single test
pytest tests/test_file.py -k "pattern"              # Run tests matching pattern
ruff check .                                        # Lint with ruff
ruff format .                                       # Format with ruff
mypy app/                                           # Type check with mypy
```

### Docker
```bash
docker compose up --build      # Start all services
docker compose down            # Stop all services
```

> **Important:** Do NOT add `package.json`, `pyproject.toml`, or install dependencies until the relevant module's specification and boundaries are documented. Keep the scaffolding clean.

---

## Code Style Guidelines

### General

- Use English for code, commit messages, and technical documentation.
- Use Spanish for UI text, microcopy, and legal/institutional content (see DESIGN.md for voice and tone).
- No comments in code unless explicitly asked.
- Keep changes small and reviewable.
- Follow the commit convention: `type(module): short description` (see `.opencode/agents/commit.md`).

### Frontend (TypeScript / React / Next.js)

- Use TypeScript strict mode. No `any` types.
- Use functional components with hooks. No class components.
- Use named exports by default. Default exports only for Next.js pages.
- Use `interface` for object shapes, `type` for unions and utilities.
- File naming: `kebab-case.tsx` for components, `kebab-case.ts` for utilities.
- Component naming: PascalCase matching the design system (e.g., `EvidenceCard`, `HashBlock`, `PanicExitButton`).
- Use semantic props: `variant`, `size`, `state` — never raw color props.
- Use CSS variables (design tokens) from `DESIGN.md`. Never hardcode colors outside the token file.
- Use Tailwind with CSS variable mapping (see DESIGN.md section 18).
- Import order: React/Next → third-party → local components → local utilities → types.
- Use shadcn/ui + Radix UI for accessible primitives. Restyle with tokens.
- Use Lucide React for icons.
- Target WCAG 2.2 AA: contrast 4.5:1 text, 3:1 large/icons, visible focus rings, 44px touch targets.
- Respect `prefers-reduced-motion`.

### Backend (Python / FastAPI)

- Target Python 3.11+.
- Use Pydantic v2 for schemas and validation.
- Use `snake_case` for files, functions, variables.
- Use `PascalCase` for classes and Pydantic models.
- Use `UPPER_SNAKE_CASE` for constants.
- Import order: stdlib → third-party → local (separated by blank lines).
- Use `async` for I/O-bound routes and services.
- Use type hints on all function signatures.
- Use `ruff` for linting and formatting (line length: 88).
- Use `mypy` for type checking with strict settings.
- Keep API routes thin — delegate logic to service layer.
- Separate domain logic from infrastructure in `app/domain/`.

### Error Handling

- Frontend: Show user-facing errors per DESIGN.md section 20.3 — explain what happened, whether data is safe, and what to do next. Never blame the user.
- Backend: Use structured error responses with Pydantic. Never expose internal tracebacks to clients.
- Always distinguish between "local-only" and "network" failures for evidence flows.
- Use specific exception classes, never bare `except:`.

### Naming Conventions

- **Modules:** Nahuatl names (`tlachia`, `machiyotl`, `chimalli`) — lowercase in code and directories.
- **Legal references:** Always cite source, version, date, and location in `legal-corpus/`.
- **Evidence states:** Use the defined state vocabulary from DESIGN.md (e.g., `sealed-local`, `ready`, `submitted`).
- **Risk levels:** Use `low`, `medium`, `high`, `unclassified` — never `confirmed` for AI-detected patterns.
- **UI terms:** Follow the preferred terminology in DESIGN.md section 12.3 (e.g., "mujer protegida" not "usuaria vulnerable").

---

## Key References

| File | Purpose |
|---|---|
| `DESIGN.md` | Design system, visual style, components, accessibility, microcopy |
| `ARCHITECTURE.md` | Conceptual architecture, layers, modules, cross-cutting services |
| `SECURITY.md` | Security principles, prohibited data, privacy by design |
| `CONTRIBUTING.md` | Contribution rules and workflow |
| `CLAUDE.md` | Additional context for coding agents |
| `.opencode/agents/commit.md` | Commit message format convention |

---

## Critical Reminders

- This is a **scaffolding** repo. Do not implement advanced logic without explicit specification.
- Do not connect real APIs, create definitive endpoints, or implement authentication yet.
- Do not implement AI, scraping, or real social media connections in this phase.
- Any legal change must cite source, version, date, and location in `legal-corpus/`.
- Any evidence flow must preserve chain of custody and auditability.
- When uncertain, choose: more readable, more respectful, more private, more explicit about consent, more transparent about AI limitations, more accessible, less visually dramatic.
