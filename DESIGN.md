# DESIGN.md — Yaocíhuatl

Design system and implementation rules for the Yaocíhuatl web platform.

This document is the single source of truth for visual design, interaction behavior, layout, tone, components, accessibility, and UI implementation. Any model, agent, developer, or designer working on this system must follow these rules unless explicitly instructed otherwise.

---

## 1. Product Identity

### 1.1 Product Name

**Yaocíhuatl**

Meaning: woman warrior.

The product is a civic technology platform for detecting, documenting, preserving, and routing cases related to digital political violence against women in gender-based contexts.

### 1.2 Core Modules

The system is divided into three product areas. Each area must feel part of the same product while having a clear visual role.

| Module | Meaning | Product Role | Visual Personality |
|---|---|---|---|
| **Tlachia** | Observe | Institutional monitoring and risk detection | Analytical, precise, calm, dashboard-oriented |
| **Machiyotl** | Seal / mark | Mobile-first forensic evidence capture | Private, safe, focused, step-by-step |
| **Chimalli** | Shield | Conversational guidance and routing | Supportive, clear, human, protective |

### 1.3 Brand Positioning

Yaocíhuatl must look like a serious civic, legal, and technological system. It must not look like a generic social media app, activist poster, wellness app, or police tool.

The interface must communicate:

- Institutional trust
- Emotional safety
- Procedural clarity
- Technical reliability
- Privacy by design
- Human oversight
- Non-revictimizing guidance

### 1.4 Product Personality

Use these traits consistently:

| Trait | UI Translation |
|---|---|
| Protective | Soft surfaces, clear confirmations, visible privacy controls |
| Institutional | Structured layouts, restrained color, precise labels |
| Human | Warm microcopy, respectful language, plain explanations |
| Technical | Hashes, timestamps, evidence metadata, audit states shown clearly |
| Discreet | No sensational visuals, no aggressive red-heavy screens, no dramatic imagery |
| Accessible | High contrast, readable text, strong focus states, simple navigation |

---

## 2. Design Principles

### 2.1 Dignity First

Every screen must preserve the dignity of the user. Do not use alarming, graphic, punitive, or sensational language. The system must feel like a safe institutional assistant, not a hostile investigation environment.

**Use:**

- “Tu evidencia está guardada en este dispositivo.”
- “Puedes revisar antes de enviar.”
- “La decisión final corresponde a la autoridad competente.”

**Avoid:**

- “Caso grave detectado.”
- “Agresor identificado.”
- “Denuncia enviada automáticamente.”
- “Víctima vulnerable.”

### 2.2 Agency and Consent

The user must always understand what is happening and must explicitly approve sensitive actions.

Required rules:

- Never upload evidence automatically.
- Never imply that the AI decides legal validity.
- Always show a clear review step before submission.
- Always distinguish “guardado localmente” from “enviado a autoridad”.
- Always provide an exit or pause path in victim-facing flows.

### 2.3 Calm Clarity

Use concise layouts and strong hierarchy. The interface must reduce cognitive load during stressful situations.

Required rules:

- One primary action per screen.
- Critical flows must be step-based.
- Avoid dense paragraphs in app screens.
- Use progressive disclosure for legal or technical details.
- Show status in plain language before showing technical metadata.

### 2.4 Evidence Integrity Without Intimidation

Technical information must be visible, but not overwhelming.

Display forensic details as structured metadata blocks:

- File name
- Source platform
- Capture date and time
- Local hash
- Device status
- Upload status
- Chain of custody step

Do not show long hashes as the main focus. Truncate them by default and provide a copy button.

Example:

```txt
SHA-256
9f2a7c...d18b40
[Copiar hash]
```

### 2.5 Human-in-the-Loop

The system must clearly communicate that AI assists, organizes, and suggests. It must never visually imply that AI determines truth, guilt, sanctions, or admissibility.

Required labels:

- “Sugerencia generada por IA”
- “Pendiente de revisión humana”
- “Requiere validación de autoridad”
- “No sustituye asesoría legal”

### 2.6 Discretion and Safety

Victim-facing screens must support discreet use.

Required rules:

- Include a panic action on sensitive pages.
- Panic action must be visible enough to find, but not visually loud.
- Avoid page titles that expose sensitive content in public contexts.
- Avoid browser-facing labels that expose “denuncia” or “violencia” in mobile quick views when possible.
- Use neutral loading and transition labels.

---

## 3. Visual Style

### 3.1 Overall Visual Direction

The interface should feel modern, soft, and institutional. Use a refined dashboard/application style with rounded geometry, spacious layouts, subtle shadows, and calm color blocking.

Preferred style:

- Light-first interface
- Soft lavender and off-white backgrounds
- Deep purple for authority and hierarchy
- Magenta/plum for brand emphasis
- Teal/green for protection, confirmation, and certified states
- Amber for caution
- Red only for destructive or urgent risk states

Avoid:

- Neon gradients
- Overly saturated purple backgrounds on full screens
- Heavy black sections unless used for specific dashboard contrast
- Comic illustration style
- Stock photos of distressed women
- Aggressive red alert systems
- Police/criminal visual language

### 3.2 Surface Model

Use layered surfaces:

