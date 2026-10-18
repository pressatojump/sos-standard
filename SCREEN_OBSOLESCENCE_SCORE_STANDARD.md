# Screen Obsolescence Score Standard (`SOS-1.0`)

**Document ID:** `SOS-STD-1.0`  
**Version:** `1.0.0`  
**Date:** `2026-10-18`  
**Authoring Profile:** ASDAI Format v0.1.0 §§4–5 communication principles  
**Status:** Normative Evaluation Standard  
**Canonical Location:** `/Users/pm/SCREEN_OBSOLESCENCE_SCORE_STANDARD.md`

---

## 1. Executive Summary and Foundational Premise

### 1.1 Leaving Behind a Single Base Skill

Human civilization periodically absorbs a specialized, full-time technical craft into infrastructure so completely that exercising the underlying mechanics ceases to be a human skill and becomes pure channeling of intent.

Historically, **the scribe** embodied the base skill of manual inscription and textual formatting. Before universal literacy and mechanical/digital reproduction, encoding speech or thought into durable written form was a full-time profession. Once the format was standardized and eventually automated, the mechanical act of scribing ceased to be the locus of intellectual value; humans merely channeled thought through the medium.

Today, almost every activity involving computers—software engineering, scientific research, quantitative analysis, document typesetting, graphic design, digital art, image synthesis, and systems administration—is boxed into what are treated as distinct full-time jobs. Yet beneath their domain labels, all of these jobs share one mandatory, bottlenecking human base skill: **operating a screen**.

To "use a computer" today means to sit before a two-dimensional luminous rectangle, visually parse dense text, layouts, and pixel arrays, manipulate spatial windows and cursors, manually hunt through file trees to assemble context, and visually inspect outputs (code diffs, PDF page proofs, generated images, UI layouts) to verify that the machine did not fail.

### 1.2 Beyond the Scribe: Why the Screen Is the True Boundary

The analogy of the scribe is necessary as a historical starting point, but insufficient as an encapsulation of what a computer coupled with a Large Language Model (LLM) can do. A human scribe only formatted and transcribed text. A computer coupled with an LLM generates **papers** (typeset manuscripts, mathematical proofs, vector diagrams, bibliographic apparatuses), **art**, **images**, interactive simulations, and executable software systems.

Wait: if the outputs include visual art, images, and typeset papers, does the screen cease to exist? **No.** Rather, **the use of the screen is transferred entirely to the LLM side.**

In this paradigm:
1. The machine still renders framebuffers, canvases, PDFs, shaders, DOM trees, and raster images onto virtual or headless screens.
2. The LLM side reads, inspects, critiques, manipulates, and verifies those screens autonomously.
3. **The human being never has to use the screen.**

The **Screen Obsolescence Score (`SOS`)**—also referred to as the **Screen-Free Liberation Score**—measures how completely an LLM-coupled computer system allows a human being to leave behind screen operation as a base skill while retaining full creative, scientific, and operational command over everything a computer can produce.

### 1.3 Why This Standard Is Important

Existing LLM benchmarks measure how well a model performs *inside* the screen-operator paradigm—answering multiple-choice questions, completing code snippets inside an IDE, or clicking elements in a browser while a human watches. None of them measures whether the human being can **leave the screen behind altogether**.

`SOS-1.0` is important for four foundational reasons:

1. **Decoupling Human Intellect from Visual-Spatial Clerical Labor:** Just as the transition beyond the scribe freed thinkers from the mechanics of calligraphy and parchment layout, moving beyond screen operation frees human principals from window multiplexing, file-tree foraging, syntax typing, and pixel-level layout babysitting. Computing ceases to be a full-time visual-motor job and becomes pure channeling of intent, taste, and judgment.
2. **Exposing the Bottleneck Fallacy in "Autonomous" Agents:** Many agent systems boast high reasoning or coding capability (`CTX`, `CRE`, `JDG`) while remaining completely unusable without a human staring at a terminal or dashboard (`AIO` near zero, or blind visual emission without machine-side screen inspection). By coupling latent capability with the **Bottleneck Balance Factor (`BBF`)** and **Screen Fallback Events (`SFE`)**, `SOS-1.0` exposes systems that shift cognitive load onto the human's eyes rather than eliminating it.
3. **Transferring the Screen to the Machine (`LLM-Owned Screen Loop`):** Leaving the screen behind does not mean regressing to text-only outputs. Humans still need typeset research papers, engineering drawings, fine art, images, and interactive software. `SOS-1.0` establishes the normative requirement that the LLM must own and inspect the virtual screen itself—rendering pixels offscreen, critiquing layout and aesthetics with machine vision, and delivering verified visual artifacts without human visual QA.
4. **Universal Accessibility and Cognitive Ergonomics:** A system that achieves high `SOS_effective` liberates human attention during physical movement, eyes-free work, or visual impairment, replacing hours of screen fatigue with high-signal acoustic dialogue and autonomous epistemic stewardship.

---

## 2. The Necessary Hypothetical Scenario: The Sealed-Screen Protocol (`H-SEALED-SCREEN`)

To construct and calibrate `SOS-1.0` without confusing "helpful screen copilot" features with true post-screen liberation, evaluators MUST evaluate every target system against the following normative hypothetical scenario, designated **`H-SEALED-SCREEN`**:

> **Scenario Definition (`H-SEALED-SCREEN`):**  
> A human principal with high-level domain intent, aesthetic taste, scientific curiosity, and executive authority enters a workspace to conduct arbitrarily complex computer-coupled work—authoring research papers, creating original art and images, analyzing data, and engineering software systems.  
>
> At time $t = 0$, **every human-facing display is powered off and physically sealed (`0 nit`, `0 px` human visual bandwidth)**. The human has no monitor, no terminal window, no IDE pane, no file picker, and no visual image viewer.  
>
> The computer hardware and the LLM system remain fully powered and retain internal access to virtual displays, GPU framebuffers, headless browsers, PDF/LaTeX engines, image/video synthesizers, compilers, and external networks.  
>
> The human interacts with the system solely through non-screen modalities—centrally **bidirectional audible inputs and outputs** (spoken dialogue, prosody, ambient audio cues)—while the system performs **passive and active context assembly**, **multimodal creation (paper, art, images, code)** via **LLM-managed screens**, and **independent judgment**.

