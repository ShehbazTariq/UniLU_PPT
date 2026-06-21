# Self-Learning Recipes

Use this only when the user asks to improve the skill or when a non-obvious Beamer workflow failure was solved.

## Commands
```powershell
python academic-beamer\scripts\skill_memory.py search "<task or error>"
python academic-beamer\scripts\skill_memory.py learn --title "..." --problem "..." --root-cause "..." --fix "..."
python academic-beamer\scripts\skill_memory.py review
```

## Policy
- Search recipes before re-debugging build, path, asset, overlay, citation, or layout issues.
- Add a recipe only after a deck builds or the visual/layout failure mode is verified.
- Keep recipes short: symptom, root cause, fix, exact command, relevant file, validation.
- Recipes never override the institutional design, sectionized architecture, or user-authored slide content.
- Move repeated long lessons here instead of growing `SKILL.md`.