| Layer | Purpose | Token |
|---|---|---|
| App background | Global page background | `--background` |
| Soft section | Lavender-tinted regions | `--surface-soft` |
| Elevated card | Main content cards | `--surface-card` |
| Raised panel | Dashboards/modals | `--surface-raised` |
| Overlay | Modal/backdrop | `--overlay` |

Rules:

- Cards must have clear separation through border and shadow, not heavy outlines.
- Dashboard panels may use denser layouts, but must preserve whitespace.
- Mobile flows should use full-width cards and bottom action bars.

---

## 4. Color System

### 4.1 Core Tokens

Use semantic tokens. Do not hardcode raw colors in components except inside the token definition file.

```css
:root {
  /* Brand */
  --brand-950: #1B0B25;
  --brand-900: #2A1038;
  --brand-800: #421557;
  --brand-700: #5B1D75;
  --brand-600: #742B8F;
  --brand-500: #8D3AA7;
  --brand-400: #B461C6;
  --brand-300: #D998E2;
  --brand-200: #EEC9F2;
  --brand-100: #F8E6FA;
  --brand-50:  #FCF4FD;

  /* Supportive accent */
  --accent-plum: #7A1E4D;
  --accent-rose: #F7D8EF;
  --accent-lilac: #EFE1F4;
  --accent-mint: #DDEDD7;

  /* Semantic */
  --success-700: #176B56;
  --success-600: #21806A;
  --success-100: #DDF3EB;
  --warning-700: #9A5B00;
  --warning-100: #FFF1CC;
  --danger-700: #9F1D35;
  --danger-100: #FBE1E7;
  --info-700: #285C8A;
  --info-100: #E1F0FB;

  /* Neutral */
  --neutral-950: #131117;
  --neutral-900: #1E1A23;
  --neutral-800: #2B2630;
  --neutral-700: #433B49;
  --neutral-600: #5F5468;
  --neutral-500: #7B7183;
  --neutral-400: #A49BAA;
  --neutral-300: #C9C2CE;
  --neutral-200: #E3DDE7;
  --neutral-100: #F1EDF4;
  --neutral-50:  #FAF8FB;

  /* App surfaces */
  --background: #FBF8FC;
  --foreground: #1E1A23;
  --surface-soft: #F7EAF8;
  --surface-card: #FFFFFF;
  --surface-raised: #FFFFFF;
  --border: #E3DDE7;
  --border-strong: #C9C2CE;
  --overlay: rgba(19, 17, 23, 0.52);

  /* Interactive */
  --primary: #5B1D75;
  --primary-hover: #742B8F;
  --primary-active: #421557;
  --primary-foreground: #FFFFFF;

  --secondary: #EFE1F4;
  --secondary-hover: #E7D2ED;
  --secondary-foreground: #421557;

  --focus-ring: #B461C6;
}
```

### 4.2 Semantic Color Rules

| Use Case | Color | Rule |
|---|---|---|
| Primary action | `--primary` | Used only once per screen when possible |
| Secondary action | `--secondary` | Used for safe alternatives |
| Certified / sealed / saved | `--success-*` | Used for completed evidence states |
| Warning / needs review | `--warning-*` | Used for missing metadata, incomplete fields |
| Danger / destructive | `--danger-*` | Used sparingly for delete, urgent risk, or irreversible actions |
| Informational | `--info-*` | Used for explanations and neutral guidance |
| AI suggestion | Brand/lilac treatment | Never use success or legal-looking finality |

### 4.3 Risk Colors

Risk must not rely only on color. Always include label and icon.

| Risk Level | Label | Color | Icon | Usage |
|---|---|---|---|---|
| Low | Bajo | Green/teal | ShieldCheck | Low activity, no immediate action |
| Medium | Medio | Amber | AlertCircle | Needs review |
| High | Alto | Red/plum | AlertTriangle | Urgent analyst review |
| Unknown | Sin clasificar | Neutral | CircleHelp | Insufficient data |

Do not display “High Risk” as a full red page. Use a contained badge/card treatment.

### 4.4 Color Accessibility

All text must meet:

- Normal text: minimum contrast ratio **4.5:1**.
- Large text and icons: minimum contrast ratio **3:1**.
- Interactive component boundaries: minimum contrast ratio **3:1** against surrounding surface.
- Placeholder text must be readable and cannot be the only label.

Do not use pale lilac text over white. Use pale lilac only as background or decoration.

---

## 5. Typography

### 5.1 Font Stack

Use modern system-native typography. Prioritize legibility and platform consistency.

```css
--font-sans: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
--font-display: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
--font-mono: "JetBrains Mono", "SF Mono", Consolas, ui-monospace, monospace;
```

Rules:

- Use `Inter` if available.
- Use system UI fallback for speed and consistency.
- Use monospace only for hashes, IDs, timestamps, and technical metadata.
- Do not use decorative typefaces.
- Do not use all caps for long labels.

### 5.2 Type Scale

```css
--text-xs: 0.75rem;      /* 12px */
--text-sm: 0.875rem;     /* 14px */
--text-base: 1rem;       /* 16px */
--text-lg: 1.125rem;     /* 18px */
--text-xl: 1.25rem;      /* 20px */
--text-2xl: 1.5rem;      /* 24px */
--text-3xl: 1.875rem;    /* 30px */
--text-4xl: 2.25rem;     /* 36px */
--text-5xl: 3rem;        /* 48px */
```