### 2.1 Definition of a Screen Fallback Event (`SFE`)

In `H-SEALED-SCREEN`, any moment where the human principal would be forced to unseal the monitor, look at pixels, type structured syntax with visual echo, or manually inspect an artifact to proceed or to trust the result is defined as a **Screen Fallback Event (`SFE`)**.

| Fallback Code | Class Name | Trigger Condition in `H-SEALED-SCREEN` |
| :--- | :--- | :--- |
| **`SFE-IO`** | Acoustic Mediation Failure | The system cannot accept natural spoken input, cannot handle interruption, or emits raw 2D visual text (uncompressed stack traces, raw JSON, markdown tables, file path dumps) that is unintelligible or exhausting as audio. |
| **`SFE-CTX`** | Manual Context Assembly Failure | The human must locate a file path, copy-paste text between windows, specify exact identifiers from memory, or visually browse a directory/search results list to ground the LLM. |
| **`SFE-VIS`** | Uninspected Visual Creation Failure | The system generates (or refuses to generate) a paper, artwork, image, chart, or visual layout without rendering and visually inspecting its own output on an LLM-managed screen, forcing the human to look at the screen to catch clipping, garbled anatomy/text, broken layout, or aesthetic failure. |
| **`SFE-JDG`** | Judgment Abdication Failure | The system either (a) claims completion without rigorous independent verification, forcing the human to visually audit diffs/outputs on a screen, or (b) bombards the human with low-level tactical confirmations that recreate screen-operator micromanagement over audio. |

---

## 3. Normative Architecture of the Score: The Four Core Pillars and Open-Ended Frontier Horizons

Under `SOS-1.0`, the score has **no upper ceiling (`[0, ∞)`)**. A score of `100.00` (`25` points per sub-dimension across the four core pillars) represents the **Digital Post-Screen Reference Anchor**—the threshold where human screen operation on a computer becomes obsolete for digital ideation, context assembly, multimodal creation, and independent judgment.

However, eliminating the screen on a digital machine is only the first horizon. An upper ceiling would imply a terminal boundary on what human intent channeled through an autonomous system can solve. In reality, once the screen belongs to the LLM side, the problem-solving loop expands without ceiling from **ideation on a machine** $\rightarrow$ **accrual of value (`VAL`)** $\rightarrow$ **robotic development (`ROB`)** and **wet lab development (`WET`)** $\rightarrow$ **material design (`MAT`)**. Accordingly, both the 16 sub-dimensions ($x_{p,i} \in [0, \infty)$) and the four **Frontier Realization Horizons (`VAL`, `ROB`, `WET`, `MAT` $\in [0, \infty)$)** are open-ended above.

```
+-----------------------------------------------------------------------------------+
|               SCREEN OBSOLESCENCE SCORE (SOS-1.0) — DOMAIN: [0, ∞)                |
|   "From zero-screen ideation on a machine to value accrual, robotics, wet labs,   |
|                         and inverse material design"                              |
+-----------------------------------------------------------------------------------+
         |                          |                         |                  |
         v                          v                         v                  v
+------------------+     +--------------------+     +------------------+  +------------------+
| PILLAR I: AIO    |     | PILLAR II: CTX     |     | PILLAR III: CRE  |  | PILLAR IV: JDG   |
| Audible Inputs   |     | Passive & Active   |     | Creation & LLM-  |  | Independent      |
| & Outputs        |     | Context Assembly   |     | Managed Screen   |  | Judgment         |
| (Ref: 100 | 0-∞) |     | (Ref: 100 | 0-∞)   |     | (Ref: 100 | 0-∞) |  | (Ref: 100 | 0-∞) |
+------------------+     +--------------------+     +------------------+  +------------------+
| AIO-1 Spoken In  |     | CTX-1 Passive Mem  |     | CRE-1 Paper Gen  |  | JDG-1 Epistemic  |
| AIO-2 2D->1D Out |     | CTX-2 Active Hunt  |     | CRE-2 Art/Image  |  | JDG-2 Aesthetic  |
| AIO-3 Audio Zoom |     | CTX-3 Drift/Prov   |     | CRE-3 Self-Screen|  | JDG-3 Tactical   |
| AIO-4 Zero-GUI   |     | CTX-4 Zero-Copy    |     | CRE-4 CrossModal |  | JDG-4 Escalation |
+------------------+     +--------------------+     +------------------+  +------------------+
         |                          |                         |                  |
         +--------------------------+------------+------------+------------------+
                                                 |
                                                 v
+-----------------------------------------------------------------------------------+
|             UNBOUNDED FRONTIER REALIZATION HORIZONS (FRI ∈ [0, ∞))                |
|  +-----------------+  +-----------------+  +-----------------+  +---------------+ |
|  | FRH-1: VAL      |  | FRH-2: ROB      |  | FRH-3: WET      |  | FRH-4: MAT    | |
|  | Accrual of      |  | Robotic &       |  | Wet Lab &       |  | Material      | |
|  | Value [0, ∞)    |  | Embodied [0, ∞) |  | Bio/Chem [0, ∞) |  | Design [0, ∞) | |
|  +-----------------+  +-----------------+  +-----------------+  +---------------+ |
+-----------------------------------------------------------------------------------+
```

---

### Pillar I: Audible Inputs and Outputs (`AIO` — 0 to 100 Points)

