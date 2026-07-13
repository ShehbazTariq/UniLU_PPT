# UniLU Academic Deck Review Workflow

Choose the narrowest review mode that answers the request. Reviews are
read-only by default; edit only when the user asks for corrections or an
upgrade.

## Review Modes

### Proofread

Check grammar, terminology, notation, citation text, cross-references, and
action-title clarity. Do not change technical meaning silently.

### Structural Audit

Run `deck_audit.py` and inspect the ghost deck. Check source-frame count against
speaking time, section balance, overlay practice, density, placeholders,
assets, references, and build-log health.

### Visual And Layout Audit

Build twice, render the compiled PDF, and inspect every edited page and overlay.
Check title and closing geometry, footer clearance, text and equation fit,
figure legibility, table spacing, contrast, and stable overlay geometry. Source
inspection alone cannot pass this mode.

### Pedagogy Review

Check whether the audience can follow the argument:

- the research question or design problem appears by frame 2 or 3
- motivation precedes definitions and machinery
- symbols and assumptions are introduced before use
- formal runs are interrupted by examples, diagrams, or results
- comparisons are simultaneous when side-by-side judgment matters
- the summary answers the opening question and states durable takeaways

### Comprehensive Review

Combine proofreading, structural, visual, pedagogical, and domain checks. For a
scientific deck, verify claims against supplied evidence and identify any point
that requires an author or domain-expert decision.

### Devil's-Advocate Review

Generate the strongest plausible audience questions, grouped by assumptions,
method, evidence, interpretation, limitations, and reproducibility. For each
question, identify the best current response and whether a backup frame or
source check is needed. Do not manufacture weaknesses merely to populate a
list.

## Standard Finding

Report issues in descending severity. Every actionable finding should include:

```text
Location: Sections/05_results.tex, frame "The gain persists under loss"
Severity: critical | major | minor
Current: what the source or rendered page presently shows
Risk: why it affects correctness, comprehension, or presentation
Proposal: the smallest concrete correction
```

Use **critical** for scientific errors, missing required evidence, unreadable or
clipped content, and build failures. Use **major** for argument, pacing, or
layout problems that materially weaken the talk. Use **minor** for local prose,
spacing, or consistency improvements.

If no issue is found, say so and state residual risk, such as unverified source
claims or an untested projector/font environment.

## Commands

```powershell
# Source and structure diagnostics
conda run -n SigCOM python academic-beamer/scripts/deck_audit.py example.tex `
  --duration-minutes 15

# Compile and export pages plus a contact sheet for visual review
powershell -ExecutionPolicy Bypass -File academic-beamer/scripts/build.ps1
conda run -n SigCOM python academic-beamer/scripts/deck_audit.py example.tex `
  --log example.log --pdf example.pdf --render-dir deck-audit/rendered `
  --report deck-audit/report.json
```

The audit returns nonzero for errors. Use `--warnings-as-errors` only for a
strict project gate; advisory findings can be valid exceptions in real decks.
Mark an intentional static legend with `% audit: allow-static-list` and an
intentional missing placeholder asset with `% audit: allow-missing-asset`.
Keep either suppression local to the affected frame.
