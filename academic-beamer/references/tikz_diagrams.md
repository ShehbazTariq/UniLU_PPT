# TikZ Diagrams For UniLU/SnT Beamer

Use this reference for conceptual diagrams, workflows, architectures, networks, state transitions,
and quantum-system schematics. Use the PGFPlots skill for data-driven plots and `quantikz` for
quantum circuits.

## Artifact Contract

Keep editable TikZ source in `Sections/` or a project-local `figures/tikz/<slug>/` folder. For a
diagram that needs isolated iteration, retain:

```text
figures/tikz/<slug>/
  <slug>.tex
  qa/<version>/page-001.png
  qa/<version>/tikz-slide-qa.json
```

Do not commit `_preview.*`, auxiliary LaTeX files, or disposable QA renders to the template repo.
The deck source and its relative assets remain the source of truth.

## Design Gate

Before drawing, state the diagram's single job and choose one grammar:

| Job | Grammar |
| --- | --- |
| Ordered processing | left-to-right flow |
| Quantum/classical architecture | aligned layers or swimlanes |
| Network or MIMO topology | typed nodes and links |
| Protocol progression | state machine or sequence |
| Adaptation | forward path with an outside return edge |
| Causal assumptions | directed acyclic graph |
| Before/after explanation | matched panels with shared geometry |

Split a slide that tries to combine a full architecture, benchmark plot, equations, and a result
table. The frame action title states the conclusion; do not repeat a title, subtitle, interpretation
paragraph, or source block inside the TikZ picture.

Record the logic status in the QA command:

- `exact`: geometry follows equations, source values, or protocol rules.
- `schematic`: only qualitative structure is intended; avoid exact-looking scales or coordinates.
- `needs-source`: the relation is not verified; do not present it as established.

## Stable Slide Geometry

- Define semantic styles separately from coordinates. Use named nodes and anchors.
- Give variable-length nodes a `text width`, `minimum width`, `minimum height`, and alignment.
- Keep labels short and readable at normal presentation distance. Do not use `\tiny` to rescue a
  crowded slide.
- Connect node borders, not coordinates inside boxes. Route feedback edges outside the main flow.
- Position edge labels explicitly with `above`, `below`, `sloped`, `auto`, or `pos=...`; mask the
  line behind a label when needed.
- Keep the frame-title region and footer/logo band clear. If the diagram needs aggressive scaling,
  simplify or split it.
- Use restrained, grayscale-safe colors. Color must identify a role, state, or emphasis.

## Overlays

Keep coordinates and node dimensions identical on every overlay. Draw the full structure once, then
use `\onslide`, `\uncover`, `visible on`, or `alt` to reveal labels or change emphasis. Avoid placing
geometry inside `\only` when its disappearance would reflow or resize the picture.

Prefer Beamer overlays to `animate.sty`. Use animation only when motion itself explains traversal,
accumulation, or convergence and the delivery environment is known to support it.

For overlay-aware TikZ styles, load `overlay-beamer-styles` only when the deck already supports the
library; otherwise use ordinary Beamer commands around fixed TikZ elements.

## Quantum Diagrams

- Separate quantum evolution and measurement from classical estimation, optimization, or readout.
- For reservoir computing, distinguish encoding, reservoir dynamics, measured observables, and the
  trained readout. Do not visually imply that fixed reservoir parameters are optimized.
- Distinguish quantum channels from classical control or side information using edge style as well
  as color, and explain that encoding in the frame or notes.
- Use `quantikz` and standard gate notation for circuits. Keep a conceptual architecture and its
  circuit realization separate unless their mapping is the point of the slide.

## Source And Caption Practice

Use `\framecite{...}` for literature provenance. Include author/year, paper title, and DOI or arXiv
link as required by `presentation_rules.md`. Put assumptions, schematic limits, and longer
interpretation in speaker notes. Never invent a topology, causal edge, or parameter ordering to fill
visual space.

## QA Workflow

1. Preview the source or labeled frame with `preview.ps1`.
2. Run the QA script on the source and preview PDF:

```powershell
conda run -n SigCOM python academic-beamer/scripts/tikz_slide_qa.py `
  Sections/03_model.tex --pdf _preview.pdf --logic schematic --decision keep
```

3. Inspect every rendered overlay PNG at intended slide size. Check reading order, clipped labels,
   arrow/text collisions, stable geometry, footer clearance, and whether each overlay is true.
4. Make one focused repair and rerun. After two failed repairs to the same defect, simplify or split
   the diagram.
5. Run the full two-pass `build.ps1` before delivery.

The script performs source lint, PDF nonblank checks, text-box overlap checks, footer intrusion checks,
and versioned PNG/JSON output. These checks cannot establish scientific correctness; the author must
still verify equations, causal direction, thresholds, and overlay semantics.

## Completion Gate

- The diagram has one clear job and an action title outside the picture.
- Logic is recorded as `exact`, `schematic`, or `needs-source`.
- Literature-dependent relations have a source and any schematic limits are stated.
- Every overlay is rendered and inspected; node geometry does not jump.
- No label, arrowhead, frame title, citation, or footer logo collision remains.
- The decision is recorded as `keep`, `simplify`, `split`, or `reject`.

