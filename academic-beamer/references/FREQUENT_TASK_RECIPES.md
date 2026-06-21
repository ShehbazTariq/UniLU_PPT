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