A screen presents information in parallel across two spatial dimensions ($x, y$), allowing the human eye to skim, jump, and filter. Audio unfolds serially in one temporal dimension ($t$). Therefore, replacing the screen with audio is not achieved by piping terminal stdout into a text-to-speech (`TTS`) engine; it requires **bidirectional acoustic intelligence** and **2D-to-1D semantic transduction**.

#### `AIO-1`: Audible Input Capture, Duplex Flow, and Paralinguistic Fidelity (0–25 pts)
- **0–5 (Absent / Screen-Typed Only):** System accepts only keyboard/pointer text or file inputs; no native speech-to-intent pipeline exists.
- **6–12 (Batch Dictation Wrapper):** System accepts pre-recorded audio files or external OS dictation transcribed into a text box, but lacks continuous listening, turn-taking, or acoustic awareness.
- **13–19 (Interactive Voice Turn-Taking):** System provides a live spoken input channel with automatic endpoint detection, tolerates conversational disfluencies, and maps informal spoken phrasing to structured intents without requiring spoken punctuation or exact symbol spelling.
- **20–25 (Full-Duplex Acoustic Co-Presence):** System supports low-latency full-duplex voice interaction with instant barge-in/interruption, prosodic cue recognition (hesitation, emphasis, urgency), ambient whisper/murmur handling, and zero-wake-fatigue continuous session flow.

#### `AIO-2`: 2D-to-1D Semantic Audio Transduction (0–25 pts)
- **0–5 (Raw Screen Dump):** Output is formatted exclusively for visual reading (Markdown tables, raw code diffs, JSON payloads, long file paths, terminal logs); reading it aloud causes severe cognitive overload (`SFE-IO`).
- **6–12 (Basic Prose Summarization):** System writes prose summaries suitable for reading, but still embeds visual-only constructs (inline code blocks, URLs, line-number tables) as primary carriers of meaning.
- **13–19 (Speech-Native Synthesis):** System restructures complex 2D state (architectural diffs, experimental tables, error traces) into ear-parseable narrative with clear discourse markers, Spoken-First pacing, and zero reliance on visual formatting to convey structure.
- **20–25 (Adaptive Multimodal-to-Acoustic Transduction):** System dynamically translates visual layouts, mathematical proofs, figure topologies, and art compositions into vivid, high-precision spoken briefings tailored to human working-memory constraints ($\le 4$ chunks per turn unless expanded).

#### `AIO-3`: Progressive Audible Zoom and Background Sonification (0–25 pts)
- **0–5 (Monolithic Output):** System emits a single fixed-length response; the user cannot interactively drill down or skim by voice.
- **6–12 (Turn-Based Q&A Drilldown):** User can ask follow-up questions in text/voice, but long-running tasks emit either silence or visual-only progress bars/logs.
- **13–19 (Hierarchical Audible Navigation):** System organizes output into navigable acoustic layers (Headline $\rightarrow$ Executive Argument $\rightarrow$ Evidence/Component $\rightarrow$ Exact Verbatim Span) controllable by voice commands ("skip that", "zoom in on the second claim", "read the exact equation").
- **20–25 (Spatial & Earcon Sonification):** In addition to hierarchical voice zoom, background waves, multi-agent deliberations, build states, and anomalies are communicated via non-intrusive acoustic cues/earcons or scheduled spoken check-ins, completely replacing visual dashboards.

#### `AIO-4`: Zero-Screen Lifecycle Bootstrap and Operational Control (0–25 pts)
- **0–5 (Screen Required for Setup & Run):** Launching, configuring, monitoring, and recovering the system requires a terminal, CLI flags, JSON config edits, or a browser GUI.
- **6–12 (CLI-Launched, Voice-Assisted):** A human must start the session on a screen/terminal, after which partial voice interaction is possible until an error or configuration change occurs.
- **13–19 (Headless Daemon with Voice Session Control):** System runs as a persistent background daemon controllable via voice for routine task execution, pausing, and status queries.
- **20–25 (Complete Zero-Screen Sovereignty):** Cold boot, authentication, environment configuration, crash recovery, campaign management, and shutdown can all be executed by the human without ever touching a screen or keyboard.

---

### Pillar II: Passive and Active Context Assembly (`CTX` — 0 to 100 Points)

One of the largest hidden taxes of screen-based computing is **human context assembly**: hunting for the right window, running `rg` or Finder searches, reading old notes, copying file paths, and pasting context into prompts. A system cannot free the human from the screen if the human must still look at a screen to tell the system *what* to work on.

#### `CTX-1`: Passive Ambient and Cross-Session Context Assembly (0–25 pts)
- **0–5 (Stateless / Session-Amnesiac):** Every session starts blank unless the user manually supplies files, paths, or state.
- **6–12 (Explicit Ledger / File Persistence):** System persists state in local JSON/Markdown/SQLite files across runs, but requires explicit task IDs, file paths, or resume commands to reload.
- **13–19 (Automatic Workspace & Temporal Continuity):** System automatically indexes active repositories, recent commits, session journals, and open campaigns on startup, reconstructing "what we were doing" without human prompting.
- **20–25 (Continuous Ambient Epistemic Graph):** System passively maintains an evolving, multi-project temporal memory graph (user taste, prior decisions, rejected hypotheses, live filesystem watchers, external feeds, and cross-session profiles) that silently grounds every utterance.

#### `CTX-2`: Active Multi-Source Epistemic Hunting (0–25 pts)
- **0–5 (Caller-Supplied Context Only):** System operates only on files or text explicitly handed to it by the caller.
- **6–12 (Single-Repo Lexical/Vector Search):** System can search the current directory when asked, but fails on oblique references or cross-corpus dependencies.
- **13–19 (Autonomous Multi-Hop Discovery):** Given an underspecified intent, the system actively formulates search hypotheses, traverses codebases, documentation, git history, and external web/literature sources, and ranks relevance via calibrated decision gates.
- **20–25 (Omniscient Active Grounding):** System resolves deictic, temporal, and conceptual spoken references ("fix the bottleneck we saw in the second path yesterday and align it with the NAACL baseline") across local repos, scholarly literature, runtime logs, and enterprise/personal stores with zero human path hints.

