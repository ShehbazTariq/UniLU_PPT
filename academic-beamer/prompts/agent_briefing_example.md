# Agent Briefing — UniLU/SnT Beamer Template

Paste this block at the top of any prompt when asking an AI to write or edit slides in this deck.

---

You are writing slides for a Beamer deck built on the **UniLU/SnT institutional template**.

**Read first — mandatory:**
`academic-beamer/SKILL.md` — contains the complete template map, decision table, build instructions, and editing rules. Also read `academic-beamer/content_guidelines.md` (argument and density rules) and `academic-beamer/slide_patterns.md` (copy-paste LaTeX frame templates).

**Author block** (use verbatim on title/closing slide):
Dr. Shehbaz Tariq · Postdoctoral Researcher, SIGCOM · SnT, University of Luxembourg · shehbaz.tariq@uni.lu

**Per-talk editing rules:**
- Metadata (title, author, date, event, contact): edit **only** `Sections/01_metadata.tex`
- Content slides: edit/replace `Sections/03_*.tex` through `Sections/08_*.tex`
- Never touch `Sections/02_title_slide.tex`, `Sections/09_closing.tex`, or `beamerthemeblei.sty` unless a redesign is explicitly requested
- Keep the sectionized architecture: no `\documentclass`, no `\begin/\end{document}` inside `Sections/*` files
- Add new content by creating a new `Sections/NN_name.tex` and adding one `\input{Sections/NN_name}` line to `example.tex`

**Build:**
```powershell
pwsh academic-beamer/scripts/build.ps1
```
Two passes are mandatory (TikZ `remember picture`). The script kills Adobe/SumatraPDF before compiling so the PDF lock does not block the build. Always use `-LiteralPath` for any PowerShell path operations — the project path contains `[SigCom]` (square brackets are wildcard characters in PowerShell).

**Action titles:** every `\begin{frame}{...}` title must be a complete sentence stating the takeaway — not a topic label like "Results" or "Method".

**Bullets:** visible bullet lists must reveal one point at a time. Use `\begin{itemize}[<+->]` / `\begin{enumerate}[<+->]` or explicit `\item<n->` overlays. Keep static bullets only for compact legends or if the user asks for handout-style slides.

**Highlighting:** highlight very little: one or two important terms, numbers, or decisions per slide. Do not color whole paragraphs or dense table regions.

**Equations:** use native LaTeX math (`\[...\]`, `align`, `align*`). Derivation details go in `\note{...}` or backup frames after `\appendix`. Use `\widesep` inside `\begin{itemize}[<+->]` to increase vertical spacing between bullets.

**Figures:** paths relative to the template root (`UniLU_PPT/`). Prefer `.pdf`/`.pgf` for plots; high-res `.png` for diagrams. Missing figures render as a labelled placeholder box — compile always succeeds.

**Footer boundary:** the uni.lu/SnT logos define a hard bottom boundary. No content, plots, tables, captions, or equations may cross into the footer/logo area. Split overloaded slides instead.

**Citations:** cite inline with `\framecite{...}` so the claim gets a small superscript marker and the matching `\scriptsize` source appears in the footer. Use `\framecite[2]{...}` for a second source on the same slide. Do not create an end references frame unless the user or venue requires a bibliography.

**Section breaks:** do not include an agenda slide unless asked. Each `\section{...}` creates a modern section card on the old template background with a circular section number, uppercase title, and bullet subheadings from `\subsection{...}` entries; do not add repeated full Contents dividers.

**Frame layout:** normal content frames are top-aligned by default. Start content under the frame title with the template margins; only use `\begin{frame}[c]{...}` for an intentionally centered slide.

**Speaker notes:** use `\note{...}` for single-paragraph notes or the `\notes{point one; point two}` helper (defined in `00_preamble.tex`) for bullet-list notes.

**Decision table — change X → edit file Y:**

| Want to change | Edit |
|---|---|
| Title, author, affiliation, date, event, contact email/web, theme colours | `Sections/01_metadata.tex` |
| Content-slide chrome: section label, inset frame counter, navy title, block style, footer logos | `Sections/00_preamble.tex` |
| Title slide design (panel, arcs, logos) | `Sections/02_title_slide.tex` |
| Closing/contact slide or QR card | `Sections/09_closing.tex` |
| Packages or repeated macros | `Sections/00_preamble.tex` |
| Add/remove/reorder slides | Create/edit a `Sections/*.tex`, then add `\input{...}` to `example.tex` |