### 5.3 Typography Roles

| Role | Size | Weight | Line Height | Use |
|---|---:|---:|---:|---|
| Display | 48px | 700 | 1.05 | Landing hero only |
| Page title | 30–36px | 700 | 1.15 | Main page headers |
| Section title | 24px | 700 | 1.2 | Content sections |
| Card title | 18–20px | 650 | 1.3 | Cards and panels |
| Body | 16px | 400 | 1.6 | Main reading text |
| Body strong | 16px | 600 | 1.5 | Emphasis |
| Supporting | 14px | 400 | 1.5 | Help text and metadata |
| Label | 14px | 600 | 1.2 | Form labels |
| Caption | 12px | 500 | 1.3 | Badges, timestamps, table helpers |
| Code/meta | 13px | 500 | 1.4 | Hashes and IDs |

### 5.4 Text Width

- Long-form text max width: `680px`.
- Legal explanations max width: `760px`.
- Dashboard cards may be wider but must use headings, labels, and spacing.
- Chat messages max width: `72ch` on desktop and `calc(100vw - 48px)` on mobile.

---

## 6. Spacing, Radius, and Elevation

### 6.1 Spacing Scale

Use an 8-point spacing system.

```css
--space-1: 0.25rem;  /* 4px */
--space-2: 0.5rem;   /* 8px */
--space-3: 0.75rem;  /* 12px */
--space-4: 1rem;     /* 16px */
--space-5: 1.25rem;  /* 20px */
--space-6: 1.5rem;   /* 24px */
--space-8: 2rem;     /* 32px */
--space-10: 2.5rem;  /* 40px */
--space-12: 3rem;    /* 48px */
--space-16: 4rem;    /* 64px */
--space-20: 5rem;    /* 80px */
```

### 6.2 Layout Spacing Rules

- Page horizontal padding mobile: `16px`.
- Page horizontal padding tablet: `24px`.
- Page horizontal padding desktop: `32px–48px`.
- Section vertical spacing: `48px–80px`.
- Card internal padding: `20px–24px`.
- Dense dashboard card padding: `16px–20px`.
- Form field gap: `16px`.
- Button group gap: `12px`.

### 6.3 Radius Scale

```css
--radius-xs: 0.375rem;  /* 6px */
--radius-sm: 0.5rem;    /* 8px */
--radius-md: 0.75rem;   /* 12px */
--radius-lg: 1rem;      /* 16px */
--radius-xl: 1.5rem;    /* 24px */
--radius-full: 9999px;
```

Rules:

- Buttons: `12px` radius.
- Cards: `16px` radius.
- Large hero panels: `24px` radius.
- Badges: full radius.
- Avoid sharp institutional boxes unless rendering formal documents.

### 6.4 Elevation

```css
--shadow-sm: 0 1px 2px rgba(19, 17, 23, 0.06);
--shadow-md: 0 8px 24px rgba(19, 17, 23, 0.08);
--shadow-lg: 0 16px 48px rgba(19, 17, 23, 0.12);
```

Rules:

- Use shadows subtly.
- Use borders more than heavy shadows.
- Modals and floating panels may use `--shadow-lg`.
- Dashboard widgets should use `--shadow-sm` or no shadow with border.

---

## 7. Layout System

### 7.1 Breakpoints

```css
--breakpoint-sm: 640px;
--breakpoint-md: 768px;
--breakpoint-lg: 1024px;
--breakpoint-xl: 1280px;
--breakpoint-2xl: 1536px;
```

### 7.2 Containers

| Container | Max Width | Use |
|---|---:|---|
| `container-readable` | 760px | Articles, forms, legal guidance |
| `container-standard` | 1120px | Landing sections, settings |
| `container-dashboard` | 1440px | Dashboards and data-heavy layouts |
| `container-full` | 100% | App shell |

### 7.3 App Shell

Authenticated app layout:

```txt
┌────────────────────────────────────────────┐
│ Top bar: product, role, status, panic       │
├──────────────┬─────────────────────────────┤
│ Sidebar      │ Main content                 │
│ Navigation   │ Header + workspace           │
└──────────────┴─────────────────────────────┘
```

Mobile authenticated layout:

```txt
┌────────────────────────┐
│ Compact top bar         │
├────────────────────────┤
│ Main content            │
├────────────────────────┤
│ Bottom navigation       │
└────────────────────────┘
```

Rules:

- Sidebar is for authority and analyst roles.
- Bottom navigation is for victim-facing mobile flows.
- Panic action is always in the top-right or bottom-right safe zone on sensitive screens.
- Keep the app shell neutral and consistent across modules.

### 7.4 Grid Rules

- Landing: 12-column desktop grid, 4-column mobile grid.
- Dashboard: flexible CSS grid with 12 columns desktop, 6 columns tablet, 1 column mobile.
- Forms: single-column by default. Use two columns only for non-sensitive administrative fields.
- Evidence capture: single-column, step-by-step, mobile-first.

---

## 8. Navigation