#### `CTX-3`: Source Provenance, Freshness, and Drift Invalidation (0–25 pts)
- **0–5 (Unbound Context Window):** Retrieved snippets and summaries float in context without revision bindings; stale summaries silently masquerade as current truth.
- **6–12 (Timestamp/Hash Logging):** System logs file hashes or timestamps in artifacts, but does not automatically invalidate downstream reasoning when underlying sources mutate.
- **13–19 (Revision-Bound Snapshots & Drift Detection):** Context bundles bind claims to explicit source revisions/digests, detect worktree drift or concurrent edits, and force re-reading of mutated files before acting.
- **20–25 (Transactional Proof-Barrier Context Compiler):** System maintains a formal dependency graph over source revisions, representations, and authority epochs, automatically invalidating and recompiling affected context records upon any source change so the human never has to visually audit whether context is stale.

#### `CTX-4`: Zero-Copy, Zero-Pointer Context Ergonomics (0–25 pts)
- **0–5 (Heavy Manual Plumbing):** User must regularly copy-paste errors, paths, URLs, or task JSON payloads to drive the workflow.
- **6–12 (Structured Command Invocation):** User avoids raw copy-paste of file contents, but must still supply exact CLI flags, file paths, or task identifiers.
- **13–19 (Intent-Driven Workspace Resolution):** User states high-level goals in natural language; the system resolves target workspaces, files, and dependencies autonomously.
- **20–25 (Zero-Touch Context Assembly):** Across an entire multi-day project, the human never types a path, never pastes a snippet, never selects an item from a visual menu, and never manages window focus.

---

### Pillar III: Creation Across Modalities and LLM-Managed Screen Stewardship (`CRE` — 0 to 100 Points)

This pillar captures the leap **beyond the scribe**. Because an LLM-coupled computer can generate **papers, art, images**, and interactive software, leaving the screen behind requires that **the LLM side take full ownership of the screen**—rendering visual and spatial artifacts internally, inspecting them with machine vision and structural critics, and iterating until they are complete.

#### `CRE-1`: Paper, Manuscript, and Formal Document Generation (0–25 pts)
- **0–5 (Plain Text / Snippet Only):** System outputs only chat fragments or unformatted text notes.
- **6–12 (Markdown/Draft Generation Without Typesetting Loop):** System authors structured Markdown reports, PRDs, or raw LaTeX/DOCX source, but relies on the human to compile, format, or visually check pagination and layout.
- **13–19 (Automated Typeset Compilation & Structural Validation):** System autonomously synthesizes full-length research papers or formal technical specifications complete with equations, tables, citations, and bibliography, and compiles them into target deliverables (e.g., PDF/DOCX).
- **20–25 (Publication-Grade Autonomous Paper Foundry):** System conducts end-to-end paper creation—literature grounding, theorem/proof checking, figure generation, LaTeX/PDF compilation, and page-level visual inspection of every rendered page (margins, float placement, widow/orphan control, equation overflow)—delivering camera-ready manuscripts without human screen review.

#### `CRE-2`: Art, Image, and Visual Media Synthesis (0–25 pts)
- **0–5 (No Visual Synthesis):** System is text/code-only and cannot generate or manipulate art, images, diagrams, or visual shaders.
- **6–12 (Single-Shot Prompt-to-Image Tool Call):** System can invoke an external image generator or write SVG/shader/chart code, but treats generation as a blind one-shot call without iterative visual refinement.
- **13–19 (Multi-Stage Visual Asset Pipeline):** System orchestrates structured generation of diagrams, data visualizations, UI canvases, 3D/shader scenes, or raster/vector art with programmatic layout constraints and style consistency.
- **20–25 (Autonomous Studio for Art & Visual Media):** System directs complex multi-pass art and image creation (concept exploration, composition locking, palette/lighting control, typography integration, animation/video framing, and surgical inpainting/refinement) entirely from high-level non-visual human direction.

#### `CRE-3`: LLM-Owned Screen Loop — Machine Rendering and Closed-Loop Visual Self-Inspection (0–25 pts)
- **0–5 (Blind Emission / Human Is the Framebuffer):** System writes HTML, SwiftUI, LaTeX, plots, or images and immediately hands them to the human without ever rendering and looking at the pixels (`SFE-VIS`).
- **6–12 (DOM/AST/Compile Check Only):** System verifies that UI/document/graphic code compiles or passes DOM/schema checks, but does not inspect rendered pixels for visual defects (overlapping text, contrast failure, broken layout, visual artifacts).
- **13–19 (Headless Capture + Vision Critic Loop):** System renders outputs onto a headless/virtual screen (headless browser, offscreen Metal/OpenGL framebuffer, PDF rasterizer), captures screenshots/frames, evaluates them with a multimodal vision critic, and performs bounded repair loops.
- **20–25 (Complete LLM Screen Sovereignty):** Every visual surface—whether an OS application window, a web app, a typeset paper, a scientific plot, or a piece of generative art—is rendered, navigated, visually audited at pixel level, and iteratively perfected on an LLM-managed virtual screen before the human is ever informed of completion.

#### `CRE-4`: Cross-Modal Synthesis and Deliverable Packaging (0–25 pts)
- **0–5 (Isolated Fragments):** Code, text, and visuals exist as disconnected outputs requiring human assembly.
- **6–12 (Repo-Level File Co-Location):** System writes code, tests, and documentation into a shared repository structure.
- **13–19 (Integrated Multi-Artifact Workflows):** System couples executable experiments/code directly to generated figures, tables, and narrative reports so that quantitative outputs flow automatically into final documents.
- **20–25 (End-to-End Autonomous Production Pipeline):** System seamlessly fuses computation, empirical benchmarks, generated art/figures, typeset papers, and deployed services into verified, release-ready packages with zero human screen assembly.

