# UniLU Academic Deck Creation Workflow

Use this workflow for substantial new decks and paper-to-slide conversions. For
small edits, keep the same principles but skip gates that add no value.

## 1. Establish The Talk Contract

Read supplied material before asking content questions. Record what is already
known and ask only for missing decisions that materially affect the deck:

- audience and assumed prerequisites
- venue, talk type, and speaking time
- central claim the audience should remember
- required topics, exclusions, and disclosure constraints
- desired balance of intuition, formalism, evidence, and discussion
- speaker-note and backup-slide needs

Write the result in `content/deck_outline.yaml` or an equivalent local planning
file. Do not force an interview when the brief or existing deck answers these
questions.

## 2. Inventory Sources And Evidence

For each supplied paper, note, result file, or existing figure, identify:

- claims it can support
- equations, definitions, or notation that must remain exact
- figures or tables that may be reused or redrawn
- DOI, arXiv URL, or other public provenance
- uncertainty, conflicts, or missing evidence

Use `content/slide_sources.yaml` for the map when the talk is evidence-heavy.
Never infer a citation from memory when a source can be checked. Extracting a
paper page is not evidence that every statement on the slide comes from that
page.

For a paper figure or page region, use the Poppler helper and retain its
generated provenance CSV:

```powershell
powershell -ExecutionPolicy Bypass -File academic-beamer/scripts/extract_pdf_figure.ps1 `
  -Pdf notes/paper.pdf -Pages 4 -Crop '180,260,1650,900' -Prefix method
```

The crop is `x,y,width,height` in rendered pixels at the selected DPI. Recreate
tables in LaTeX and use the PGFPlots skill for data-driven plots. When the
figure comes from another paper, add a public `\framecite{...}` on its first
slide use; the local provenance CSV is not a visible attribution.

## 3. Budget By Speaking Time

Budget source frames, not PDF overlay pages. Treat these ranges as planning
guidance rather than a target to fill:

| Speaking time | Typical source frames | Core argument |
| --- | ---: | ---: |
| 5 min | 5-7 | 2-3 |
| 10 min | 8-12 | 4-5 |
| 15 min | 10-15 | 5-7 |
| 20 min | 13-18 | 6-9 |
| 45 min | 22-30 | 10-14 |
| 90 min | 45-60 | 25-35 |

Reserve 40-50% of speaking time for the main contribution. Allow time for
figures, audience reaction, and transitions; a dense derivation usually needs
more time than a visual result.

## 4. Design The Argument Before Frames

Choose one narrative spine from `content_guidelines.md`. Draft a ghost deck in
which each content frame has:

```yaml
- id: result-scaling
  purpose: establish the empirical advantage
  action_title: The learned policy preserves fidelity as loss increases
  exhibit: one simplified result plot
  evidence: doi-or-citekey-and-result-location
  takeaway: the gain persists across the tested loss range
  seconds: 75
```

Read the action titles in order. They should state the argument without body
content. Put motivation before formalism, define notation before use, and avoid
more than three or four consecutive theory-heavy frames without an example,
result, or visual reset.

For a new deck or major restructuring, show the outline to the user before
drafting. This approval gate is unnecessary for routine corrections or when the
user has already supplied an exact slide plan.

## 5. Draft In Verifiable Batches

Draft related frames in small batches. For each batch:

1. Use the frame patterns in `slide_patterns.md`.
2. Keep visible bullets incremental unless the user requests a handout or the
   list is a compact legend.
3. Define symbols close to first use and keep derivations in notes or backup.
4. Use one main exhibit and one clear takeaway per frame.
5. Add sparse footer provenance at the first supporting use.
6. Build an isolated preview for the edited section or labeled frame.
7. Inspect the rendered pages, including every overlay state.

Do not use font shrinking as the primary density fix. Split, simplify, or move
supporting detail to notes.

## 6. Quality Loop

Before delivery:

```powershell
conda run -n SigCOM python academic-beamer/scripts/deck_audit.py example.tex
powershell -ExecutionPolicy Bypass -File academic-beamer/scripts/build.ps1
conda run -n SigCOM python academic-beamer/scripts/deck_audit.py example.tex `
  --log example.log --pdf example.pdf --render-dir deck-audit/rendered
```

Then perform the relevant review modes in `review_workflow.md`. Automated
findings are diagnostics, not a substitute for checking scientific logic,
figure semantics, pacing, and the compiled pages. Resolve errors; assess
warnings in context and document intentional exceptions.