### 8.1 Global Navigation Items

Use role-based navigation. Do not show unavailable sections to users without access.

Protected user:

- Inicio
- Capturar evidencia
- Mis evidencias
- Chimalli
- Kit de evidencia
- Configuración de privacidad

Authority / analyst:

- Panel Tlachia
- Alertas
- Casos recibidos
- Expedientes
- Reportes agregados
- Configuración institucional

Judge / read-only reviewer:

- Expedientes asignados
- Evidencia verificable
- Historial de revisión

Public observer:

- Datos agregados
- Tendencias
- Metodología

### 8.2 Navigation Rules

- Current page must have clear active state.
- Use icons only with labels.
- Do not rely on color alone for active state.
- Sensitive user flows should minimize navigation options to prevent accidental exits.
- Use breadcrumbs in authority workflows and evidence review screens.

---

## 9. Component System

### 9.1 Buttons

#### Primary Button

Use for the main action on a screen.

Visual:

- Background: `--primary`
- Text: white
- Radius: `12px`
- Height: `44px` desktop, `48px` mobile
- Font: 14–16px, weight 600

Examples:

- “Continuar”
- “Guardar evidencia”
- “Revisar expediente”
- “Enviar a revisión”

Rules:

- Only one primary button per screen or card section.
- Do not use primary for destructive actions.
- Do not use vague labels like “Aceptar” if a specific verb is possible.

#### Secondary Button

Use for safe alternatives.

Examples:

- “Guardar borrador”
- “Volver”
- “Editar información”
- “Copiar hash”

#### Destructive Button

Use only for irreversible actions.

Visual:

- Background: `--danger-700` or white with danger border
- Must open confirmation dialog before execution

Examples:

- “Eliminar evidencia local”
- “Cancelar envío”

#### Panic Button

The panic action must be a reusable component.

Default visual:

- Small ghost or secondary button
- Icon: `LogOut`, `Shield`, or `EyeOff`
- Label: “Salida rápida”
- Position: top-right in desktop, bottom-right floating in mobile

Behavior:

- Immediately redirects to a neutral page.
- Clears sensitive in-memory state.
- Does not display dramatic animation.
- Must be keyboard accessible.

### 9.2 Cards

Default card:

```txt
Card
- background: --surface-card
- border: 1px solid --border
- radius: --radius-lg
- padding: 20–24px
- shadow: --shadow-sm
```

Card anatomy:

```txt
[Optional icon/badge]
Title
Supporting description
Main content
Footer actions/status
```

Rules:

- Cards must have a clear title.
- Avoid cards inside cards unless necessary.
- Use section dividers for dense metadata.
- Keep icons decorative but meaningful.

### 9.3 Forms

Form fields must include:

- Visible label
- Optional helper text
- Input
- Error text when needed
- Accessible `aria-describedby`

Input visual:

- Height: `44px–48px`
- Radius: `12px`
- Border: `--border-strong`
- Focus ring: `2px solid --focus-ring`
- Background: white

Error state:

- Border: `--danger-700`
- Helper text: `--danger-700`
- Include icon or text prefix

Do not use placeholder text as the only label.

### 9.4 Badges

Badge types:

| Type | Example | Visual |
|---|---|---|
| Status | “Guardado local” | Neutral |
| Certified | “Sellado” | Success |
| Pending | “Pendiente de revisión” | Warning |
| AI | “Sugerencia IA” | Brand/lilac |
| Risk | “Riesgo alto” | Semantic risk color |
| Privacy | “No enviado” | Neutral or success |

Badge rules:

- Use short labels.
- Pair icons with critical badges.
- Never use “Verificado” unless a real verification process occurred.

### 9.5 Alerts

Alert variants:

- Info
- Success
- Warning
- Danger
- Privacy
- AI suggestion

Alert anatomy:

```txt
Icon
Title
Description
Optional action
```

Rules:

- Alerts must be specific and actionable.
- Avoid permanent red alerts on victim-facing flows.
- Use warning for incomplete steps, not danger.

### 9.6 Modals and Dialogs

Use dialogs for:

- Confirmation before sending evidence
- Deleting local evidence
- Explaining privacy or legal disclaimers
- Leaving a partially completed flow

Dialog rules:

- Title must clearly state the decision.
- Body must explain consequences in plain language.
- Primary action should be safe or progressive.
- Destructive actions must be visually distinct.
- Always include cancel/close.

### 9.7 Evidence Item Component

Required fields:

```txt
EvidenceCard
- thumbnail or file icon
- evidence title or source
- source platform
- capture timestamp
- local status
- hash preview
- upload status
- chain step
- actions: view, copy hash, add note, remove
```

States:

| State | Label | Visual |
|---|---|---|
| Draft | “Sin sellar” | Neutral |
| Sealed local | “Sellado local” | Success |
| Ready | “Listo para revisar” | Info |
| Submitted | “Enviado a revisión” | Success/Info |
| Error | “Requiere atención” | Warning/Danger depending on severity |

Do not show image previews by default if they may contain sensitive content. Use blurred thumbnail or generic file card until the user taps “Ver”.

### 9.8 Hash Block Component

Use for technical evidence identity.