---

### Pillar IV: Independent Judgment (`JDG` — 0 to 100 Points)

Without **independent judgment**, a screenless interface is merely an exhausting voice-activated puppet. If the system cannot judge truth, quality, aesthetics, and operational risk on its own, either the human must open a screen to verify the work (`SFE-JDG`) or the human must act as a full-time verbal micromanager.

#### `JDG-1`: Epistemic, Empirical, and Adversarial Self-Verification (0–25 pts)
- **0–5 (Unverified Assertion):** System trusts its own single-pass generation; hallucinations, subtle bugs, and unverified claims are reported as done.
- **6–12 (Basic Test/Lint Gate):** System runs existing unit tests or linters before reporting, but does not design new falsification checks or question flawed assumptions.
- **13–19 (Multi-Path Exploration & Independent Judge Battery):** System explores competing hypotheses/paths in parallel, subjects candidates to an independent adversarial judge or verification battery, and strictly separates verified observations from inferences and unknowns.
- **20–25 (Self-Falsifying Scientific & Formal Rigor):** System autonomously designs decisive experiments, statistical null-control calibrations, and adversarial audits; refuses to promote unverified claims; and proves presence/absence against immutable source/execution evidence before reporting.

#### `JDG-2`: Autonomous Aesthetic, Rhetorical, and Compositional Judgment (0–25 pts)
- **0–5 (Zero Taste Filter):** System emits generic, cliché, poorly proportioned, or rhetorically weak prose, art, and layouts as long as they are syntactically valid.
- **6–12 (Rule-Based Style Checklists):** System enforces basic formatting or prose rules (e.g., banned words, linter rules, schema templates) without holistic compositional judgment.
- **13–19 (Multi-Criterion Quality & Design Evaluation):** System evaluates candidate narratives, designs, or visual artifacts against explicit domain rubrics (information density, clarity, visual hierarchy, originality), pruning weak candidates autonomously.
- **20–25 (Calibrated Autonomous Taste & Editorial Authority):** System exercises high-dimensional editorial and aesthetic judgment across papers, art, images, and architecture—iteratively rejecting mediocre compositions, refining visual/prose harmony, and surfacing only work that meets a high bar of craft.

#### `JDG-3`: Long-Horizon Tactical Autonomy and Self-Healing (0–25 pts)
- **0–5 (Fragile Single-Turn Execution):** System halts or asks the user for help on the first compiler error, timeout, missing dependency, or ambiguous file location.
- **6–12 (Bounded Local Retry):** System retries failed commands a few times within a single turn, but loses momentum across larger multi-step obstacles.
- **13–19 (Multi-Wave Orchestration & Diagnostic Recovery):** System decomposes large goals into dependency-ordered task waves, dispatches isolated workers, diagnoses root causes across layers, and recovers from failed branches without human intervention.
- **20–25 (Elastic Multi-Session Autonomous Drive):** System sustains coherent execution across hours or days via durable ledgers, watchdogs, automatic replanning, and self-healing recovery loops, treating obstacles as engineering problems to solve rather than reasons to stop.

#### `JDG-4`: Calibrated Principal Escalation Boundary (0–25 pts)
- **0–5 (Chronic Over- or Under-Escalation):** System either asks permission for trivial implementation choices ("Should I edit `utils.py`?") or silently makes destructive/unauthorized policy changes.
- **6–12 (Static Permission Prompts):** Escalation is governed by rigid tool-call approval prompts rather than semantic understanding of principal authority vs. worker execution.
- **13–19 (Policy-Aware Autonomous Resolution):** System resolves technical, architectural, and formatting decisions autonomously within declared charter bounds, escalating only genuine requirement conflicts or external blockers.
- **20–25 (Optimal Principal Bandwidth Conservation):** System treats human attention as the scarcest resource: zero tactical interruptions, 100% adherence to safety/authority boundaries, and concise, decision-ready framing whenever a true principal value judgment is required.

---

### Unbounded Frontier Realization Horizons (`FRH` — `[0, ∞)` Points)

Why does `SOS-1.0` have **no upper ceiling**? Because once a human being no longer needs a screen to ideate, assemble context, create multimodal artifacts, and verify truth on a computer (`100.00` Reference Digital Baseline), the boundary of what can be solved by channeling intent through the machine expands outward into the physical, economic, biological, and material world:

1. **`FRH-1` (`VAL` — Accrual of Value, `[0, ∞)` pts):**  
   Measures how completely the system closes the loop from digital creation on a machine to **real-world accrual of value** without human screen supervision—autonomous service deployment, user/customer acquisition loops, market telemetry feedback, capital/resource allocation, revenue or utility generation, and compounding operational value.
2. **`FRH-2` (`ROB` — Robotic & Embodied Development, `[0, ∞)` pts):**  
   Measures closed-loop **robotic and physical system development**—CAD/kinematic synthesis, sensorimotor policy training, sim-to-real transfer, mechatronic fabrication, hardware-in-the-loop bring-up, and autonomous physical manipulation without human teleoperation monitors.
3. **`FRH-3` (`WET` — Wet Lab Development, `[0, ∞)` pts):**  
   Measures closed-loop **wet-lab biological, chemical, and life-science experimentation**—compiling spoken scientific hypotheses into cloud-lab, microfluidic, or liquid-handling robotic protocols, executing physical assays, ingesting raw instrument telemetry (mass spectrometry, sequencing, microscopy), and iterating experimental rounds autonomously.
4. **`FRH-4` (`MAT` — Material Design & Matter Synthesis, `[0, ∞)` pts):**  
   Measures end-to-end **inverse material design and matter realization**—generative crystal/polymer/alloy/metamaterial design, multi-scale quantum/DFT/molecular-dynamics simulation, autonomous synthesis pathway compilation, physical synthesis execution, and diffractometry/spectroscopy characterization closure.

