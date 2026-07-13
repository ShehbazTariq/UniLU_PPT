# Beamer Slide Patterns

Use these patterns when adding or revising frames in the sectionized UniLU/SnT Beamer template.

## 1. Driver Pattern

Keep `example.tex` as the driver:

```latex
\input{Sections/00_preamble}
\input{Sections/01_metadata}

\begin{document}

\input{Sections/02_title_slide}
\input{Sections/03_motivation_and_model}
\input{Sections/04_prior_candidates}
\input{Sections/05_derivation_and_properties}
\input{Sections/06_application}
\input{Sections/07_summary}
\input{Sections/09_closing}

\end{document}
```

Add new content by creating or editing files under `Sections/`, then add one `\input{...}` line to the driver when needed. Each content section opens with `\section{...}` (and optional `\subsection{...}`), which creates a modern section card on the old template background: circular section number, uppercase title, and bullet subheadings from the section's subsections. Do not include an agenda slide unless the user explicitly asks for one.

## 2. Title Slide Pattern

The title slide lives in `Sections/02_title_slide.tex`.

Preserve:

- `\begin{frame}[plain,t]`
- the `tikzpicture` overlay
- `Assets/UniLu_White.png`
- `Assets/SnT_White.png`
- the navy background, periwinkle panel, and red accent geometry

Change title-slide text in either:

- `Sections/01_metadata.tex` for metadata values, or
- `Sections/02_title_slide.tex` for the manually drawn text nodes.

## 3. Standard Claim Frame

Use for most argument steps.

```latex
\begin{frame}{Action title stating the takeaway}
\begin{itemize}[<+->]
  \widesep
  \item First evidence point\framecite{Author et al., short venue/year}.
  \item Second evidence point.
  \item Implication or bridge to the next frame.
\end{itemize}
\end{frame}
```

Normal content frames are top-aligned by the template. Start with the evidence
or exhibit directly under the frame title; do not add manual vertical centering.

Keep bullets short. Use color sparingly: highlight only one or two important
terms or numbers on the slide.

## 4. Two-Column Frame

Use for comparisons, model-vs-baseline, or text plus figure.

```latex
\begin{frame}{Action title stating the comparison}
\begin{columns}[T,onlytextwidth]
\begin{column}{0.48\textwidth}
\begin{itemize}[<+->]
  \item Left-side claim.
  \item Supporting detail.
\end{itemize}
\end{column}
\begin{column}{0.48\textwidth}
\centering
\includegraphics[width=\textwidth]{figures/example.pdf}\framecite{Source: dataset/paper/software note}
\end{column}
\end{columns}
\end{frame}
```

Do not overload both columns with dense text. Keep all content above the footer
logos; split the slide if a table, plot, or text block enters the logo area.
For stacked callouts or callouts in columns `<=0.45\textwidth`, use
`compactblock` instead of a plain `block`:

```latex
\begin{column}{0.42\textwidth}
\begin{compactblock}{Main result}
One or two short lines of visible takeaway text.
\end{compactblock}
\vspace{0.45em}
\begin{compactblock}{Next step}
Another short callout; move exact values to notes.
\end{compactblock}
\end{column}
```

## 5. Equation Frame

Use for one key equation and interpretation.

```latex
\begin{frame}{Action title explaining what the equation shows}
\[
  F_{\mathrm{out}} = \frac{\langle \psi | \rho_{\mathrm{out}} | \psi \rangle}
                         {\mathrm{Tr}(\rho_{\mathrm{out}})}
\]\framecite{Notation follows Author et al., year}
\begin{itemize}[<+->]
  \item Define only the symbols needed on this frame.
  \item State the interpretation, not every algebra step.
\end{itemize}
\end{frame}
```

Move derivations to notes or backup frames.

## 6. Overlay Frame

Use overlays when revealing logic step by step.

```latex
\begin{frame}{Action title}
\begin{itemize}[<+->]
  \item First point.
  \item Second point.
  \item Takeaway.
\end{itemize}
\end{frame}
```