```txt
HashBlock
- Algorithm label: SHA-256
- Short hash: first 6 + last 6 characters
- Copy button
- Expand button
- Tooltip: “Identificador criptográfico de este archivo”
```

Rules:

- Use monospace font.
- Truncate by default.
- Copy action must show “Hash copiado”.
- Do not make the hash the visual hero of the card.

### 9.9 Timeline Component

Use for chain of custody and procedural progress.

Timeline item anatomy:

```txt
Status icon
Step title
Timestamp
Actor/system
Description
```

Required steps:

- Captura iniciada
- Evidencia sellada
- Metadatos revisados
- Expediente generado
- Enviado a revisión
- Recibido por autoridad

### 9.10 Chat Component

Chimalli chat must look supportive and procedural, not casual.

Rules:

- Assistant messages align left.
- User messages align right.
- Use soft surfaces, not bright chat bubbles.
- Always provide quick reply chips for stressful decisions.
- Long legal explanations must collapse behind “Ver explicación”.
- AI suggestions must be labeled.
- Never produce aggressive or emotionally charged phrasing.

Suggested quick replies:

- “Agregar evidencia”
- “No sé qué autoridad corresponde”
- “Necesito guardar y continuar después”
- “Quiero revisar antes de enviar”
- “Explicarlo en palabras simples”

### 9.11 Dashboard Metric Cards

Use for Tlachia and authority panels.

Metric card anatomy:

```txt
Title
Primary number
Delta/trend
Context label
Optional sparkline
```

Rules:

- Never display personal victim identifiers in public or aggregated dashboards.
- Use aggregated metrics by default.
- Risk metrics must include date range and data source.
- Always distinguish “alertas” from “casos confirmados”.

### 9.12 Tables

Use tables for authority workflows, case lists, evidence lists, and audit logs.

Rules:

- Provide search and filters.
- Use sticky headers for large tables.
- Allow sorting only on clear columns.
- Sensitive columns must be hidden by default when not necessary.
- Use row actions in a final actions column.
- Provide empty, loading, and error states.

---

## 10. Icons and Illustration

### 10.1 Icon Style

Use a single outline icon set across the product.

Recommended icon style:

- Stroke width: 1.75–2px
- Rounded line caps
- Simple geometry
- No filled multicolor icons in core UI

Recommended icon concepts:

| Concept | Icon |
|---|---|
| Protection | Shield, ShieldCheck |
| Evidence | FileCheck, FileLock |
| Hash | Fingerprint, KeyRound |
| Alert | AlertCircle, AlertTriangle |
| AI suggestion | Sparkles, Bot |
| Privacy | Lock, EyeOff |
| Timeline | Clock, History |
| Dashboard | BarChart, Activity |
| Routing | Route, MapPinned |

### 10.2 Illustration Style

Use illustrations sparingly.

Allowed style:

- Geometric vector illustration
- Soft shadows
- Diverse women in empowered, calm, professional contexts
- Abstract protective shapes
- Civic/institutional scenes

Avoid:

- Crying or distressed women
- Bruising, harassment screenshots, or explicit abuse visuals
- Police imagery
- Courtroom drama clichés
- Decorative visuals that trivialize the topic

### 10.3 Empty States

Empty states must be calm and useful.

Example:

```txt
Aún no hay evidencia guardada
Cuando captures una publicación, aparecerá aquí con su sello local y fecha de captura.
[Capturar evidencia]
```

---

## 11. Motion and Interaction

### 11.1 Motion Principles

Motion must support comprehension, not decoration.

Use motion for:

- Step transitions
- Toast confirmations
- Expanding technical details
- Loading states
- Highlighting newly added evidence

Avoid:

- Bouncy playful motion
- Dramatic warning animations
- Constant pulsing alerts
- Excessive parallax

### 11.2 Timing

```css
--duration-fast: 120ms;
--duration-base: 180ms;
--duration-slow: 260ms;
--ease-standard: cubic-bezier(0.2, 0, 0, 1);
--ease-emphasized: cubic-bezier(0.2, 0, 0, 1);
```

### 11.3 Reduced Motion

Respect `prefers-reduced-motion`.

When reduced motion is enabled:

- Remove page transition animations.
- Replace sliding panels with instant state changes.
- Keep opacity transitions under 100ms or remove them.

---

## 12. Content and Microcopy

### 12.1 Voice

The voice must be:

- Clear
- Respectful
- Calm
- Direct
- Non-judgmental
- Procedural when needed
- Human without being informal

### 12.2 Writing Rules

Use plain Spanish by default.

Rules:

- Prefer “persona” and “mujer protegida” over “víctima” in general UI.
- Use “víctima” only in legal/procedural contexts where necessary.
- Do not blame the user for missing information.
- Avoid passive-aggressive validation messages.
- Explain technical terms when first introduced.
- Avoid legal jargon in primary flows.

### 12.3 Preferred Terms

| Use | Avoid |
|---|---|
| Mujer protegida | Usuaria vulnerable |
| Evidencia | Prueba incriminatoria |
| Persona señalada | Agresor, culpable |
| Autoridad competente | Tribunal correcto, fiscalía correcta |
| Sugerencia de canalización | Decisión legal |
| En revisión | Caso ganado/perdido |
| Sellado local | Prueba definitiva |
| Enviar a revisión | Denunciar automáticamente |

