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

Use `\framecite{...}` at the citation site. It prints a small superscript marker
and a matching footer citation. Do not build a separate end references frame
unless the user or venue requires it.

## 8. Summary Frame

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

## 9. Backup Frame

Use backup frames for derivations, extra plots, robustness checks, and anticipated questions.

```latex
\appendix

\begin{frame}{Backup: derivation detail}
...
\end{frame}
```

Keep backup frames organized and title them clearly.

## 10. Compile Pattern

Build with the helper (closes Adobe, runs two passes, reports):

```powershell
pwsh academic-beamer/scripts/build.ps1
```

Manual equivalent — **two passes** are mandatory (title/closing use TikZ
`remember picture`; nav/hyperlinks also need a second pass):

```powershell
Set-Location -LiteralPath '<path-to-UniLU_PPT>'   # -LiteralPath: path has [brackets]
pdflatex -interaction=nonstopmode example.tex ; pdflatex -interaction=nonstopmode example.tex
```

Open `example.pdf` after compiling and visually check the edited frames.