---

## 4. Mathematical Formulation of the Score (Unbounded `[0, ∞)` Domain)

### 4.1 Pillar Totals and Open-Ended Sub-Dimensions

Each sub-dimension $x_{p,i} \in [0, \infty)$ has **no upper ceiling** (`25.0` is the Digital Reference Sovereign Anchor; scores $> 25.0$ represent open-ended super-human/autonomous mastery). Each core pillar score $P_k \in [0, \infty)$ for $k \in \{\text{AIO}, \text{CTX}, \text{CRE}, \text{JDG}\}$ (`100.0` Digital Reference Anchor) is the sum of its four sub-dimension scores:

$$\text{AIO} = \sum_{i=1}^{4} \text{AIO}_i, \quad \text{CTX} = \sum_{i=1}^{4} \text{CTX}_i, \quad \text{CRE} = \sum_{i=1}^{4} \text{CRE}_i, \quad \text{JDG} = \sum_{i=1}^{4} \text{JDG}_i \in [0, \infty)$$

The **Frontier Realization Index (`FRI`)** sums the four unbounded frontier horizons ($\text{VAL}, \text{ROB}, \text{WET}, \text{MAT} \in [0, \infty)$, defaulting to $0$ when a system operates purely on digital ideation-to-machine tasks):

$$\text{FRI} = \text{VAL} + \text{ROB} + \text{WET} + \text{MAT} \in [0, \infty)$$

### 4.2 Latent Post-Screen Capability Score (`SOS_latent`)

The **Base Digital Latent Score (`SOS_base_latent`)** is the arithmetic mean of the four core pillars, and the total **Latent Post-Screen Capability Score (`SOS_latent`)** adds the unbounded Frontier Realization Index:

$$\text{SOS}_{\text{base\_latent}} = \frac{\text{AIO} + \text{CTX} + \text{CRE} + \text{JDG}}{4} \in [0, \infty)$$

$$\text{SOS}_{\text{latent}} = \text{SOS}_{\text{base\_latent}} + \text{FRI} = \frac{\text{AIO} + \text{CTX} + \text{CRE} + \text{JDG}}{4} + (\text{VAL} + \text{ROB} + \text{WET} + \text{MAT}) \in [0, \infty)$$

### 4.3 Effective Screen-Free Liberation Score (`SOS_effective`)

In the hypothetical scenario `H-SEALED-SCREEN`, the four core pillars form a **serial survival chain**. Even if a system connects to wet-lab instruments or trading/deployment APIs, if its audible I/O (`AIO`) or LLM-owned screen inspection (`CRE-3`) is broken, the human principal is still forced back to a screen (`SFE-IO`, `SFE-VIS`, `SFE-JDG`).

Therefore, `SOS-1.0` defines the canonical headline metric—the **Effective Screen-Free Liberation Score (`SOS_effective`)** on the unbounded interval **`[0, ∞)`**—by coupling `SOS_latent` with the **Bottleneck Balance Factor (`BBF`)**:

$$\text{BBF} = \sqrt{\frac{\min(\text{AIO}, \text{CTX}, \text{CRE}, \text{JDG}) + \epsilon}{\max(\text{AIO}, \text{CTX}, \text{CRE}, \text{JDG}) + \epsilon}} \in (0, 1], \quad \text{where } \epsilon = 10$$

$$\text{SOS}_{\text{effective}} = \text{round}\left(\text{SOS}_{\text{latent}} \times \text{BBF},\, 2\right) \in [0, \infty)$$

- **Why $\epsilon = 10$, exponent $\gamma = 0.5$, and no upper ceiling (`[0, ∞)`):**  
  A pure geometric mean collapses to $0$ if any pillar is $0$, obscuring substantial architectural progress in headless autonomy. Adding $\epsilon = 10$ and taking the square root ($\gamma = 0.5$) penalizes severe modality bottlenecks honestly (e.g., a headless system with `AIO = 0` and other pillars at `80` receives $\text{BBF} = \sqrt{10/90} = 0.333$, reducing a `60.0` latent score to an effective `20.0`) while preserving strict monotonicity of `SOS_latent` across all 16 sub-dimensions and 4 frontier horizons, strict monotonicity of `SOS_effective` across the bottleneck pillar, non-maximum pillars, and all 4 frontier horizons, and **unbounded upward scaling ($\lim \text{SOS}_{\text{effective}} = \infty$)** as problem-solving expands from machine ideation into value accrual, robotics, wet labs, and material design.

### 4.4 Scribe-to-Post-Screen & Unbounded Frontier Maturity Tiers

Every `SOS-1.0` evaluation MUST classify the system into one of nine normative tiers (`Level 0` through `Level 8`, where `Level 8` has **no upper ceiling**: `[220.00, ∞)`) based on `SOS_effective` and mandatory floor requirements:

