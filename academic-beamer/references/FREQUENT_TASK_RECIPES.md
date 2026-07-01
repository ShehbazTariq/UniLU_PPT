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