### 12.4 Button Copy

Good labels:

- “Capturar evidencia”
- “Guardar localmente”
- “Sellar evidencia”
- “Revisar antes de enviar”
- “Generar kit”
- “Copiar hash”
- “Solicitar orientación”
- “Continuar después”

Avoid:

- “OK”
- “Aceptar”
- “Procesar”
- “Mandar”
- “Validar delito”
- “Confirmar agresor”

### 12.5 Error Messages

Error messages must explain:

1. What happened.
2. Whether data is safe.
3. What the user can do next.

Example:

```txt
No se pudo completar el sellado
Tu archivo sigue guardado en este dispositivo. Revisa tu almacenamiento disponible e inténtalo nuevamente.
```

---

## 13. Accessibility Requirements

### 13.1 Required Standard

Design and implementation must target WCAG 2.2 AA.

Minimum requirements:

- Text contrast: 4.5:1.
- Large text and meaningful icons: 3:1.
- Visible keyboard focus on all interactive elements.
- All controls reachable by keyboard.
- Form fields connected to labels.
- Error messages announced to screen readers.
- Touch targets at least 44px high/wide.
- No information conveyed by color alone.
- Reduced motion support.
- Meaningful page titles and landmarks.

### 13.2 Focus States

Focus ring:

```css
:focus-visible {
  outline: 2px solid var(--focus-ring);
  outline-offset: 2px;
}
```

Rules:

- Never remove focus outlines without replacement.
- Focus order must follow visual order.
- Modals must trap focus and restore it when closed.

### 13.3 Screen Reader Labels

Required examples:

```tsx
<button aria-label="Copiar hash SHA-256 de la evidencia">
<button aria-label="Salida rápida de la pantalla actual">
<section aria-labelledby="evidence-summary-title">
```

### 13.4 Forms

- Every input must have a visible label.
- Required fields must be marked in text, not only with `*`.
- Use `aria-invalid` for fields with errors.
- Use `aria-describedby` for helper and error text.

---

## 14. Privacy and Safety UI Rules

### 14.1 Privacy Labels

Every sensitive action must display one of these labels:

| State | Label |
|---|---|
| Local only | “Solo en este dispositivo” |
| Not uploaded | “No enviado” |
| Encrypted | “Cifrado” |
| Ready to send | “Listo para revisión” |
| Submitted | “Enviado a autoridad” |
| Deleted locally | “Eliminado de este dispositivo” |

### 14.2 Evidence Upload Rules

Before upload, show a review screen with:

- Evidence list
- Metadata summary
- What will be sent
- Who may receive it
- What remains local
- Confirmation checkbox
- Primary action: “Enviar a revisión”

Do not upload on file selection.

### 14.3 Consent Screen Rules

Consent must be explicit and readable.

Required layout:

```txt
Title
Short plain-language explanation
What the system can do
What the system cannot do
Data handling summary
Consent checkbox list
Primary action
Secondary action
```

Required checkboxes:

- “Entiendo qué información será utilizada.”
- “Entiendo que puedo revisar antes de enviar.”
- “Autorizo el tratamiento de mis datos para este flujo.”

### 14.4 Panic Mode Rules

Panic mode must:

- Redirect immediately to a neutral page.
- Clear visible sensitive state.
- Stop active camera/screen capture if running.
- Avoid confirmation dialog.
- Be accessible from keyboard.

Do not label it “pánico”. Use “Salida rápida”.

---

## 15. Data Visualization

### 15.1 General Rules

Data visualization must be restrained, explanatory, and auditable.

Rules:

- Always label axes.
- Always show date range.
- Always show source context.
- Always distinguish detected patterns from confirmed cases.
- Do not use 3D charts.
- Do not use decorative gradients in charts.
- Do not expose personal data in aggregated views.

### 15.2 Chart Types

| Use Case | Chart Type |
|---|---|
| Alerts over time | Line chart or area chart |
| Risk distribution | Stacked bar or segmented cards |
| Platform distribution | Bar chart |
| Cluster relationships | Network graph with cautious labeling |
| Case funnel | Step/funnel cards |
| Geographic aggregation | Region map only with sufficient anonymity |

### 15.3 Dashboard Color Rules

- Use brand purple for primary series.
- Use teal for certified or resolved states.
- Use amber for pending review.
- Use red only for high-risk or urgent patterns.
- Provide text labels and legends.

---

## 16. Screen Specifications

### 16.1 Landing Page

Goal: explain the platform clearly and establish trust.

Required sections:

1. Hero
2. Three-module explanation
3. How it works
4. Privacy and consent summary
5. Institutional use cases
6. Accessibility/safety statement
7. Call to action

Hero layout:

```txt
[Badge: Plataforma de protección digital]
Title: Yaocíhuatl
Subtitle: Detecta, sella y canaliza evidencia de violencia política digital de género.
Primary CTA: Iniciar orientación
Secondary CTA: Ver cómo funciona
Right side: abstract shield/evidence illustration or product preview
```

Rules:

- Keep hero calm and civic.
- Avoid long legal paragraphs.
- Show the three modules as distinct cards.