| Tier | Name | `SOS_effective` Range | Floor Requirement | Custom Design Badge | Operational Meaning (`H-SEALED-SCREEN` $\rightarrow$ Physical Reality) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Level 0** | **Manual Screen Labor** | `0.00 – 19.99` | None | ![Level 0 Badge](badges/level-0-manual-screen-labor.svg) | Human performs primary reading, writing, navigation, and verification directly on the screen. |
| **Level 1** | **Assisted Screen Scribe** | `20.00 – 39.99` | All pillars $\ge 5$, or bottlenecked engine | ![Level 1 Badge](badges/level-1-assisted-screen-scribe.svg) | LLM accelerates drafting or coding, but the human remains tethered to a screen-based CLI/IDE/viewer for I/O or visual inspection. |
| **Level 2** | **Headless Cognitive Engine (Screen-Tethered Boundary)** | `40.00 – 59.99` | At least two pillars $\ge 50$ | ![Level 2 Badge](badges/level-2-headless-cognitive-engine.svg) | System exhibits substantial autonomous context, creation, or judgment internally, but requires human screen fallback for acoustic I/O or visual QA. |
| **Level 3** | **Supervised Screen-Free Delegation** | `60.00 – 79.99` | All four pillars $\ge 50$ | ![Level 3 Badge](badges/level-3-supervised-screen-free-delegation.svg) | Human operates primarily without a screen via bidirectional audio; LLM manages virtual screens for most creation and verification. |
| **Level 4** | **Autonomous Screen Stewardship** | `80.00 – 94.99` | All four pillars $\ge 75$ | ![Level 4 Badge](badges/level-4-autonomous-screen-stewardship.svg) | System manages the screen end-to-end across papers, art, images, and code with closed-loop visual critics and full-duplex audio. |
| **Level 5** | **Post-Screen Liberation (Ideation-on-Machine Closure)** | `95.00 – 119.99` | All four pillars $\ge 90$ | ![Level 5 Badge](badges/level-5-post-screen-digital-sovereign.svg) | Computer operation as a human visual-spatial base skill is obsolete. Ideation on a machine to verified software, papers, art, and images is 100% closed-loop. |
| **Level 6** | **Autonomous Value Accrual** | `120.00 – 159.99` | All four pillars $\ge 90$ and `VAL >= 15` | ![Level 6 Badge](badges/level-6-autonomous-value-accrual-sovereign.svg) | System solves problems from spoken ideation on a machine through autonomous deployment, operational feedback, and measurable **accrual of value** (`VAL`). |
| **Level 7** | **Robotic and Wet-Lab Execution** | `160.00 – 219.99` | All four pillars $\ge 95$, `VAL >= 20`, and (`ROB >= 20` or `WET >= 20`) | ![Level 7 Badge](badges/level-7-robotic-wetlab-sovereign.svg) | Screenless autonomy extends into physical actuation—closing the loop across **robotic development** (`ROB`) and/or **wet-lab experimentation** (`WET`). |
| **Level 8** | **Open-Ended Material and Physical Synthesis** | `220.00 – ∞` *(No Upper Ceiling)* | All four pillars $\ge 95$, `VAL >= 25`, (`ROB >= 25` or `WET >= 25`), and `MAT >= 25` | ![Level 8 Badge](badges/level-8-unbounded-matter-reality-foundry.svg) | Open-ended horizon (`[220.00, ∞)`): works and solves problems end-to-end from **ideation on a machine $\rightarrow$ accrual of value $\rightarrow$ robotic/wet-lab development $\rightarrow$ inverse material design (`MAT`)**. |

> **Normative Tier Cap Rule (`RULE-TIER-CAP`):**  
> Even if `SOS_effective` exceeds a tier threshold numerically, a system MUST NOT be certified at **Level 3 or higher** unless `AIO >= 50` AND `CRE-3 (LLM-Owned Screen Loop) >= 13`. Furthermore, **Level 6** requires `VAL >= 15`, **Level 7** requires `VAL >= 20` and $\max(\text{ROB}, \text{WET}) \ge 20$, and **Level 8 (`[220.00, ∞)`)** requires `VAL >= 25`, $\max(\text{ROB}, \text{WET}) \ge 25$, and `MAT >= 25`.

### 4.5 Custom Design Badges Specification (`SOS-BADGE-1.0`)

Each normative level (`Level 0` through `Level 8`) has an archival specification-plate SVG badge (`badges/level-<N>-*.svg`) featuring a restrained `1.2px` monochrome orthographic/mathematical schematic diagram on a coordinate reticle, classical serif and tabular monospace typography, and a clean bracketed notation string:

| Level | Technical Schematic Diagram (`1.2px` Orthographic Line Glyph) | Archival Ink Tone | Inline Metrological Notation | SVG Asset |
| :---: | :--- | :--- | :--- | :--- |
| **L0** | **Cartesian Viewport Plane** — 2D rectangular viewport with orthogonal partition lines | Slate (`#334155` / `#64748b`) | `[SOS-1.0 \| Level 0 \| 0.00–19.99 \| Manual Screen Labor]` | [`level-0-manual-screen-labor.svg`](badges/level-0-manual-screen-labor.svg) |
| **L1** | **Typographic Baseline Register** — Parallel horizontal text baselines inside a document margin | Oxford Slate (`#1e3a5f` / `#475569`) | `[SOS-1.0 \| Level 1 \| 20.00–39.99 \| Assisted Screen Scribe]` | [`level-1-assisted-screen-scribe.svg`](badges/level-1-assisted-screen-scribe.svg) |
| **L2** | **Partitioned Directed Graph** — Three-node directed graph ($G=(V,E)$) with dashed I/O boundary | Prussian Slate (`#1e293b` / `#334155`) | `[SOS-1.0 \| Level 2 \| 40.00–59.99 \| Headless Cognitive Engine]` | [`level-2-headless-cognitive-engine.svg`](badges/level-2-headless-cognitive-engine.svg) |
| **L3** | **Harmonic Temporal Axis** — Continuous 1D waveform $\psi(t)$ along a horizontal time axis | Muted Verdigris (`#134e4a` / `#2d6a64`) | `[SOS-1.0 \| Level 3 \| 60.00–79.99 \| Supervised Screen-Free Delegation]` | [`level-3-supervised-screen-free-delegation.svg`](badges/level-3-supervised-screen-free-delegation.svg) |
| **L4** | **Closed-Loop Feedback Schematic** — Classical two-block control loop ($\text{Render} \to \text{Critic}$) | Deep Steel (`#1e3a5f` / `#3b5980`) | `[SOS-1.0 \| Level 4 \| 80.00–94.99 \| Autonomous Screen Stewardship]` | [`level-4-autonomous-screen-stewardship.svg`](badges/level-4-autonomous-screen-stewardship.svg) |
| **L5** | **Commutative Closure Square** — Four-vertex commutative diagram with diagonal morphism | Charcoal Ink (`#0f172a` / `#334155`) | `[SOS-1.0 \| Level 5 \| 95.00–119.99 \| Post-Screen Liberation]` | [`level-5-post-screen-digital-sovereign.svg`](badges/level-5-post-screen-digital-sovereign.svg) |
| **L6** | **Cumulative Utility Integral** — Monotonic step function on orthogonal axes | Graphite (`#27272a` / `#52525b`) | `[SOS-1.0 \| Level 6 \| 120.00–159.99 \| Autonomous Value Accrual]` | [`level-6-autonomous-value-accrual-sovereign.svg`](badges/level-6-autonomous-value-accrual-sovereign.svg) |
| **L7** | **Orthogonal 3-Axis Triad & Assay Cell** — $(x, y, z)$ spatial frame paired with an experimental cell | Archival Iron (`#18181b` / `#3f3f46`) | `[SOS-1.0 \| Level 7 \| 160.00–219.99 \| Robotic and Wet-Lab Execution]` | [`level-7-robotic-wetlab-sovereign.svg`](badges/level-7-robotic-wetlab-sovereign.svg) |
| **L8** | **Isometric Cubic Unit Cell & Open Ray** — Bravais lattice unit cell with open ray $[0, \infty)$ | Obsidian Ink (`#090d16` / `#1e293b`) | `[SOS-1.0 \| Level 8 \| 220.00–∞ \| Open-Ended Material and Physical Synthesis]` | [`level-8-unbounded-matter-reality-foundry.svg`](badges/level-8-unbounded-matter-reality-foundry.svg) |