Avoid complex nested `overprint` unless necessary. If using `overprint`, ensure slides do not overlap and compile-check the frame.

## 7. Figure Result Frame

Use for simulation plots and experimental results.

```latex
\begin{frame}{Action title interpreting the result}
\begin{columns}[T,onlytextwidth]
\begin{column}{0.58\textwidth}
\centering
\includegraphics[width=\textwidth]{figures/result.pdf}
\end{column}
\begin{column}{0.38\textwidth}
\begin{itemize}[<+->]
  \item What changes in the plot.
  \item Why it matters.
  \item Limitation or condition.
\end{itemize}
\end{column}
\end{columns}
\end{frame}
```

The title should state the result, not `Results`.

Use `\framecite{...}` to print a footer citation. The visible citation should
include author/year text and the paper title, linked to the DOI or arXiv DOI URL
when available. Use `\framecite[2]{...}` and `\framecite[3]{...}` for additional
sources on separate footer lines. Do not print numbered reference labels, and
do not build a separate end references frame unless the user or venue requires
it.

## 8. Stable TikZ Overlay Frame

Use one fixed coordinate system and reveal state or emphasis without rebuilding the layout.

```latex
\begin{frame}{Measurement closes the hybrid optimization loop}
\centering
\begin{tikzpicture}[
  node distance=12mm,
  stage/.style={draw, rounded corners=2pt, minimum width=27mm,
    minimum height=9mm, text width=24mm, align=center},
  flow/.style={-{Latex[length=2.2mm]}, semithick}
]
  \node[stage] (encode) {Input encoding};
  \node[stage, right=of encode] (quantum) {Quantum process};
  \node[stage, right=of quantum] (measure) {Measurement};
  \node[stage, below=of quantum] (update) {Classical update};

  \draw[flow] (encode) -- (quantum);
  \draw[flow] (quantum) -- (measure);
  \draw[flow] (measure) to[bend left=20]
    node[right, pos=0.55, fill=white] {observables} (update);
  \draw[flow] (update) to[bend left=20]
    node[left, pos=0.55, fill=white] {parameters} (quantum);

  \onslide<2->{\node[overlay, draw=accentred, very thick, fit=(measure), inner sep=2pt] {};}
  \onslide<3->{\node[overlay, draw=accentblue, very thick, fit=(update), inner sep=2pt] {};}
\end{tikzpicture}
\framecite{Author/year, paper title, DOI-linked source}
\end{frame}
```

Load `positioning`, `arrows.meta`, and `fit` in the preamble. Read
`references/tikz_diagrams.md`, preview the frame, run `tikz_slide_qa.py`, and inspect each overlay.

## 9. Summary Frame

Use for the final visible frame.

```latex
\begin{frame}{Summary}
\begin{enumerate}[<+->]
  \item Main contribution.
  \item Main evidence.
  \item Practical implication or next step.
\end{enumerate}
\end{frame}
```

Do not introduce new evidence on the summary frame.

## 10. Backup Frame

Use backup frames for derivations, extra plots, robustness checks, and anticipated questions.

```latex
\appendix

\begin{frame}{Backup: derivation detail}
...
\end{frame}
```

Keep backup frames organized and title them clearly.

## 11. Compile Pattern

Build with the helper (closes Adobe, runs two passes, reports):

```powershell
pwsh academic-beamer/scripts/build.ps1
```

Windows fallback when `pwsh` is not available:

```powershell
powershell -ExecutionPolicy Bypass -File academic-beamer/scripts/build.ps1
```

Manual equivalent — **two passes** are mandatory (title/closing use TikZ
`remember picture`; nav/hyperlinks also need a second pass):

```powershell
Set-Location -LiteralPath '<path-to-UniLU_PPT>'   # -LiteralPath: path has [brackets]
pdflatex -interaction=nonstopmode example.tex ; pdflatex -interaction=nonstopmode example.tex
```

Open `example.pdf` after compiling. Visually check edited frames and click
section/subsection navigation links after any section-card or TOC change.
