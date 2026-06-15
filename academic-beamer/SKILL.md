---
name: academic-beamer
description: Use for creating, editing, compiling, and reviewing academic Beamer presentations in the UniLU/SnT LaTeX template from ShehbazTariq/UniLU_PPT - conference talks, seminars, defenses, lab meetings, paper-to-slide conversions, research updates. Applies when creating new local presentations from the GitHub template repo, working with example.tex, Sections/*.tex, beamerthemeblei.sty, the title/closing slides, content-slide chrome, LaTeX equations, citations, figures, logos/QR assets, and sectionized Beamer workflows.
---

# Academic Beamer Skill (UniLU/SnT template)

## Purpose

Create, revise, compile, or review academic Beamer decks built on the UniLU/SnT
template in this project. Preserve the institutional design; improve the argument.

## Template source workflow

- Treat `https://github.com/ShehbazTariq/UniLU_PPT` as the canonical template
  repository for new presentations.
- Before creating a new presentation, look for an existing local clone of
  `ShehbazTariq/UniLU_PPT`. If none exists, clone the repo; do not reclone over
  an existing copy.
- If the local template clone exists, update it from the remote with a
  conservative fast-forward pull when the working tree is clean. If local
  changes would be overwritten or the pull cannot fast-forward, stop and report
  the state instead of forcing it.
- Keep presentation-specific content, figures, build artifacts, PDFs, notes,
  and output folders local to the new deck/workspace. Do not commit or push
  generated presentation work back to the template repository unless the user
  explicitly asks.
- Copy or instantiate from the template for each new deck; use the template repo
  only as the source of the structure and theme.

## Template map

Template root = the parent of this skill folder.

```text
UniLU_PPT/
  example.tex              driver: \input order, \begin/\end{document}
  beamerthemeblei.sty      base theme (do not edit unless asked)
  Assets/                  logos + QR (see "Assets" below)
  Sections/
    00_preamble.tex        packages, macros, AND the content-slide chrome
    01_metadata.tex        all talk metadata + theme colours  ← edit per talk
    02_title_slide.tex     custom navy title slide (TikZ)
    03_motivation_and_model.tex .. 08_references.tex
                           generic EXAMPLE content slides; each opens a
                           \section{...} (+ optional \subsection{...}):
                           Introduction, Layouts, Equations, Figures, Summary,
                           References — these feed the auto section dividers
    09_closing.tex         closing/contact slide (mirror of title + QR card)
  academic-beamer/
    SKILL.md  content_guidelines.md  slide_patterns.md
    scripts/  build.ps1  clean_bg.py
```

## Decision table — change X → edit file Y

| Want to change… | Edit |
| --- | --- |
| Title, author, affiliation, date, event name, contact email/web, theme colours | `Sections/01_metadata.tex` |
| Content-slide chrome: section label, numbered corner arc, navy title size, block style, footer logos | `Sections/00_preamble.tex` (the "Content-slide layout" block) |
| Title slide design (panel, arcs, logos, layout) | `Sections/02_title_slide.tex` |
| Outline icon, section dividers, TOC/label styling | `Sections/00_preamble.tex` (`\outlinebutton`, `\AtBeginSection`, headline) |
| Closing/contact slide, QR card placement | `Sections/09_closing.tex` |
| Add/remove/reorder slides | create/edit a `Sections/*.tex`, then add one `\input{...}` to `example.tex` |
| Packages, repeated macros | `Sections/00_preamble.tex` |

## This template's specifics

- **Content slides are automatic.** Just write `\section{Label}` (sets the
  grey top-left label) and `\begin{frame}{Action title}`. The preamble supplies
  the navy title, the numbered top-right corner arc, styled `block`s, and the
  uni.lu (left) / SnT (right) footer logos. `\AtBeginSection{}` is intentionally
  emptied so `\section` adds **no** auto-outline frames.
- **Navigation (clean model).** Each content section opens with `\section{...}`
  and may use `\subsection{...}`.
  - `\AtBeginSection` auto-inserts a **per-section divider** ("Contents",
    `[plain,noframenumbering]`) before each section: current section
    highlighted with its subsections, other sections shaded with subsections
    hidden
    (`\tableofcontents[currentsection,sectionstyle=show/shaded,subsectionstyle=show/show/hide]`).
    Each divider sets `\hypertarget{sec\arabic{section}}{}` and lists every
    section (clickable), so any divider is a full navigation hub.
  - Content slides carry **no nav bar** — just a small clickable outline icon
    (`\outlinebutton`, bottom-centre) that jumps to the **current section's
    divider** (`\hyperlink{sec\arabic{section}}`), plus a quiet top-left section
    label for context. There is no separate master Contents slide.
  - These hyperlinks/TOCs make the two-pass build mandatory.
- **Metadata-driven.** `\title \author \institute \date`, plus `\eventname`
  `\eventfull` (title slide) and `\contactemail` `\contactweb` (closing slide).
- **Title & closing geometry** use a 16×9 TikZ grid (10 mm/unit at
  aspectratio=169). The closing slide is the title mirrored about x=8. The
  red/white accent arcs are tangent line → quarter arc → tail; the panel is
  drawn on top so tails tuck behind its rounded corner.
- **Assets:** title → `UniLu_White.png`, `SnT_White.png`; content footer →
  `UniLu_short.png`, `SnT_logo.png`; closing → `Uni_lu_White_last.png`,
  `QR_Linkedin_clean.png`. Logos/QR placed on navy must have a transparent
  background — clean black/white backgrounds with `scripts/clean_bg.py`
  (ImageMagick is not installed; this uses Pillow). Never edit a `*_clean.png`
  source; regenerate it.

## Build

Always **two passes** (the title and closing slides use `remember picture`,
so the first pass renders blank). Use the helper:

```powershell
pwsh academic-beamer/scripts/build.ps1
```

It closes Adobe (which locks `example.pdf`), runs `pdflatex` twice from the
root, and reports the PDF path plus fatal errors / missing files. Manual
equivalent:

```powershell
Get-Process Acrobat -EA SilentlyContinue | Stop-Process -Force -EA SilentlyContinue
Set-Location -LiteralPath '<path-to-UniLU_PPT>'   # -LiteralPath: the path has [brackets]
pdflatex -interaction=nonstopmode example.tex ; pdflatex -interaction=nonstopmode example.tex
```

Gotchas: the project path contains `[SigCom]` → always `-LiteralPath`. Run
`biber example` only when a real bibliography is cited.

## Editing rules

- Keep the sectionized architecture: no `\documentclass`, packages, or
  `\begin/\end{document}` inside `Sections/*` content files; those live in
  `00_preamble.tex` / `example.tex`.
- Keep asset/figure paths relative to the template root.
- Preserve `02_title_slide.tex`, `09_closing.tex`, and `beamerthemeblei.sty`
  unless a redesign is explicitly requested.
- The `03..08` files are disposable examples — replace their content freely for
  a real talk.

## When doing substantial content work

Sketch a slide outline first (number · purpose · action title · exhibit · key
evidence · takeaway). Then:

- **Argument, density, equations, figures, citations, speaker notes, QA** →
  read `content_guidelines.md` (authoritative; not repeated here).
- **Concrete Beamer frame patterns** (claim, two-column, equation, overlay,
  figure-result, summary, backup) → read `slide_patterns.md`.
- If a `notes/` folder exists, treat it as a source library, not a slide order:
  extract claims/results/citations, select what serves the talk, push
  derivations to `\note{...}` or backup frames. Never invent citations.