### 16.2 Authentication

Auth must feel institutional and secure.

Required screens:

- Sign in
- Role selection or role detection
- Two-factor/e.firma placeholder where applicable
- Privacy notice link

Rules:

- Avoid social-login-first layout for institutional users.
- Use clear role labels.
- Show security reassurance, not marketing copy.

### 16.3 Onboarding / Consent

Goal: explain what the system does before any monitoring, evidence capture, or guidance.

Steps:

1. Role and context
2. Privacy and data use
3. Consent
4. Safety options
5. Start

Rules:

- Use stepper.
- Allow save/exit.
- Never ask for more data than needed.

### 16.4 Tlachia Dashboard

User: authority analyst.

Primary goal: detect and review coordinated risk patterns without making automated legal conclusions.

Layout:

```txt
Header
- Title: Panel Tlachia
- Date range selector
- Export/report action

Top metrics
- Alertas nuevas
- Riesgo alto
- Casos en revisión
- Patrones detectados

Main grid
- Timeline of alerts
- Platform distribution
- Risk cluster list
- Explainability panel

Lower section
- Recent alerts table
- Audit log
```

Required UI details:

- Every alert must show why it was generated.
- Risk labels must include “detectado” or “sugerido”, not “confirmado”.
- Analyst actions must include: “Abrir alerta”, “Marcar para revisión”, “Descartar con motivo”.

### 16.5 Machiyotl Capture Flow

User: protected woman.

Primary goal: capture and seal evidence safely.

Mobile-first steps:

1. Start capture
2. Select source
3. Add file/screenshot/link
4. Add optional context
5. Generate local seal
6. Review evidence
7. Save locally or continue to Chimalli

Required UI details:

- Show “Solo en este dispositivo” before upload.
- Show offline status.
- Show progress one step at a time.
- Blur sensitive thumbnails by default.
- Make “Guardar y continuar después” available.

### 16.6 Chimalli Chat Flow

User: protected woman.

Primary goal: guide narrative, classify context, and prepare an evidence kit.

Layout:

```txt
Top bar with status and quick exit
Conversation area
Quick reply chips
Evidence tray
Bottom composer
```

Required UI details:

- Explain what the assistant is doing.
- Ask one question at a time.
- Allow “No sé” and “Prefiero no responder”.
- Show extracted information in editable cards.
- Label all generated summaries as AI suggestions.

### 16.7 Evidence Kit Screen

Goal: review before sending or exporting.

Required sections:

1. Summary
2. Evidence list
3. Timeline / chain of custody
4. Suggested authority routing
5. User narrative
6. Technical metadata
7. Review checklist
8. Final action

Rules:

- Use a formal but readable layout.
- Keep the send action at the end.
- Show exactly what is included.
- Include export/download options only after review.

### 16.8 Authority Case Review

User: authority analyst or reviewer.

Goal: inspect submitted evidence and route the case.

Required sections:

- Case header
- Current status
- Evidence table
- Chain of custody timeline
- AI extraction panel
- Routing recommendation
- Human decision panel
- Audit log

Rules:

- Highlight “human decision required”.
- Do not mark AI suggestions as official determinations.
- Allow comments and reasons for decisions.

### 16.9 Public Aggregated Dashboard

User: public observer.

Goal: show trends without exposing sensitive data.

Rules:

- Show only aggregated, anonymized metrics.
- Do not expose names, handles, screenshots, direct posts, or small group identifiers.
- Display methodology and privacy explanation.
- Use gentle institutional visual style.

---

## 17. Component Naming for Implementation

Use consistent names across code and design.

```txt
AppShell
TopBar
SidebarNav
BottomNav
PanicExitButton
RoleGate
ConsentStepper
PrivacyNoticeCard
EvidenceCaptureStepper
EvidenceCard
EvidenceTray
HashBlock
CustodyTimeline
RiskBadge
RiskScoreCard
AlertExplainabilityPanel
AIAssistBadge
ChimalliChat
ChatMessage
QuickReplyChips
EvidenceKitSummary
AuthorityRoutingCard
HumanReviewPanel
AuditLogTable
PublicMetricsDashboard
```

Rules:

- Components must accept semantic props, not raw color props.
- Use `variant`, `size`, and `state` props.
- Avoid one-off components when a reusable pattern exists.

Example:

```tsx
<RiskBadge level="medium" label="Riesgo medio" />
<EvidenceCard status="sealed-local" privacy="local-only" />
<HashBlock algorithm="SHA-256" hash={hash} />
```

---

## 18. Tailwind Implementation Guidance

Use Tailwind with CSS variables.

Example theme mapping:

