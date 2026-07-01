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

`content/` is talk-specific local scratch/planning output and is ignored by
Git in the template repo. Use it for intermediate outlines and source maps;
final visible slide content belongs in `Sections/`. When useful, create:

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
- 2 to 4 short bullets, revealed one at a time with Beamer overlays
- one main figure, diagram, table, or equation block
- compact callouts only when they fit without crowding
- one compact citation line when needed

Use `\begin{itemize}[<+->]` or `\begin{enumerate}[<+->]` by default. Every
visible bullet should appear one at a time unless the user explicitly asks for a
static handout-style slide or the list is only a compact legend.

For mathematical frames:

- one main equation block
- 1 to 3 interpretation bullets
- minimal symbol definitions
- derivation details in notes or backup frames

Avoid paragraphs on visible slides.

Avoid overloaded slides. Treat the footer logos as a hard lower boundary:
content, equations, plots, tables, and captions must stay above the logo area.
If the frame only fits by shrinking text aggressively or crossing the footer,
split it or move details to notes/backup.

For callouts, use `compactblock` instead of a plain `block` when the callout is
stacked with another callout or sits in a `<=0.45\textwidth` column. Keep the
visible body to one or two short lines; put exact values, caveats, and longer
supporting detail in notes or backup.

Highlight very little. Use color for at most one or two important terms,
numbers, or decisions per slide. Do not highlight whole bullets, paragraphs, or
large table regions.

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

### TikZ diagrams and flow charts — no overlapping arrows or labels

When you draw node-and-arrow diagrams (pipelines, graphs, lifecycles), the most
common defect is an arrowhead, line, or edge label colliding with text. Avoid it:

- Connect arrows between node *borders* (`\draw (a) -- (b);`), never to a
  coordinate that lands inside or on top of another node. Let TikZ clip the line
  at each node's border so arrowheads sit on the border, not on a label.
- Never let a line or arrowhead cross a label. If a label must sit *on* an edge
  (e.g. a key/badge on a connector), make it a `node` with `fill=white` (or the
  slide background colour) so it masks the line behind it, and keep the
  arrowheads on the far node borders, well clear of that label.
- Do not stack a label and an arrowhead at the same point. Place edge labels off
  the line with `auto`, `left=`/`right=`, or `sloped`, plus a small offset.
- Give nodes real separation (`node distance`, or explicit coordinates) so
  arrows have a clear run and labels have room. If a small badge sits between two
  boxes, leave a vertical gap taller than the badge.
- Route feedback / back edges around the *outside* of the layout (bend the curve
  away from the cluster, e.g. `to[bend left=45] (a.west)`) instead of through the
  boxes, and put the label on the outer side of the curve.
- After rendering, open the page and check every arrow, arrowhead, and label for
  overlap before finalizing — this is part of the QA checklist below.

## 8. Citations

Use citations that are present in the source material or bibliography.

Rules:

- Do not invent references.
- Cite claims with `\framecite{...}`. This prints a small footer citation above
  the logos. It does not print a visible marker in the slide body.
- The visible citation must include author/year text and the paper title. Link
  the citation text to the DOI or arXiv DOI URL when one is available.
- Do not show numbered reference labels in the footer.
- Use `\framecite[2]{...}` for a second source, `\framecite[3]{...}` for a
  third source, and so on. Each source appears on its own footer line.
- Keep footer citations above the footer logos and outside the main content
  area. If content approaches the citations, move the content up, split the
  slide, or lower the citation rows in the preamble.
- Prefer footer citations over a final references section for ordinary meeting
  decks. Add an end references frame only when the user asks for a bibliography
  or the venue requires one.
- Keep visible citations compact but complete enough for a talk: author/year,
  paper title, venue or preprint server, and a DOI-linked target.
- Put detailed reference context in notes or backup frames.
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
- Check every TikZ diagram for overlapping arrows, arrowheads, or labels (see "TikZ diagrams and flow charts" above).
- Confirm citations are either resolved or clearly reported as pending.
- Click section headings and subsection bullets in the PDF; confirm they jump to the correct section card or subsection start page.
