# Faraday — Flow & UI Spec

> *AI-assisted lab notebook for industry chemists. Record like Faraday. Search like Google. Audit like the FDA expects.*

**Status**: Planning doc — NOT for any repo. Build deferred until post-offer.
**Scope of this doc**: End-to-end user flow + UI screens only. Backend architecture, data model, tech stack decisions captured at a high level; details locked when building starts.

---

## 1. The user

### 1.1 Primary persona

**Bench chemist working in a regulated industry research lab — pharma, biotech, or materials R&D — who runs experiments daily and is responsible for documenting them to regulatory-defensible standards.**

Typical profile:
- 2-10 years post-MSc/PhD experience
- Works under SOPs and project protocols
- Notebooks are legal documents (subject to FDA / EMA / sponsor audits)
- Reports to a senior scientist or principal investigator
- Documentation is roughly 30-50% of their time — most of it tedious

### 1.2 What they do today — verbatim observations

From 5 years in academic labs (Sindhuja's MSc Chemistry) + observation of how chemists actually work:

- **Tools are fragmented**: paper notebook, Excel for data tables, Word for protocols, Outlook for sending to collaborators
- **Search is broken**: every time chemists need historical data, they re-look-up or rely on memory. *"Where did I record that yield?"* → 20 minutes lost
- **"Full data" is undefined**: definition of complete documentation varies person to person. One chemist records observation depth, another doesn't. Same lab, no shared standard.
- **No clear status**: hard to know what's done vs. what's pending across a multi-day experiment
- **Failure diagnosis is gut-feel**: when something goes wrong, identifying *which step* failed is guesswork. Often leads to re-running the entire experiment.

### 1.3 Industry-specific pain layered on top

What industry chemists face that academic ones don't:

- **Regulatory weight**: lab notebooks are legal records. 21 CFR Part 11 (FDA) requires immutable audit trails, electronic signatures bound to identity, system-generated timestamps. Hand-written notebooks are still common because most digital ELNs feel worse than paper.
- **ALCOA data integrity**: Attributable, Legible, Contemporaneous, Original, Accurate. Plus ALCOA+: Complete, Consistent, Enduring, Available. Every data point must satisfy all of these.
- **SOP referencing**: every experiment must reference the controlled SOP being followed. Today chemists open the SOP doc in another window, type the section reference manually. Hours wasted per week.
- **Reagent traceability**: every chemical has a CAS number + a supplier lot number + a Certificate of Analysis. Audit trail must link experiment → reagent lot → CoA. Manual entry is error-prone.
- **Deviation reports**: when something goes off-protocol, formal documentation is required. Today this means a separate Word doc + emails + signatures. Chemists avoid it, then catch hell from QA later.
- **Instrument data**: HPLC, NMR, MS, IR, GC outputs are CSV/XLSX/JDX/raw files. Today chemists manually copy values into Excel or transcribe by hand. Instrument-to-notebook integration is broken in most ELNs.
- **Witness/review workflow**: notebook entries need a peer/supervisor sign-off. Existing ELNs make this slow and bureaucratic. Often delayed days, breaking the contemporaneous principle.
- **Bench reality**: chemists work standing at a fume hood with gloves on. Typing into a laptop while wearing nitrile gloves and handling solvents is awkward. Most ELN UIs assume desk-bound users.

### 1.4 What existing tools get wrong

The ELN market (Benchling, LabArchives, Dotmatics, IDBS, Signals, RSpace) is:
- **Expensive**: $50-500 per user per year
- **Form-heavy**: feels like data entry, not lab work
- **Slow**: page loads, mandatory fields, validation friction
- **Bad at search**: no semantic search; keyword search returns noise
- **Bad at instrument data**: CSV import is manual click-by-click
- **Bad at observations**: forces structured fields; chemists want to dictate or scribble freely
- **Bad on mobile**: bench-side use is painful

Many industry chemists end up *paying for ELN compliance + still using paper for actual work* — defeating the point.

### 1.5 What Faraday does differently

The thesis: **modern AI + modern UX can collapse the documentation-versus-doing tradeoff**. Specifically:

- Auto-complete reagent details from CAS number (no manual typing)
- Auto-link to relevant SOPs based on experiment context
- Convert instrument output files into structured data automatically (NMR → Curie integration is the flagship example)
- Voice-to-text for observations (chemist talks while working)
- Natural-language search across all past experiments
- Auto-generate experiment summary draft for review
- Smart audit trail — preserves immutability AND makes history readable
- Word-doc-like editing UX, not form-based — chemists own the prose, AI fills the scaffolding

**Critical wedge**: editing IS the work. Unlike published research papers where editing is for authors only, lab notebook entries are *in-progress* documents that chemists continuously author. The editable doc UX (Sindhuja's BRD-GEN engineering) maps to this use case perfectly.

---

## 2. The canonical user journey

Faraday is **open to three trigger scenarios** — chemists don't fit one pattern, so we don't force one path:

1. **Assigned protocol**: a planned experiment handed down from the project lead or PI, possibly assigned to a specific team member
2. **Freelance experiment**: chemist designs something new based on literature review or hypothesis
3. **Variation of known experiment**: a previously-run experiment with one or more parameters changed (different solvent, catalyst, temperature, etc.)

The UI accommodates all three through three entry paths described in 2.2.

### 2.1 Entry — how a chemist starts a new experiment

**Three paths, surfaced clearly on the home screen:**

| Path | When to use | What Faraday does |
|---|---|---|
| **Template library** | Common industry experiments (synthesis, characterization, analytical methods) | Pre-populates: SOP reference, default reagents, default equipment, standard observation checkpoints |
| **Blank canvas (notebook mode)** | New / freelance experiments, or combining multiple sub-experiments into one record | Empty document with block-level structure; chemist composes from scratch |
| **Search past experiments** | Repeating with a variation, or referencing a prior result | Returns matching past experiments by name / reagents / outcome; chemist can clone-and-modify any of them |

**v0.1 template library scope**: start with 5-10 of the most common industry experiments (e.g., recrystallization, column chromatography purification, NMR characterization, HPLC purity check, Suzuki coupling, reduction reaction). Expandable.

### 2.2 Reagent setup

When chemist selects a template, default reagents are auto-filled. **Everything is overridable** — catalyst, solvents, even the main starting material can be swapped.

**Adding or changing a reagent supports multiple input methods:**

| Method | UX |
|---|---|
| **Type-ahead search** | Start typing compound name → autocomplete from internal DB |
| **CAS number entry** | Paste/type CAS number → Faraday looks up structure, MW, hazards |
| **Barcode scan (image upload)** | Upload a photo of the reagent bottle barcode → OCR + lookup |
| **Inventory pick** | If lab has its inventory in Faraday, select from stocked compounds with lot numbers |

**v0.1 internal DB scope**: 10-20 most common reagents pre-loaded (common solvents, reductants, oxidants, catalysts, starting materials for the template library experiments above). Not 10,000 — that's enterprise scope, deferred.

**Fallback for unknown compounds**: if Faraday's DB doesn't have it, show alternate suggestions (related compounds, suggest user enter manually with structure-drawing tool deferred to v0.2).

**Reagent record captures**: CAS, MW, supplier, lot number, source (Sigma-Aldrich, Fisher, Merck — *suggestion only, not a sales channel*), Certificate of Analysis link if available.

### 2.3 Live experiment recording — at the bench

**The hardest UX challenge.** Chemists are standing at the fume hood, often with gloves on. No laptop in hand. Sometimes a phone is allowed; sometimes not (regulated labs may prohibit phones near sensitive equipment).

**v0.1 approach** — multiple capture methods, none forced:

| Method | When it works |
|---|---|
| **Standard checkpoints** | Chemist taps a pre-defined event ("added Reagent A," "started stirring," "stopped reaction") — fast, glove-friendly |
| **Custom comment** | Free-text annotation tied to a timestamp |
| **Voice-to-text** | If phone/voice device is allowed, chemist dictates observations naturally — Faraday transcribes |
| **Manual entry post-hoc** | If neither phone nor voice is available, chemist enters observations at end of session — timestamps are approximate but auto-flagged as such |

**Every event gets a system-generated timestamp** (ALCOA-compliant — chemist cannot edit the timestamp, only the description).

**v0.2 future** — camera integration: if the lab has a fixed camera in the fume hood area, Faraday can ingest the video stream and AI auto-identifies events (reagent added, stirring changed, color changed) with timestamps. Chemist reviews and confirms. **Deferred — but worth flagging in the spec because it's a credible roadmap item.**

### 2.4 After the experiment — ingesting instrument data

When the experiment is done, chemist has output files from instruments: NMR (.jdx, .csv), HPLC (.csv, .xlsx), MS (raw, .csv), IR (.csv), XRD (raw, .csv), GC (.csv), UV-Vis (.csv), etc.

**v0.1 ingest UX**:

1. **Drag-and-drop** the file onto the experiment page
2. **Faraday detects file type** by extension + content signature
3. **AI identifies the instrument and experiment context** ("This looks like 1H NMR data — confirm?")
4. **Chemist confirms or corrects** the instrument type
5. **Faraday parses** the file into structured data — peaks, retention times, masses, intensities — and appends a Results block to the experiment record
6. **Original file is also preserved** for audit (the parsed data is a derivative; the source file is the legal record)

**Faraday does NOT predict, elucidate, or interpret in v0.1.** It records and structures the data. Interpretation (e.g., "this NMR matches an aromatic ester") is **Curie's job** — and Curie integration is a future link, not a v0.1 feature.

**Why no Curie integration in v0.1**: Curie itself is still in v0.1 ("retrieve first, reason second" — 60% top-1 accuracy on textbook compounds). Until Curie's outputs are reliable enough that chemists won't second-guess them, auto-piping NMR data through Curie creates more confusion than value. **v0.2 Curie integration**: optional "Run through Curie" button on NMR data blocks → results return as a *suggested annotation* the chemist can accept, edit, or ignore.

### 2.5 Calculations and computed fields

**v0.1 keeps math simple:**
- Yield % (from mass in vs mass out)
- Concentration (mass / volume)
- Molar equivalents
- Theoretical yield (from reagent moles + stoichiometry)
- Reaction time (from start/stop timestamps)

**Not in v0.1**: thermodynamics calculations, kinetics modeling, retrosynthesis suggestions, mechanism prediction. These are research-tool features, not lab-notebook features.

### 2.6 Final output — the experiment report

When chemist marks the experiment complete, Faraday generates a **shareable experiment report**:

- Clean, structured layout (not the editor view — a presentation-ready view)
- Includes: title, abstract (AI-drafted from notes, editable), reagent table, procedure (timestamped), observations, results, calculations, conclusions
- Exports to PDF, DOCX, and Faraday's native format
- Auto-generated visual abstract — the **PaperBanana-style illustration integration** Sindhuja flagged
  - Inputs: structured experiment data
  - Output: a single visual abstract image summarizing the experiment (similar to journal-required visual abstracts)
  - Editable: chemist can refine the illustration, swap colors, adjust layout

**Why the visual abstract belongs in Faraday (and not Franklin)**: this is *the chemist's own in-progress work* — they're authoring it, they need to edit it. Exactly the use case that killed Franklin (where editing a published paper's visual abstract had no user). Here, editing IS the work — and the chemist is generating the visual for *their own* completed experiment, before sharing internally or filing.

This unifies what would have been "Franklin" into Faraday as a natural final step. **No need for a separate Franklin project.**

### 2.7 Lab Memory — the search layer (NOT a chatbot)

**Faraday isn't a chatbot. It's your lab's memory.**

Three distinct interaction modes — each visually and behaviorally distinct from chatbot conventions:

#### Mode A — Ask
- Natural-language query
- Answer is a **visualization** (chart, scatter, time series) — not prose
- Example query: *"Show Suzuki couplings with yield below 60% in last 6 months"*
- Example answer: scatter plot of yields over time, colored by catalyst; click any point to open that experiment

#### Mode B — Compare
- Chemist selects 2-5 past experiments
- Side-by-side structured diff view: reagents, conditions, observations, results, what changed
- No prose answer — pure structured rendering

#### Mode C — Watch (the unique mode)
- Proactive — surfaces relevant past experiments WHILE chemist works
- Example: when chemist enters reagents at the start of a new experiment, sidebar quietly shows *"Your last 3 runs with this catalyst + solvent yielded 42%, 38%, 61%."*
- Like a senior chemist whispering over the shoulder
- **No other ELN does this. This is Faraday's distinctive feature.**

The framing line for README and pitch: ***"Faraday isn't a chatbot. It's your lab's memory."***

### 2.8 Publication Mode — design choice, not v0.1 feature

When a chemist has run experiments over months and is ready to publish, **Faraday composes a paper draft from N selected experiments.**

Workflow:
1. Chemist selects multiple past experiments from history
2. Faraday generates:
   - Visual abstract synthesizing across all selected experiments
   - Methods section draft (from procedures and reagent tables)
   - Results section with auto-formatted data tables
   - Figure suite composed from instrument outputs
3. Chemist edits in Faraday's editor (the BRD-GEN-style editable doc UX is the wedge here)
4. Exports to journal-ready format (PDF, DOCX with journal templates)

**v0.1 does NOT ship Publication Mode** — it's a v0.2/v0.3 feature.

**But v0.1's data model is designed FOR it.** Specifically:
- Experiments stored as structured data, not text blobs → AI can compose across them later
- Reagents, observations, results stored with rich metadata
- Cross-experiment relationships explicit (variant of X, repeat of Y, references Z)

This is what *"design choice, not decoration"* means — the architecture supports the future use case from day one.

### 2.9 Why no agents in v0.1 — explicit justification

We don't use an agent just because the AI ecosystem is using them. Per-feature justification:

| Feature | Technique | Why NOT an agent |
|---|---|---|
| Semantic search | RAG (FAISS + embeddings) | Single retrieve + answer call. Agent loop adds latency, no insight gain. |
| Visual answers (Ask mode) | LLM structured output + chart renderer | LLM returns structured spec, chart library renders. No agentic exploration needed. |
| Compare mode | Pure structured diff (no LLM) | Data shaping. No reasoning required. |
| Watch mode | Vector similarity + light LLM filter | Match past experiments → LLM picks top 1-3. Single call. |
| Anomaly detection | LLM-as-judge with 3-4 fixed checks | Stoichiometry, SOP match, language tone, history compare. Each check is independent and always runs. Agent adds nothing. |
| Reagent autocomplete | PubChem API + vector search | Pure lookup. |
| Voice-to-text | Whisper (local) | Pure transcription. |
| Instrument parsing | Structured LLM call | One call returns structured JSON. |
| Smart audit summarization | Single LLM call over audit log | Stateless. |

**v0.1 = zero agents.** Justification: *"Each feature is a stateless RAG call or structured LLM call. Agentic complexity would add latency and reduce predictability without adding value at v0.1's scope."*

**When agents become justified (v0.2/v0.3):**
- **Publication Mode** — true agent territory (multi-step, branching, decision-heavy across many experiments)
- **Smart Audit deep navigation** — flexible reasoning across long audit history

That's the deliberate architectural restraint. The portfolio signal: *this person knows when not to use the latest pattern.*

### 2.10 v0.1 scope — LOCKED

**No more changes to this scope. Build target.**

| Area | v0.1 ships |
|---|---|
| **Entry** | Template library (5 industry experiments) + Blank canvas |
| **Reagent setup** | Type-ahead search · CAS lookup · Barcode scan (image upload) · Inventory pick · Custom compound entry (5 methods) |
| **Live recording** | Standard checkpoints (auto-generated from template steps) + custom comments. Voice-to-text → v0.2. |
| **Instrument ingest** | NMR (.jdx, .csv) + HPLC (.csv). *"Working on"* placeholder for IR, MS, XRD, GC. |
| **Lab Memory** | All 3 modes — **Watch** (proactive sidebar), **Ask** (NL query → visual answer), **Compare** (side-by-side diff of N selected experiments) |
| **Anomaly detection** | Stoichiometry sanity + SOP deviation + history comparison (3 checks). Language tone dropped — false-positive risk. |
| **Calculations** | Yield % · Molar equivalents · Theoretical yield · Thermodynamics (ΔG, ΔH, ΔS with user-input values + auto-fill from PubChem where available) · Kinetics (rate fitting from concentration-time data) · Calculation plots in naturalist editorial style |
| **Output** | Editable structured report + PDF export. No DOCX in v0.1. |
| **Audit trail** | ALCOA timestamps + immutable change history + manual *"Witnessed by [name]"* field (cryptographic signatures → v0.2 with auth) |
| **SOP object** | Captures instruments + reagents + PPE metadata (PPE camera detection → v0.3) |
| **Auth** | None — single-user demo product |

**Build estimate (solo, post-offer):** ~6-8 weeks

**v0.2 roadmap (additive — does not require refactor):**
- Voice-to-text recording (Whisper integration)
- Compare mode polish (currently structured diff; add semantic similarity hints)
- Publication Mode (paper composition from N experiments — uses v0.1 data model)
- Visual abstract generation (PaperBanana-style, beyond the v0.1 calculation plots)
- Additional instrument formats (IR, MS, XRD, GC)
- Cryptographic witness signatures (requires auth)
- Multi-tenant collaboration

**v0.3 roadmap:**
- Camera ingest with AI event detection (in-fume-hood video → timestamped observations)
- PPE compliance detection via camera + SOP PPE metadata
- Curie integration for NMR auto-interpretation (when Curie hits 80%+ top-1)
- Enterprise compound DB (10K+)

---

## 3. Design language

The reference points: **Adobe Firefly's creative confidence, Apple's intentional minimalism, Notion AI's content-first restraint, Linear's typographic discipline** — but warmed by the **naturalist chemistry-notebook aesthetic** established by Curie and Darwin.

The result should feel like *writing in a beautifully-designed artisanal lab journal that happens to be powered by AI* — not like a SaaS product.

### 3.0.1 Palette

| Token | Hex | Use |
|---|---|---|
| `surface.warm` | `#FAF8F3` | Page background (cream, warmer than `#FFFFFF`) |
| `surface.elevated` | `#FFFFFF` | Cards, modals, editor canvas |
| `ink.primary` | `#1B1F1A` | Body text, headings |
| `ink.secondary` | `#5C6360` | Captions, meta, secondary labels |
| `ink.tertiary` | `#A8AFAB` | Disabled state, faint dividers |
| `accent.faraday` | `#B45309` | Faraday's signature warm-amber (electrochemistry roots) |
| `accent.curie` | `#7C3AED` | When Curie integration surfaces (future) |
| `state.ai-suggest` | `#8B5CF6` | AI-suggested content (subtle violet — never default; chemist accepts to adopt) |
| `state.confirmed` | `#059669` | Confirmed, verified, witnessed |
| `state.warn` | `#D97706` | Anomaly flag, deviation, attention needed |
| `state.error` | `#B91C1C` | Hard errors only — rare |
| `botanical.line` | `#9CA89A` | Corner illustration line work |

**No dark mode. Light mode only.** Decision: chemists work in well-lit labs; dark mode would fight the existing environment + complicate the editorial illustration work.

### 3.0.2 Typography

| Role | Font | Notes |
|---|---|---|
| Display / hero | **Fraunces** or **Tiempos Headline** (serif with character) | Large, editorial, slightly artisanal |
| Body | **Inter** | Clean sans, broad screen-reader support |
| Mono (code, CAS numbers, timestamps) | **JetBrains Mono** | Same as Curie + Darwin — series consistency |

Size scale (modular):
- Hero: 56-72pt
- H1: 36pt
- H2: 24pt
- H3: 18pt
- Body: 16pt
- Caption: 13pt
- Mono labels: 13pt at 0.04em letter spacing

### 3.0.3 Spacing + rhythm

- Base unit: **8px**
- Card padding: **24px** (3 units)
- Section spacing: **48px** (6 units)
- Hero negative space: **96px+** top/bottom on landing screens
- Editor block spacing: **16px** between blocks

The whole product should feel **under-filled, not over-filled**. Apple/Notion-level breathing room.

### 3.0.4 Illustration + visual motif

- **Botanical line corners** on hero / landing / empty states — same eucalyptus + fern style as Curie + Darwin
- **No stock icons.** Custom line icons drawn in the same hand-feel (or open-source set like Phosphor-thin)
- **Chemistry visuals** (molecule structures, NMR spectra) rendered with RDKit-JS / D3, styled to match the editorial palette
- **Calculation plots** — naturalist editorial style (cream background, soft amber/violet data lines, hand-drawn axes feel)

### 3.0.5 Interaction language

- **Hover states**: subtle elevation increase (1-2px shadow grow), no color flash
- **Focus**: 2px outline in `accent.faraday` (amber) — visible, accessible (WCAG 2.1 AA)
- **AI-suggested content**: rendered with `state.ai-suggest` (violet) ghost text. Chemist must explicitly accept (`Tab` or click) to adopt. Never auto-inserts.
- **Witnessed / confirmed items**: subtle `state.confirmed` green checkmark + faint background tint
- **Anomaly chips**: `state.warn` amber pill with chevron — clickable to expand reasoning, dismissible
- **Transitions**: 200-300ms ease-out for everything. Nothing snappy. Nothing slow.

### 3.0.6 Layout system

- **Responsive breakpoints**:
  - Mobile: 0-639px (limited to viewing experiments + Lab Memory Ask; no editor)
  - Tablet: 640-1023px (bench mode — full editor with simplified chrome)
  - Desktop: 1024px+ (full UI)
- **Editor canvas**: max-width 880px (readable measure), centered with breathing margins
- **Lab Memory Watch sidebar**: 320px fixed right (desktop), collapses to floating button (tablet/mobile)

### 3.0.7 Editor model (the BRD-GEN inheritance)

Same block-based editor pattern as BRD-GEN (general engineering knowledge, reimplemented from scratch):

- **Blocks**: paragraph, heading, reagent table, checkpoint, observation, instrument data, calculation, plot, witness signature
- **Block-level controls**: drag handle (left), block menu (right), insert-below (between blocks)
- **Slash command** to insert blocks (`/reagent`, `/checkpoint`, `/calc`, etc.)
- **AI command**: `/ai` opens an AI suggestion panel for the current context
- **Inline AI**: typing `+ai` followed by a question inline pulls AI suggestion as ghost text — chemist accepts or rejects
- **Tab navigation** through blocks (accessibility)
- **Screen reader**: each block has `role="region"` + `aria-label` from block type + content summary

### 3.0.8 Accessibility (WCAG 2.1 AA target)

- Color contrast ≥ 4.5:1 for all text
- Focus indicators visible everywhere
- All interactions keyboard-accessible
- ARIA landmarks for navigation regions
- Editor blocks announced correctly by screen readers
- Voice-to-text (v0.2) doubles as alternative input

### 3.0.9 The feeling we're going for

If a chemist opens Faraday for the first time and the immediate gut reaction is *"this doesn't look like an ELN"* — we've succeeded.

If they then realize it's also *more capable than the ELN they've been forced to use* — they convert.

The aesthetic + capability combination is the wedge.

---

## 3.1 Landing page — Option A (hero-first), LOCKED

### Layout direction
**Hero-first.** Single bold gesture above the fold: massive serif headline + a beautifully-rendered Faraday hero illustration + one warm-amber CTA. Workspace utility (recent experiments, Watch sidebar) appears below the fold on scroll. Inspired by Adobe Firefly / Apple research apps.

### Hero illustration — LOCKED (`faraday-hero.png`)
The hero is an open hand-bound lab notebook with the analog-to-digital metaphor rendered as image:
- **Left page** — handwritten Faraday-style numbered paragraph entry (¶ 2,847 — 14:32), cursive observation about a colour shift (yellow → amber → violet rendered in coloured handwriting), molecule sketched in margin (anisole derivative with OMe group), small ink smudge for authenticity
- **Right page** — same entry transformed into structured digital blocks: OBSERVATION block with the same colour-shifted text, STRUCTURE block with cleaner molecule, tag chips (`colour shift`, `pH responsive`, `conjugation`, `phenoxide`), violet AI-suggested `deviation?` chip
- **Memory thread** — saturated warm-gold glowing arc flows left page → right page
- **Pressed botanicals** — eucalyptus + fern fronds tucked between the pages
- **Periphery details** — teacup, fountain pen, colour-coded tabs along the notebook edge, loose paper with another molecule sketch peeking out — all signalling a notebook in active use, not an archive

Palette: warm cream background (`#FAF8F3`), fresh ivory paper (`#FFF9EE`), warm caramel binding, vibrant pressed greens, saturated gold memory thread, Faraday-signature amber accents. Light-mode native, full vibrancy.

### Above-the-fold composition

```
┌──────────────────────────────────────────────────────────────┐
│  Faraday                                              [👤]   │  ← minimal nav
│                                                              │
│                                                              │
│                  Your lab's memory.                          │  ← 72pt Fraunces serif
│         Record like Faraday. Search like Google.             │  ← 18pt body, italic
│                                                              │
│                                                              │
│       ┌────────────────────────────────────────┐             │
│       │                                        │             │
│       │      [faraday-hero illustration]       │             │  ← 60% viewport height
│       │                                        │             │
│       └────────────────────────────────────────┘             │
│                                                              │
│                                                              │
│              [+ Start your first experiment]                 │  ← single amber pill CTA
│                                                              │
│                  ↓ scroll to see recent work                 │  ← faint scroll hint
└──────────────────────────────────────────────────────────────┘
```

### Below the fold (revealed on scroll)
- Recent experiments grid (3-column card layout on desktop, stacks on mobile)
- Watch mode sidebar (right rail on desktop, becomes a floating chip on mobile/tablet)
- Quick links to Lab Memory (Ask / Compare)
- Faint footer with version, license, links

### Returning user state
After the chemist's first experiment exists, the hero illustration shrinks to a small marginal flourish and *"Welcome back, [name]"* with experiment count replaces the headline. Workspace becomes the primary fold. Hero remains visible on the home page but stops dominating.

### Micro-interactions
- Hero illustration fades in over 400ms ease-out on first load
- Memory thread glow loops subtly (3s ease-in-out cycle, very low amplitude)
- CTA button has a soft amber glow on hover, no movement
- Botanical corners appear last (200ms delay) as quiet watermarks

---


| Stage | In v0.1 | Deferred |
|---|---|---|
| Entry | Template library (5-10) · Blank canvas · Past-experiment search | Multi-tenant sharing, cross-lab templates |
| Reagent | Type-ahead · CAS · Barcode-image · Inventory (10-20 default) | Enterprise 10K+ compound DB, automated CoA pull |
| Recording | Checkpoints · Voice-to-text · Custom comments · Manual entry | Camera ingest with AI event identification |
| Data ingest | Drag-drop · AI file-type detection · Structured parse · Source file preservation | Curie integration for NMR interpretation |
| Calculation | Yield, concentration, equivalents, theoretical yield, timing | Thermodynamics, kinetics, retrosynthesis |
| Output | Editable report · PDF/DOCX export · Visual abstract (PaperBanana-style) | Multi-language reports, journal-specific abstract templates |

---

