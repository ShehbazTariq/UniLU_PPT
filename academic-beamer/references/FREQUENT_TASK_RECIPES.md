# Frequent Task Recipes

Use this file before re-discovering a solved Academic Beamer workflow issue.

## Learned Recipes

Short, reproducible fixes captured after a solved skill-specific problem.

<!-- SKILL_LEARNED_RECIPE:bracket-safe-beamer-build-commands -->
### Bracket-safe Beamer build commands
- Problem: PowerShell commands can fail or resolve the wrong directory when the UniLU_PPT path contains bracketed segments such as [SigCom].
- Root cause: PowerShell treats square brackets as wildcard character classes unless the path is passed literally.
- Fix: Run Set-Location -LiteralPath '<UniLU_PPT path>' before build commands; prefer powershell -ExecutionPolicy Bypass -File academic-beamer/scripts/build.ps1 from the repo root.
- Use when: Any Beamer build or asset command touches OneDrive paths with square brackets.
- Command: `Set-Location -LiteralPath '<UniLU_PPT>'; powershell -ExecutionPolicy Bypass -File academic-beamer/scripts/build.ps1`
- File: `academic-beamer/SKILL.md`
- Tags: `powershell`, `windows-paths`, `beamer-build`
- Learned: 2026-06-21T18:40:17+02:00
<!-- /SKILL_LEARNED_RECIPE:bracket-safe-beamer-build-commands -->

<!-- SKILL_LEARNED_RECIPE:use-compactblock-for-narrow-beamer-callouts -->
### Use compactblock for narrow Beamer callouts
- Problem: Stacked or narrow-column callouts can overflow when written as plain Beamer blocks.
- Root cause: Plain blocks keep normal body size and spacing, which is too large for stacked callouts or columns <=0.45 textwidth.
- Fix: Define compactblock in Sections/00_preamble.tex and use it instead of plain block for stacked callouts or callouts in <=0.45\textwidth columns. Keep visible body text to one or two short lines and move exact values to notes.
- Use when: A slide has stacked callouts or a callout inside a narrow Beamer column.
- File: `Sections/00_preamble.tex`
- File: `academic-beamer/slide_patterns.md`
- Tags: `beamer-layout`, `compactblock`, `callouts`
- Learned: 2026-07-01T13:41:06+02:00
<!-- /SKILL_LEARNED_RECIPE:use-compactblock-for-narrow-beamer-callouts -->

<!-- SKILL_LEARNED_RECIPE:prevent-beamer-footer-citation-and-section-card-rule-overlaps -->
### Prevent Beamer footer citation and section-card rule overlaps
- Problem: Frame citations can overlap late bullet overlays, and section-card red rules can cross wrapped section titles.
- Root cause: Overlay content grows downward while framecite uses a fixed y position; section-card rule was placed at a fixed height inside the title block.
- Fix: Keep frame citations in a lower bottom safe band below body text and above footer logos; split crowded frames when needed. Place section-card rules below the full title block, reduce title font one notch, and widen title text width. Use explicit node distance and shortened arrows in flow diagrams.
- Use when: Editing UniLU/SnT Beamer decks with footer citations, section divider cards, or horizontal flow diagrams.
- File: `Sections/00_preamble.tex`
- Tags: `beamer`, `layout`, `citations`
- Learned: 2026-07-01T18:49:31+02:00
<!-- /SKILL_LEARNED_RECIPE:prevent-beamer-footer-citation-and-section-card-rule-overlaps -->

<!-- SKILL_LEARNED_RECIPE:use-sparse-footer-citations-in-beamer-decks -->
### Use sparse footer citations in Beamer decks
- Problem: Repeated footer citations on every slide make the deck noisy and can compete with content.
- Root cause: Citations were treated as a per-slide decoration instead of source provenance for the first supporting concept or figure.
- Fix: Use framecite only when a source first supports a concept, theorem, model, or reproduced figure. Do not repeat the same citation on follow-up explanation slides; keep details in speaker notes or a source/provenance slide.
- Use when: Reviewing or editing academic Beamer decks with many repeated literature footers.
- File: `academic-beamer/SKILL.md`
- File: `Sections/00_preamble.tex`
- Tags: `beamer`, `citations`, `provenance`
- Learned: 2026-07-01T18:49:31+02:00
<!-- /SKILL_LEARNED_RECIPE:use-sparse-footer-citations-in-beamer-decks -->

<!-- SKILL_LEARNED_RECIPE:keep-beamer-action-titles-compact -->
### Keep Beamer action titles compact
- Problem: Large frame titles can crowd the body area, especially for sentence-style action titles.
- Root cause: `\huge` frame titles leave too little vertical space in the UniLU/SnT content-slide geometry.
- Fix: Use `\large` as the default `frametitle` font size in `Sections/00_preamble.tex`; if a title still crowds the content, shorten the action title or split the frame.
- Use when: Updating UniLU/SnT Beamer templates or fixing slides where headings force equations, bullets, or citations into the footer safe band.
- Tags: `beamer`, `layout`, `frametitle`
<!-- /SKILL_LEARNED_RECIPE:keep-beamer-action-titles-compact -->
