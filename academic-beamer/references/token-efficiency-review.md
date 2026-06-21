# Token-Efficiency Review

Use this when explicitly reviewing or improving the skill.

## Loading Rules
- Read `SKILL.md` first.
- For content strategy, read `content_guidelines.md`.
- For frame syntax, read `slide_patterns.md`.
- For build failures, inspect `academic-beamer/scripts/build.ps1` and the shortest relevant TeX log excerpt.
- Do not scan generated build artifacts (`example.pdf`, `.aux`, `.log`, `.nav`, `.snm`, `.toc`) unless debugging a compile failure.
- Do not inspect image assets unless the task concerns logos, QR codes, missing images, or visual placement.

## Review Checklist
- Keep `SKILL.md` as the core behavior contract.
- Put new long lessons in `references/FREQUENT_TASK_RECIPES.md`.
- Add `.ignore` patterns for generated artifacts that pollute `rg --files`.
- Capture repeated failures with `skill_memory.py learn`.
