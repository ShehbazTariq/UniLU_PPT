# Upstream Workflow Adaptation Record

Reviewed upstream: [Noi1r/beamer-skill](https://github.com/Noi1r/beamer-skill)
at commit `61a6c5508d737acc6599416cb0cebf6d0b8ff4f4` on 2026-07-13.

This repository preserves the UniLU/SnT template as the authority. The review
adapted process ideas, not upstream theme or compiler policy.

| Upstream idea | UniLU adaptation |
| --- | --- |
| staged creation lifecycle | talk contract, evidence inventory, outline, batched draft, quality loop |
| timing-based slide budget | advisory source-frame ranges; overlay pages are excluded |
| named review actions | proofread, structural, visual, pedagogy, comprehensive, and devil's-advocate modes |
| deterministic validation | `deck_audit.py` with error/warning separation and JSON reports |
| compiled-PDF review | optional page rendering and contact sheet after the two-pass local build |
| paper figure extraction | bracket-safe Poppler helper with source-page provenance |

The following upstream rules were deliberately not adopted:

- XeLaTeX-only compilation: this template uses its verified two-pass
  `pdflatex` build.
- prohibition of overlays: UniLU content slides use progressive Beamer
  overlays by default.
- generic theme, palette, and geometry rules: institutional title, section,
  content, footer, and closing layouts remain authoritative.
- mandatory end bibliographies: UniLU uses sparse footer citations and adds an
  end reference frame only when requested or required.