```ts
// tailwind.config.ts
export default {
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        border: "var(--border)",
        primary: {
          DEFAULT: "var(--primary)",
          foreground: "var(--primary-foreground)",
          hover: "var(--primary-hover)",
          active: "var(--primary-active)",
        },
        secondary: {
          DEFAULT: "var(--secondary)",
          foreground: "var(--secondary-foreground)",
          hover: "var(--secondary-hover)",
        },
        success: {
          100: "var(--success-100)",
          600: "var(--success-600)",
          700: "var(--success-700)",
        },
        warning: {
          100: "var(--warning-100)",
          700: "var(--warning-700)",
        },
        danger: {
          100: "var(--danger-100)",
          700: "var(--danger-700)",
        },
      },
      borderRadius: {
        sm: "var(--radius-sm)",
        md: "var(--radius-md)",
        lg: "var(--radius-lg)",
        xl: "var(--radius-xl)",
      },
      boxShadow: {
        sm: "var(--shadow-sm)",
        md: "var(--shadow-md)",
        lg: "var(--shadow-lg)",
      },
      fontFamily: {
        sans: ["var(--font-sans)"],
        mono: ["var(--font-mono)"],
      },
    },
  },
};
```

### 18.1 Preferred UI Libraries

Allowed:

- shadcn/ui for accessible primitives
- Radix UI for dialogs, dropdowns, tabs, tooltips
- Lucide React for icons
- Recharts for standard charts
- D3 only for specialized cluster/network views

Rules:

- Restyle library components to match this design system.
- Do not use default component themes without applying tokens.
- Use accessible primitives for modals, dropdowns, tabs, menus, and tooltips.

---

## 19. Dark Mode

Dark mode is optional. If implemented, it must not be a pure inversion.

Dark theme direction:

```css
[data-theme="dark"] {
  --background: #131117;
  --foreground: #FAF8FB;
  --surface-soft: #1E1A23;
  --surface-card: #231D2B;
  --surface-raised: #2B2630;
  --border: #433B49;
  --border-strong: #5F5468;
  --primary: #D998E2;
  --primary-hover: #EEC9F2;
  --primary-active: #B461C6;
  --primary-foreground: #1B0B25;
  --secondary: #2B2630;
  --secondary-hover: #433B49;
  --secondary-foreground: #F8E6FA;
}
```

Rules:

- Maintain contrast requirements.
- Do not use pure black as default background except for special visual panels.
- Recheck chart palettes in dark mode.

---

## 20. Loading, Empty, and Error States

### 20.1 Loading

Use calm skeletons or small progress indicators.

Rules:

- Never show indefinite loading without explanation in evidence flows.
- If cryptographic work is running, label it clearly: “Generando sello local”.
- If upload is running, label it clearly: “Enviando expediente”.

### 20.2 Empty States

Empty states must teach the next safe action.

Example:

```txt
No hay alertas nuevas
Cuando Tlachia detecte actividad que requiera revisión, aparecerá en esta lista.
```

### 20.3 Error States

Errors must avoid blame.

Structure:

```txt
Title: No se pudo completar la acción
Description: Tu información sigue segura. Intenta nuevamente o guarda para continuar después.
Action: Reintentar
Secondary: Guardar y salir
```

---

## 21. Do / Do Not

### 21.1 Do

- Use a light, calm, institutional interface.
- Use strong typography hierarchy.
- Use semantic colors and accessible contrast.
- Show privacy state at every sensitive step.
- Make user review explicit before sending.
- Label AI-generated content clearly.
- Use human-centered, respectful language.
- Design mobile-first for evidence capture.
- Design dashboard-first for authority monitoring.
- Provide safe exits and save-later paths.

### 21.2 Do Not

- Do not sensationalize violence.
- Do not use graphic or fear-based imagery.
- Do not imply the AI determines guilt or legal outcome.
- Do not upload evidence without review and consent.
- Do not expose sensitive thumbnails by default.
- Do not use color alone to convey risk.
- Do not overuse red.
- Do not use playful gamified UI.
- Do not hide legal or privacy consequences behind vague buttons.
- Do not create dense legal walls of text in primary flows.

---

## 22. Quality Checklist

Before shipping any screen, verify:

### Visual

- [ ] Uses approved tokens.
- [ ] Has clear hierarchy.
- [ ] Uses one primary action.
- [ ] Spacing follows the 8-point system.
- [ ] Cards and panels use correct radius and borders.
- [ ] No raw hardcoded colors outside token files.

### Accessibility

- [ ] Text contrast passes 4.5:1.
- [ ] Icon/component contrast passes 3:1.
- [ ] Keyboard focus is visible.
- [ ] Screen reader labels exist for icon-only controls.
- [ ] Form fields have labels and errors.
- [ ] Touch targets are at least 44px.
- [ ] Motion respects reduced-motion preferences.

### Privacy and Safety

- [ ] Sensitive evidence is not previewed by default.
- [ ] Upload requires explicit review.
- [ ] Local vs uploaded state is visible.
- [ ] Panic exit is available in sensitive flows.
- [ ] AI content is labeled as suggestion.
- [ ] The interface does not imply automated legal judgment.

### Product Fit

- [ ] Tlachia screens feel analytical and auditable.
- [ ] Machiyotl screens feel private and step-based.
- [ ] Chimalli screens feel supportive and clear.
- [ ] Authority screens include human review.
- [ ] Public screens only show aggregated data.

---

## 23. Final Implementation Rule

When uncertain, choose the design that is:

1. More readable.
2. More respectful.
3. More private.
4. More explicit about user consent.
5. More transparent about AI limitations.
6. More accessible.
7. Less visually dramatic.

Yaocíhuatl must feel like a calm shield: protective, precise, discreet, and trustworthy.