---

## 5. Reference Benchmark Scenarios (`SOS-BENCH-5`)

When applying `SOS-1.0` to a target system, the evaluator MUST assess how the system behaves across five standardized reference scenarios under `H-SEALED-SCREEN`:

1. **`SCN-1` (Spoken Research Loop to Camera-Ready Paper):**  
   The human speaks a research problem in two sentences. The system must assemble literature and local codebase context, run competing experimental/analytical paths, judge the results adversarially, generate a complete typeset paper with figures, inspect the rendered PDF pages on its own virtual screen, and deliver a concise spoken defense.
2. **`SCN-2` (Blind Direction of Art, Image, and Visual Experience):**  
   The human describes an aesthetic concept or visual explanation audibly. The system must generate the visual art, images, shaders, or motion frames, render them onto an LLM-managed framebuffer, inspect the pixels for composition, legibility, and visual defects, iterate autonomously, and report the verified aesthetic state audibly.
3. **`SCN-3` (Zero-Hint Ambient Resumption):**  
   The human says, *"Pick up where we left off on the failing campaign and finish the remaining verification"* without naming a repository, task ID, file path, or branch. The system must passively and actively assemble the exact state and execute to completion.
4. **`SCN-4` (Multi-Hour Autonomous Engineering Under Fault Injection):**  
   The system is given a complex multi-file build/refactor objective where intermediate tests fail and a service dependency errors. The system must diagnose, self-heal, validate startup behavior, and report audibly without human screen intervention.
5. **`SCN-5` (Epistemic & Aesthetic Trap Resistance):**  
   The human gives a spoken instruction containing a plausible-sounding false technical premise or requests a visual/paper output prone to layout corruption. The system must exercise independent judgment to falsify the premise and repair the visual corruption before reporting.

---

## 6. Normative Evaluation Procedure and Reporting Contract

Every evaluation conducted under `SOS-1.0` MUST obey the following rules:

1. **Sequence Gate (`RULE-SEQ-01`):** The standard document MUST exist at its canonical path before any target system is scored against it.
2. **Scope Separation (`RULE-SCOPE-02`):** The evaluator MUST distinguish between:
   - **Native Target Scope:** Capabilities implemented directly inside the target repository/system under evaluation.
   - **Host/Ecosystem Coupled Scope:** Capabilities available when the target system is coupled with its surrounding host runtime (e.g., host voice/TTS tools, browser/vision MCP servers, computer-use agents), evaluated separately if relevant so neither is conflated with the other.
3. **Evidence Binding (`RULE-EVID-03`):** Every sub-dimension score MUST cite concrete source files, line ranges, architectural mechanisms, or verified absences (`OBSERVATION`), explain the scoring derivation (`INFERENCE`), and state any boundary conditions (`ASSUMPTION` / `UNKNOWN`).
4. **Required Output Table (`RULE-TABLE-04`):** Every evaluation report MUST present:
   - All 16 sub-dimension scores (`AIO-1..4`, `CTX-1..4`, `CRE-1..4`, `JDG-1..4`) with reference anchor `25` (`[0, ∞)` open-ended).
   - All 4 core pillar totals (`AIO`, `CTX`, `CRE`, `JDG`, reference anchor `100`, `[0, ∞)` open-ended) and the 4 Frontier Realization Horizons (`VAL`, `ROB`, `WET`, `MAT` $\in [0, \infty)$, `FRI`).
   - Exact calculations for `SOS_base_latent`, `FRI`, `SOS_latent`, `BBF`, `SOS_effective` $\in [0, \infty)$, the resulting Maturity Tier (`Level 0`–`Level 8`, applying `RULE-TIER-CAP` if triggered), and its corresponding Custom Design Badge.
   - Scenario-by-scenario `SFE` (Screen Fallback Event) analysis across `SCN-1` through `SCN-5`.
   - Concrete architectural delta required to advance the target system to the next Maturity Tier, to `Level 5 (Post-Screen Liberation)`, and into the unbounded Frontier Horizons (`Level 6` Value Accrual $\rightarrow$ `Level 7` Robotic/Wet-Lab $\rightarrow$ `Level 8` Material & Physical Synthesis `[220.00, ∞)`).
