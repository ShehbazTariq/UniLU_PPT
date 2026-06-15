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
\input{Sections/08_references}
\input{Sections/09_closing}

\end{document}
```

Add new content by creating or editing files under `Sections/`, then add one `\input{...}` line to the driver when needed. Each content section opens with `\section{...}` (and optional `\subsection{...}`), which automatically inserts a clean "Contents" divider before the section and feeds the bottom-centre outline button.

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
\begin{itemize}
  \widesep
  \item First evidence point.
  \item Second evidence point.
  \item Implication or bridge to the next frame.
\end{itemize}
\end{frame}
```

Keep bullets short. Use bold or `\alert{...}` sparingly.

## 4. Two-Column Frame

Use for comparisons, model-vs-baseline, or text plus figure.

```latex
\begin{frame}{Action title stating the comparison}
\begin{columns}[T,onlytextwidth]
\begin{column}{0.48\textwidth}
\begin{itemize}
  \item Left-side claim.
  \item Supporting detail.
\end{itemize}
\end{column}
\begin{column}{0.48\textwidth}
\centering
\includegraphics[width=\textwidth]{figures/example.pdf}
\end{column}
\end{columns}
\end{frame}
```

Do not overload both columns with dense text.

## 5. Equation Frame

Use for one key equation and interpretation.

```latex
\begin{frame}{Action title explaining what the equation shows}
\[
  F_{\mathrm{out}} = \frac{\langle \psi | \rho_{\mathrm{out}} | \psi \rangle}
                         {\mathrm{Tr}(\rho_{\mathrm{out}})}
\]
\begin{itemize}
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
\begin{itemize}
  \item<1-> First point.
  \item<2-> Second point.
  \item<3-> Takeaway.
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
\begin{itemize}
  \item What changes in the plot.
  \item Why it matters.
  \item Limitation or condition.
\end{itemize}
\end{column}
\end{columns}
\end{frame}
```

The title should state the result, not `Results`.

## 8. Summary Frame

Use for the final visible frame.

```latex
\begin{frame}{Summary}
\begin{enumerate}
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
