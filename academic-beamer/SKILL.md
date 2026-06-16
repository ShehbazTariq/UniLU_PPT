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

Template root = the parent of this skill folder when using the repo-local copy
at `UniLU_PPT/academic-beamer/`. When this skill is installed under
`.codex/skills/academic-beamer`, do not treat the installed skill's parent as
the template root; locate the active `UniLU_PPT` repo from the user's path,
current workspace, or an existing clone.

```text
UniLU_PPT/
  example.tex              driver: \input order, \begin/\end{document}
  beamerthemeblei.sty      base theme (do not edit unless asked)
  Assets/                  logos + QR (see "Assets" below)
  Sections/
    00_preamble.tex        packages, macros, AND the content-slide chrome
    01_metadata.tex        all talk metadata + theme colours  ← edit per talk
    02_title_slide.tex     custom navy title slide (TikZ)
    03_motivation_and_model.tex .. 07_summary.tex
                           generic EXAMPLE content slides; each opens a
                           \section{...} (+ optional \subsection{...}):
                           Introduction, Layouts, Equations, Figures, Summary
    08_references.tex      optional bibliography/reference slide; not included
                           by default for meeting decks
    09_closing.tex         closing/contact slide (mirror of title + QR card)
  academic-beamer/
    SKILL.md  content_guidelines.md  slide_patterns.md
    scripts/  build.ps1  clean_bg.py
```

## Decision table — change X → edit file Y

| Want to change… | Edit |
| --- | --- |
| Title, author, affiliation, date, event name, contact email/web, theme colours | `Sections/01_metadata.tex` |
| Content-slide chrome: section label, inset frame counter, navy title size, block style, footer logos | `Sections/00_preamble.tex` (the "Content-slide layout" block) |
| Title slide design (panel, arcs, logos, layout) | `Sections/02_title_slide.tex` |
| Section dividers, TOC/label styling, footer/logo safe area | `Sections/00_preamble.tex` (`\AtBeginSection`, headline, footline) |
| Closing/contact slide, QR card placement | `Sections/09_closing.tex` |
| Add/remove/reorder slides | create/edit a `Sections/*.tex`, then add one `\input{...}` to `example.tex` |
| Packages, repeated macros | `Sections/00_preamble.tex` |

## This template's specifics

- **Current slide-writing requirements override older examples below.**
  Use incremental overlays for visible bullet lists; keep section labels small;
  highlight only one or two important terms/numbers per slide; keep all content
  above the footer logos; use footer citations instead of end-only references;
  and use modern section cards instead of agenda/Contents slides unless the
  user asks for an agenda.
- **Bullet overlays are mandatory by default.** For visible bullet lists, use
  `\begin{itemize}[<+->]` / `\begin{enumerate}[<+->]` or explicit `\item<n->`
  so points appear one at a time. Keep static bullets only when the user asks
  for a handout-style slide or when the list is purely a compact legend.
- **Highlight sparingly.** Use color only for one or two truly important words,
  numbers, or terms on a slide. Prefer `\textcolor{accentred}{...}` or
  `\textcolor{accentblue}{...}` when those metadata colors exist. Do not color
  whole paragraphs, long bullets, or many table cells.
- **Keep the footer logo area clear.** Treat the uni.lu and SnT footer logos as
  a hard bottom boundary. Content, plots, tables, and captions must remain above
  the footline; split crowded slides instead of crossing into the logo area.
- **Cite sources on the slide.** Use `\framecite{...}` at the cited claim to
  print a small superscript marker and a matching `\scriptsize` footer citation
  above the logos. Use `\framecite[2]{...}` for a second source on the same
  slide. Prefer this over a final references section for meeting decks. Keep an
  end references frame only when the user asks for it or the venue requires a
  bibliography.
- **Section-break redesigns need approval when unsolicited.** If the user asks
  for a concrete section-card tweak, implement it and render the example. If
  you are proposing an unsolicited or ambiguous `\AtBeginSection` redesign,
  present a short plan first. Section labels/headings used for navigation or
  context should be small and unobtrusive.
- **Navigation model.** Do not include an agenda slide by default. Each
  `\section{...}` creates a no-frame-number section card with the old template
  background, a large circular section number, uppercase section title, and
  automatic bullet subheadings from that section's `\subsection{...}` entries.
  Use `\agendaslide` only when the user explicitly asks for a full agenda.

- **Content slides are automatic and top-aligned.** Just write
  `\section{Label}` (sets the grey top-left label) and
  `\begin{frame}{Action title}`. The preamble supplies the top-left content
  start, navy title, inset top-right frame counter, styled `block`s, and the
  uni.lu (left) / SnT (right) footer logos. Section-divider behavior is
  controlled by `\AtBeginSection` in `Sections/00_preamble.tex`.
- **Section navigation.** Content sections open with `\section{...}` and may use
  `\subsection{...}`. `\AtBeginSection` inserts a modern section card with
  `\hypertarget{sec\arabic{section}}{}`; subsection entries become bullet
  subheadings on the section card. The agenda and section targets make the
  two-pass build mandatory.
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

If `pwsh` is unavailable on Windows, use:

```powershell
powershell -ExecutionPolicy Bypass -File academic-beamer/scripts/build.ps1
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
- Never overload a frame. If content touches the footer, collides with logos, or
  needs very small text to fit, split it into multiple frames or move details to
  speaker notes/backup.
- The `03..07` files are disposable examples - replace their content freely for
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
