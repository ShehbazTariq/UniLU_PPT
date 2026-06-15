# Academic Beamer Content Guidelines

These rules govern the argument, density, source use, equations, and QA for academic Beamer slides built from the UniLU/SnT template.

## 1. Operating Principle

Preserve the template; improve the argument.

Priority order:

1. User's explicit request
2. Existing Beamer template structure
3. `SKILL.md`
4. This file
5. `slide_patterns.md`
6. General academic presentation conventions

Do not redesign the institutional visual identity unless explicitly asked.

## 2. Source Roles

Use folders like this:

```text
notes/       reusable source material
content/     selected outline and slide content for the current talk
figures/     generated or supplied figures
Assets/      institutional logos and template assets
Sections/    Beamer source files included by example.tex
```

`notes/` is a library. Do not copy it wholesale into slides.

`content/` is talk-specific. When useful, create:

```text
content/deck_outline.yaml
content/slide_sources.yaml
```

## 3. Argument Structure

Lead with the research question, claim, or design problem by slide 2 or 3.

Choose one narrative spine:

- Situation / Complication / Resolution
- Funnel + Answer
- Answer First

Do not present the whole paper. Select the argument that fits the talk length and move secondary derivations, robustness checks, or extra results to backup frames.

## 4. Action Titles

Every content frame should have an action title: a sentence that states the takeaway.

Use:

- `Entanglement routing becomes fragile when edge loss accumulates with path length.`
- `Postselection suppresses the dominant single-error events in the crazy graph.`
- `The proposed architecture trades acceptance rate for higher output fidelity.`

Avoid:

- `Background`
- `System Model`
- `Results`
- `Simulation Setup`

Run the ghost deck test: read only the frame titles in sequence. They should tell the story.

## 5. Slide Density

Default visible density:

- one action title
- 2 to 4 short bullets
- one main figure, diagram, table, or equation block
- one compact citation line when needed

For mathematical frames:

- one main equation block
- 1 to 3 interpretation bullets
- minimal symbol definitions
- derivation details in notes or backup frames

Avoid paragraphs on visible slides.

## 6. Equations

Use native LaTeX math.

Rules:

- Keep notation consistent with the paper or previous frames.
- Define symbols near first use.
- Do not overload one frame with multiple derivation steps.
- Put long derivations in `\note{...}` or a backup frame.
- Prefer aligned equations for multi-line derivations.

## 7. Figures And Tables

Use figures only when they support the action title.

Rules:

- Keep figure paths relative to the template root.
- Use vector formats for plots when possible: `.pdf` or `.pgf`.
- Use high-resolution `.png` for raster diagrams and screenshots.
- Do not stretch figures. Preserve aspect ratio.
- Add concise captions only when the source or interpretation is not obvious.

## 8. Citations

Use citations that are present in the source material or bibliography.

Rules:

- Do not invent references.
- Keep visible citations compact.
- Put detailed reference context in notes or references frames.
- If no bibliography exists, use short textual source markers until the user supplies one.

## 9. Speaker Notes

Use `\note{...}` or the existing `\notes{item; item}` helper for:

- derivation details
- assumptions
- source context
- anticipated questions
- oral transition text

Visible slides should remain concise.

## 10. QA Checklist

Before finalizing:

- Compile from the template root.
- Open the generated PDF.
- Check title slide logos and aspect ratio.
- Check every edited frame for overflow.
- Confirm overlays reveal content in the intended order.
- Confirm figure paths resolve.
- Confirm citations are either resolved or clearly reported as pending.
