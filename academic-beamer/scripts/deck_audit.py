#!/usr/bin/env python3
"""Audit a UniLU/SnT Beamer deck without replacing human visual review."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re
import sys
from typing import Any, Iterable


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    path: str
    line: int | None
    current: str
    recommendation: str


@dataclass(frozen=True)
class Frame:
    path: Path
    line: int
    title: str
    options: str
    section: str
    body: str
    raw: str


GENERIC_TITLES = {
    "agenda",
    "background",
    "conclusion",
    "conclusions",
    "discussion",
    "equations",
    "figures",
    "introduction",
    "method",
    "methods",
    "motivation",
    "outline",
    "results",
    "simulation setup",
    "summary",
    "system model",
}
TIMING_BUDGETS = {
    5: (5, 7),
    10: (8, 12),
    15: (10, 15),
    20: (13, 18),
    45: (22, 30),
    90: (45, 60),
}
SEVERITY_ORDER = {"error": 0, "warning": 1, "info": 2}
FRAME_DEFINITION_FILES = {"00_preamble.tex", "01_metadata.tex"}

INPUT_RE = re.compile(r"\\(?:input|include)\s*\{([^{}]+)\}")
FRAME_START_RE = re.compile(r"\\begin\s*\{frame\}(?:\s*\[([^\]]*)\])?")
FRAME_END_RE = re.compile(r"\\end\s*\{frame\}")
SECTION_RE = re.compile(r"\\section\*?\s*\{([^{}]*)\}")
FRAMETITLE_RE = re.compile(r"\\frametitle\s*\{([^{}]*)\}")
LIST_RE = re.compile(
    r"\\begin\s*\{(?:itemize|enumerate)\}(?:\s*\[([^\]]*)\])?(.*?)"
    r"\\end\s*\{(?:itemize|enumerate)\}",
    re.DOTALL,
)
ITEM_RE = re.compile(r"\\item(?:\s*<[^>]+>)?")
GRAPHICS_RE = re.compile(r"\\includegraphics(?:\s*\[[^\]]*\])?\s*\{([^{}]+)\}")
FRAMECITE_RE = re.compile(r"\\framecite(?:\s*\[[^\]]*\])?\s*\{([^{}]+)\}")
PLACEHOLDER_RE = re.compile(r"\b(?:TODO|FIXME|TBD|XXX)\b|\\missingfigure\s*\{", re.IGNORECASE)
EQUATION_RE = re.compile(
    r"\\\[|\\begin\s*\{(?:equation\*?|align\*?|gather\*?|multline\*?)\}"
)
BOX_RE = re.compile(r"\\begin\s*\{(?:block|compactblock|alertblock|exampleblock)\}")
HIGHLIGHT_RE = re.compile(r"\\(?:alert|colorboxed|textcolor)\b")
COLUMN_RE = re.compile(
    r"\\begin\s*\{column\}\s*\{\s*([0-9.]+)\\textwidth\s*\}(.*?)"
    r"\\end\s*\{column\}",
    re.DOTALL,
)


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _strip_comments(text: str) -> str:
    lines = []
    for line in text.splitlines(keepends=True):
        match = re.search(r"(?<!\\)%", line)
        if match:
            ending = "\n" if line.endswith("\n") else ""
            comment_length = len(line) - match.start() - len(ending)
            line = line[: match.start()] + (" " * comment_length) + ending
        lines.append(line)
    return "".join(lines)


def _clean_tex(value: str) -> str:
    value = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^\]]*\])?", " ", value)
    value = value.replace("{", " ").replace("}", " ")
    return " ".join(value.split()).strip(" .:;!?").casefold()


def _read_braced(text: str, start: int) -> tuple[str, int] | None:
    if start >= len(text) or text[start] != "{":
        return None
    depth = 0
    for index in range(start, len(text)):
        if text[index] == "{" and (index == 0 or text[index - 1] != "\\"):
            depth += 1
        elif text[index] == "}" and (index == 0 or text[index - 1] != "\\"):
            depth -= 1
            if depth == 0:
                return text[start + 1 : index], index + 1
    return None


def _resolve_input(token: str, deck_root: Path, parent: Path) -> Path | None:
    if any(char in token for char in "\\#$"):
        return None
    candidate = Path(token)
    if not candidate.suffix:
        candidate = candidate.with_suffix(".tex")
    for base in (deck_root, parent):
        resolved = (base / candidate).resolve()
        if resolved.exists():
            return resolved
    return None


def discover_sources(entries: Iterable[Path]) -> list[Path]:
    entries = [path.resolve() for path in entries]
    if not entries:
        return []
    deck_root = entries[0].parent
    ordered: list[Path] = []
    seen: set[Path] = set()

    def visit(path: Path) -> None:
        path = path.resolve()
        if path in seen:
            return
        seen.add(path)
        ordered.append(path)
        text = _strip_comments(path.read_text(encoding="utf-8", errors="replace"))
        for match in INPUT_RE.finditer(text):
            child = _resolve_input(match.group(1).strip(), deck_root, path.parent)
            if child:
                visit(child)

    for entry in entries:
        visit(entry)
    return ordered


def parse_frames(path: Path) -> list[Frame]:
    raw_text = path.read_text(encoding="utf-8", errors="replace")
    text = _strip_comments(raw_text)
    sections = [(match.start(), match.group(1).strip()) for match in SECTION_RE.finditer(text)]
    frames: list[Frame] = []
    cursor = 0
    while True:
        start_match = FRAME_START_RE.search(text, cursor)
        if not start_match:
            break
        end_match = FRAME_END_RE.search(text, start_match.end())
        if not end_match:
            body = text[start_match.end() :]
            cursor = len(text)
        else:
            body = text[start_match.end() : end_match.start()]
            cursor = end_match.end()

        title = ""
        title_end = start_match.end()
        while title_end < len(text) and text[title_end].isspace():
            title_end += 1
        braced = _read_braced(text, title_end)
        if braced:
            title = braced[0].strip()
        else:
            title_match = FRAMETITLE_RE.search(body)
            if title_match:
                title = title_match.group(1).strip()

        section = ""
        for position, value in sections:
            if position < start_match.start():
                section = value
            else:
                break
        raw_end = end_match.end() if end_match else len(raw_text)
        frames.append(
            Frame(
                path=path,
                line=_line_number(text, start_match.start()),
                title=title,
                options=start_match.group(1) or "",
                section=section,
                body=body,
                raw=raw_text[start_match.start() : raw_end],
            )
        )
    return frames


def recommended_frame_range(duration_minutes: float) -> tuple[int, int, int]:
    benchmark = min(TIMING_BUDGETS, key=lambda item: abs(item - duration_minutes))
    low, high = TIMING_BUDGETS[benchmark]
    return low, high, benchmark


def _display_path(path: Path, deck_root: Path) -> str:
    try:
        return path.resolve().relative_to(deck_root.resolve()).as_posix()
    except ValueError:
        return str(path)


def _finding(
    severity: str,
    code: str,
    frame: Frame,
    deck_root: Path,
    current: str,
    recommendation: str,
    line_offset: int = 0,
) -> Finding:
    return Finding(
        severity,
        code,
        _display_path(frame.path, deck_root),
        frame.line + line_offset,
        current,
        recommendation,
    )


def _asset_exists(value: str, deck_root: Path) -> bool:
    path = Path(value.replace("\\", "/"))
    candidate = deck_root / path
    if candidate.suffix:
        return candidate.exists()
    return any(candidate.with_suffix(suffix).exists() for suffix in (".pdf", ".png", ".jpg", ".jpeg", ".eps"))


def audit_frames(frames: list[Frame], deck_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    cited_by_section: dict[str, set[str]] = {}
    theory_run = 0

    for frame in frames:
        clean_title = _clean_tex(frame.title)
        is_special = "noframenumbering" in frame.options or "plain" in frame.options
        if not frame.title and not is_special:
            findings.append(_finding(
                "warning", "missing_action_title", frame, deck_root,
                "The content frame has no title.",
                "Add a compact action title that states the frame's takeaway.",
            ))
        elif clean_title in GENERIC_TITLES and not is_special:
            findings.append(_finding(
                "warning", "generic_frame_title", frame, deck_root,
                f"The frame title is generic: {frame.title!r}.",
                "Replace it with a sentence-style claim that advances the ghost deck.",
            ))
        if not frame.section and not is_special:
            findings.append(_finding(
                "warning", "missing_section_context", frame, deck_root,
                "The content frame appears before any section declaration in its source file.",
                "Add or confirm the intended \\section metadata for navigation and context.",
            ))

        total_items = len(ITEM_RE.findall(frame.body))
        if total_items > 6:
            findings.append(_finding(
                "warning", "high_bullet_density", frame, deck_root,
                f"The frame contains {total_items} bullet items.",
                "Reduce to the essential visible points or split the frame.",
            ))

        allow_static = "audit: allow-static-list" in frame.raw.casefold()
        for list_match in LIST_RE.finditer(frame.body):
            list_body = list_match.group(2)
            item_count = len(ITEM_RE.findall(list_body))
            options = list_match.group(1) or ""
            has_overlay = bool(
                re.search(r"<[^>]+>", options)
                or re.search(r"\\item\s*<[^>]+>", list_body)
                or re.search(r"\\(?:pause|onslide|uncover|only|visible|alt)\b", list_body)
            )
            if item_count > 1 and not has_overlay and not allow_static:
                findings.append(_finding(
                    "warning", "static_visible_list", frame, deck_root,
                    f"A visible list with {item_count} items has no progressive overlay.",
                    "Use [<+->] or explicit item overlays, or mark an intentional compact legend with '% audit: allow-static-list'.",
                    _line_number(frame.body, list_match.start()) - 1,
                ))

        equation_count = len(EQUATION_RE.findall(frame.body))
        if equation_count > 2:
            findings.append(_finding(
                "warning", "high_equation_density", frame, deck_root,
                f"The frame contains approximately {equation_count} displayed equation environments.",
                "Keep one main derivation step visible and move supporting algebra to notes or backup.",
            ))
        box_count = len(BOX_RE.findall(frame.body))
        if box_count > 2:
            findings.append(_finding(
                "warning", "box_fatigue", frame, deck_root,
                f"The frame uses {box_count} colored block environments.",
                "Keep at most one or two purposeful callouts and restore visual hierarchy.",
            ))
        highlight_count = len(HIGHLIGHT_RE.findall(frame.body))
        if highlight_count > 2:
            findings.append(_finding(
                "warning", "excessive_highlighting", frame, deck_root,
                f"The frame contains {highlight_count} explicit highlight commands.",
                "Highlight only the one or two terms or values that carry the decision.",
            ))
        if r"\tiny" in frame.body:
            findings.append(_finding(
                "warning", "tiny_text", frame, deck_root,
                "The frame uses \\tiny text.",
                "Simplify or split the frame instead of shrinking visible content.",
            ))
        if PLACEHOLDER_RE.search(frame.body):
            findings.append(_finding(
                "warning", "unresolved_placeholder", frame, deck_root,
                "The frame contains an unresolved TODO, FIXME, TBD, XXX, or missing-figure placeholder.",
                "Resolve it or record explicitly why the placeholder remains before delivery.",
            ))

        columns = list(COLUMN_RE.finditer(frame.body))
        if columns:
            width_sum = sum(float(match.group(1)) for match in columns)
            if width_sum > 1.01:
                findings.append(_finding(
                    "error", "column_width_overflow", frame, deck_root,
                    f"Declared column widths sum to {width_sum:.2f}\\textwidth.",
                    "Reduce the widths and leave room for inter-column spacing.",
                ))
            for match in columns:
                width = float(match.group(1))
                body = match.group(2)
                if width <= 0.45 and re.search(r"\\begin\s*\{block\}", body):
                    findings.append(_finding(
                        "warning", "plain_block_in_narrow_column", frame, deck_root,
                        f"A plain block is used inside a {width:.2f}\\textwidth column.",
                        "Use compactblock and keep its visible body to one or two short lines.",
                    ))

        for graphic in GRAPHICS_RE.finditer(frame.body):
            value = graphic.group(1).strip()
            if re.match(r"^(?:[A-Za-z]:[\\/]|/home/|/Users/)", value):
                findings.append(_finding(
                    "warning", "absolute_asset_path", frame, deck_root,
                    f"The figure uses an absolute path: {value}",
                    "Use a project-relative figure path so the deck is portable.",
                ))
            elif (
                "audit: allow-missing-asset" not in frame.raw.casefold()
                and not any(char in value for char in "\\#$")
                and not _asset_exists(value, deck_root)
            ):
                findings.append(_finding(
                    "warning", "missing_asset", frame, deck_root,
                    f"The referenced figure was not found: {value}",
                    "Add the asset, correct the relative path, or replace the placeholder before delivery.",
                ))

        section_key = _clean_tex(frame.section) or "<none>"
        seen_citations = cited_by_section.setdefault(section_key, set())
        for citation in FRAMECITE_RE.findall(frame.body):
            normalized = " ".join(citation.split()).casefold()
            if re.search(r"(?:[A-Za-z]:[\\/]|/home/|/Users/|\.tex\b|notes?[\\/])", citation):
                findings.append(_finding(
                    "warning", "private_citation_metadata", frame, deck_root,
                    f"The footer citation may expose a local path or implementation label: {citation!r}",
                    "Use public author/year, title, venue, and DOI or arXiv provenance.",
                ))
            if normalized in seen_citations:
                findings.append(_finding(
                    "warning", "repeated_section_citation", frame, deck_root,
                    f"The same footer citation is repeated in section {frame.section!r}.",
                    "Keep it at the first source-defining use unless this frame needs independent provenance.",
                ))
            seen_citations.add(normalized)

        is_theory = bool(
            equation_count
            or re.search(r"\\begin\s*\{(?:theorem|proof|definition|lemma|proposition)\}", frame.body)
        )
        has_visual_reset = bool(
            GRAPHICS_RE.search(frame.body)
            or re.search(r"\\begin\s*\{(?:tikzpicture|table|tabular|axis)\}", frame.body)
        )
        theory_run = theory_run + 1 if is_theory and not has_visual_reset else 0
        if theory_run == 5:
            findings.append(_finding(
                "warning", "long_theory_run", frame, deck_root,
                "This is at least the fifth consecutive theory-heavy frame without a visual or worked-example reset.",
                "Insert an example, diagram, comparison, result, or audience checkpoint.",
            ))

    return findings


def inspect_log(path: Path, deck_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    display = _display_path(path, deck_root)
    for index, line in enumerate(text.splitlines(), start=1):
        if line.startswith("!"):
            findings.append(Finding(
                "error", "tex_error", display, index, line.strip(),
                "Resolve the TeX error and rebuild twice before review.",
            ))
        if re.search(r"(?:Citation|Reference).*undefined|There were undefined references", line, re.IGNORECASE):
            findings.append(Finding(
                "error", "undefined_reference", display, index, line.strip(),
                "Resolve the citation or cross-reference and run the required bibliography/build passes.",
            ))
        overfull = re.search(r"Overfull \\hbox \(([-0-9.]+)pt too wide\)", line)
        if overfull and float(overfull.group(1)) > 10.0:
            findings.append(Finding(
                "warning", "large_overfull_hbox", display, index, line.strip(),
                "Inspect the affected frame and reflow, shorten, or split the content.",
            ))
    return findings


def inspect_pdf(path: Path, render_dir: Path | None, deck_root: Path) -> tuple[dict[str, Any], list[Finding]]:
    findings: list[Finding] = []
    metrics: dict[str, Any] = {"path": _display_path(path, deck_root), "size_bytes": path.stat().st_size}
    if path.stat().st_size > 50 * 1024 * 1024:
        findings.append(Finding(
            "warning", "large_pdf", metrics["path"], None,
            f"The compiled PDF is {path.stat().st_size / 1024 / 1024:.1f} MB.",
            "Compress oversized raster assets before distribution.",
        ))
    try:
        import fitz
    except ImportError as exc:
        findings.append(Finding(
            "warning", "missing_pdf_dependency", metrics["path"], None,
            f"PyMuPDF is unavailable: {exc}",
            "Install PyMuPDF in the SigCOM environment to inspect and render compiled pages.",
        ))
        return metrics, findings

    doc = fitz.open(path)
    metrics["pages"] = doc.page_count
    rendered: list[tuple[int, Any]] = []
    image_module = None
    image_draw = None
    if render_dir:
        try:
            from PIL import Image, ImageDraw
            image_module, image_draw = Image, ImageDraw
            render_dir.mkdir(parents=True, exist_ok=True)
        except ImportError as exc:
            findings.append(Finding(
                "warning", "missing_render_dependency", metrics["path"], None,
                f"Pillow is unavailable: {exc}",
                "Install Pillow in the SigCOM environment to create the visual-review contact sheet.",
            ))

    for page_number, page in enumerate(doc, start=1):
        width, height = float(page.rect.width), float(page.rect.height)
        if height <= 0 or abs((width / height) - (16 / 9)) > 0.03:
            findings.append(Finding(
                "warning", "unexpected_aspect_ratio", metrics["path"], page_number,
                f"PDF page {page_number} has size {width:.1f} x {height:.1f} pt.",
                "Confirm the deck uses the intended 16:9 document class and no page-specific override.",
            ))
        if not page.get_text().strip() and not page.get_images(full=True) and not page.get_drawings():
            findings.append(Finding(
                "error", "blank_pdf_page", metrics["path"], page_number,
                f"PDF page {page_number} appears blank.",
                "Rebuild twice and inspect remember-picture or conditional frame content.",
            ))
        if render_dir and image_module:
            pixmap = page.get_pixmap(matrix=fitz.Matrix(160 / 72, 160 / 72), alpha=False)
            png = render_dir / f"page-{page_number:03d}.png"
            pixmap.save(png)
            image = image_module.open(png).convert("RGB")
            thumb = image.copy()
            thumb.thumbnail((480, 270))
            rendered.append((page_number, thumb))

    if render_dir and rendered and image_module and image_draw:
        columns = 3
        cell_width, cell_height = 500, 300
        rows = (len(rendered) + columns - 1) // columns
        sheet = image_module.new("RGB", (columns * cell_width, rows * cell_height), "white")
        draw = image_draw.Draw(sheet)
        for index, (page_number, thumb) in enumerate(rendered):
            x = (index % columns) * cell_width
            y = (index // columns) * cell_height
            draw.text((x + 10, y + 5), f"Page {page_number}", fill="black")
            sheet.paste(thumb, (x + 10, y + 25))
        contact_sheet = render_dir / "contact-sheet.png"
        sheet.save(contact_sheet)
        metrics["render_dir"] = str(render_dir)
        metrics["contact_sheet"] = str(contact_sheet)
    doc.close()
    return metrics, findings


def build_report(
    entries: list[Path],
    duration_minutes: float | None = None,
    log: Path | None = None,
    pdf: Path | None = None,
    render_dir: Path | None = None,
) -> dict[str, Any]:
    deck_root = entries[0].resolve().parent
    sources = discover_sources(entries)
    frame_sources = [source for source in sources if source.name not in FRAME_DEFINITION_FILES]
    frames = [frame for source in frame_sources for frame in parse_frames(source)]
    content_frames = [
        frame for frame in frames
        if "noframenumbering" not in frame.options and "plain" not in frame.options
    ]
    findings = audit_frames(frames, deck_root)

    timing: dict[str, Any] | None = None
    if duration_minutes is not None:
        low, high, benchmark = recommended_frame_range(duration_minutes)
        timing = {
            "duration_minutes": duration_minutes,
            "content_source_frames": len(content_frames),
            "recommended_range": [low, high],
            "nearest_benchmark_minutes": benchmark,
        }
        if not low <= len(content_frames) <= high:
            findings.append(Finding(
                "warning", "timing_budget_mismatch", _display_path(entries[0], deck_root), None,
                f"The deck has {len(content_frames)} content source frames for {duration_minutes:g} minutes; "
                f"the {benchmark}-minute benchmark is {low}-{high}.",
                "Rehearse and adjust the source-frame budget; do not count overlay pages as separate planned slides.",
            ))

    if log:
        findings.extend(inspect_log(log.resolve(), deck_root))
    pdf_metrics = None
    if pdf:
        pdf_metrics, pdf_findings = inspect_pdf(pdf.resolve(), render_dir.resolve() if render_dir else None, deck_root)
        findings.extend(pdf_findings)

    findings.sort(key=lambda item: (SEVERITY_ORDER[item.severity], item.path, item.line or 0, item.code))
    counts = {severity: sum(item.severity == severity for item in findings) for severity in SEVERITY_ORDER}
    status = "fail" if counts["error"] else ("warn" if counts["warning"] else "pass")
    return {
        "status": status,
        "entries": [str(path.resolve()) for path in entries],
        "sources": [_display_path(path, deck_root) for path in sources],
        "metrics": {
            "source_frame_count": len(frames),
            "content_source_frame_count": len(content_frames),
            "section_count": len({_clean_tex(frame.section) for frame in frames if frame.section}),
            "timing": timing,
            "pdf": pdf_metrics,
        },
        "counts": counts,
        "findings": [asdict(item) for item in findings],
    }


def _print_report(report: dict[str, Any]) -> None:
    metrics = report["metrics"]
    print(
        f"{report['status'].upper()}: {metrics['content_source_frame_count']} content frames, "
        f"{metrics['section_count']} sections, {report['counts']['error']} errors, "
        f"{report['counts']['warning']} warnings"
    )
    for finding in report["findings"]:
        location = finding["path"]
        if finding["line"] is not None:
            location += f":{finding['line']}"
        print(f"\n[{finding['severity'].upper()}] {finding['code']} at {location}")
        print(f"  Current: {finding['current']}")
        print(f"  Proposal: {finding['recommendation']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", nargs="+", help="Root deck or section TeX files")
    parser.add_argument("--duration-minutes", type=float)
    parser.add_argument("--log", help="TeX log to inspect")
    parser.add_argument("--pdf", help="Compiled deck PDF to inspect")
    parser.add_argument("--render-dir", help="Export compiled pages and a contact sheet")
    parser.add_argument("--report", help="Write the full JSON report")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--warnings-as-errors", action="store_true")
    args = parser.parse_args(argv)

    entries = [Path(value) for value in args.sources]
    missing = [str(path) for path in entries if not path.exists()]
    for optional in (args.log, args.pdf):
        if optional and not Path(optional).exists():
            missing.append(optional)
    if missing:
        print(f"ERROR: input not found: {', '.join(missing)}", file=sys.stderr)
        return 2

    report = build_report(
        entries,
        duration_minutes=args.duration_minutes,
        log=Path(args.log) if args.log else None,
        pdf=Path(args.pdf) if args.pdf else None,
        render_dir=Path(args.render_dir) if args.render_dir else None,
    )
    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        _print_report(report)

    failed = report["status"] == "fail" or (
        args.warnings_as_errors and report["status"] == "warn"
    )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
