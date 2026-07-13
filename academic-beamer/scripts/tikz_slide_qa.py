#!/usr/bin/env python3
"""Lint TikZ slide source and render selected Beamer PDF pages for QA."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re
import sys
from typing import Any


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    message: str


UNSAFE_PATTERNS = {
    "shell_escape": re.compile(r"\\(?:immediate\s*)?write18\b"),
    "pipe_input": re.compile(r"\\(?:input|include)\s*\{\s*\|"),
}
DRAW_COMMAND_RE = re.compile(r"\\(?:draw|path)\b(?P<body>[^;]*);", re.DOTALL)
EDGE_NODE_RE = re.compile(r"\bnode(?P<opts>\[[^\]]*\])?\s*\{[^{}]*\}", re.DOTALL)
SIMPLE_NODE_RE = re.compile(r"\\node(?P<opts>\[[^\]]*\])?[^\{;]*\{(?P<body>[^{}]*)\}", re.DOTALL)
INCLUDE_RE = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{(?P<path>[^{}]+)\}")
POSITION_WORDS = ("above", "below", "left", "right", "pos=", "midway", "near start", "near end", "auto", "sloped")


def _clean(text: str) -> str:
    return " ".join(text.split())


def check_source(path: Path) -> list[Finding]:
    text = path.read_text(encoding="utf-8", errors="replace")
    findings: list[Finding] = []

    begins = text.count(r"\begin{tikzpicture}")
    ends = text.count(r"\end{tikzpicture}")
    if begins != ends:
        findings.append(Finding("error", "unbalanced_tikzpicture", f"Found {begins} begin and {ends} end markers."))

    for code, pattern in UNSAFE_PATTERNS.items():
        if pattern.search(text):
            findings.append(Finding("error", code, "The source requests shell or pipe execution."))

    for match in SIMPLE_NODE_RE.finditer(text):
        body = _clean(match.group("body"))
        opts = match.group("opts") or ""
        if len(body) > 64 and "text width" not in opts:
            findings.append(Finding(
                "warn",
                "long_unwrapped_node",
                f"Long node text has no explicit text width: {body[:90]!r}",
            ))

    for command in DRAW_COMMAND_RE.finditer(text):
        for match in EDGE_NODE_RE.finditer(command.group("body")):
            opts = (match.group("opts") or "").casefold()
            if not any(word in opts for word in POSITION_WORDS):
                findings.append(Finding(
                    "warn",
                    "unpositioned_edge_label",
                    "An edge label needs an explicit position such as above, below, sloped, or pos=...",
                ))

    if re.search(r"\\begin\{tikzpicture\}\[[^\]]*\bscale\s*=", text) and "transform shape" not in text:
        findings.append(Finding(
            "warn",
            "scale_without_transform_shape",
            "tikzpicture uses scale without transform shape; text and nodes may scale differently.",
        ))
    if r"\tiny" in text:
        findings.append(Finding("warn", "tiny_text", "Do not use tiny text as a layout fix; simplify or split the slide."))
    if r"\usepackage{animate}" in text or r"\begin{animateinline}" in text:
        findings.append(Finding(
            "warn",
            "decorative_animation",
            "Prefer Beamer overlays unless motion itself carries technical meaning and playback support is known.",
        ))
    if re.search(r"\\only<[^>]+>\s*\{[^{}]*(?:\\node|\\draw|\\path)", text, re.DOTALL):
        findings.append(Finding(
            "warn",
            "overlay_geometry_in_only",
            "Geometry inside \\only may jump between overlays; keep coordinates fixed and reveal state or emphasis.",
        ))

    for match in INCLUDE_RE.finditer(text):
        value = match.group("path").strip()
        if re.match(r"^(?:[A-Za-z]:[\\/]|/home/|/Users/)", value):
            findings.append(Finding("warn", "absolute_asset_path", f"Use a project-relative asset path: {value}"))

    return findings


def _intersection_ratio(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> float:
    x0, y0 = max(a[0], b[0]), max(a[1], b[1])
    x1, y1 = min(a[2], b[2]), min(a[3], b[3])
    if x1 <= x0 or y1 <= y0:
        return 0.0
    overlap = (x1 - x0) * (y1 - y0)
    area_a = max(0.1, (a[2] - a[0]) * (a[3] - a[1]))
    area_b = max(0.1, (b[2] - b[0]) * (b[3] - b[1]))
    return overlap / min(area_a, area_b)


def check_text_geometry(spans: list[dict[str, Any]], width: float, height: float) -> list[Finding]:
    findings: list[Finding] = []
    footer_top = 0.90 * height

    for span in spans:
        x0, y0, x1, y1 = span["bbox"]
        if min(x0, y0, width - x1, height - y1) < 1.5:
            findings.append(Finding("warn", "text_near_page_edge", f"Text is near a page edge: {span['text']!r}"))
        if y1 > footer_top and span.get("size", 99.0) > 5.6:
            findings.append(Finding(
                "error",
                "body_text_in_footer_band",
                f"Body-sized text enters the footer/logo band: {span['text']!r}",
            ))

    for index, first in enumerate(spans):
        for second in spans[index + 1:]:
            if first["block"] == second["block"] and first["line"] == second["line"]:
                continue
            if _intersection_ratio(first["bbox"], second["bbox"]) >= 0.20:
                findings.append(Finding(
                    "error",
                    "text_overlap",
                    f"Rendered text boxes overlap: {first['text']!r} and {second['text']!r}",
                ))
    return findings


def parse_pages(value: str | None, page_count: int) -> list[int]:
    if not value:
        return list(range(page_count))
    selected: set[int] = set()
    for part in value.split(","):
        token = part.strip()
        if not token:
            continue
        if "-" in token:
            start_text, end_text = token.split("-", 1)
            start, end = int(start_text), int(end_text)
            selected.update(range(start - 1, end))
        else:
            selected.add(int(token) - 1)
    invalid = [page + 1 for page in selected if page < 0 or page >= page_count]
    if invalid:
        raise ValueError(f"Page selection outside 1..{page_count}: {invalid}")
    return sorted(selected)


def render_pdf(pdf: Path, output_dir: Path, pages: str | None, dpi: int) -> tuple[list[dict[str, Any]], list[Finding]]:
    try:
        import fitz
        from PIL import Image, ImageOps
    except ImportError as exc:
        return [], [Finding("error", "missing_render_dependency", f"Install PyMuPDF and Pillow: {exc}")]

    doc = fitz.open(pdf)
    if doc.page_count < 1:
        return [], [Finding("error", "empty_pdf", "The PDF has no pages.")]

    output_dir.mkdir(parents=True, exist_ok=True)
    findings: list[Finding] = []
    page_records: list[dict[str, Any]] = []
    thumbnails = []
    for page_index in parse_pages(pages, doc.page_count):
        page = doc[page_index]
        width, height = float(page.rect.width), float(page.rect.height)
        if abs((width / height) - (16 / 9)) > 0.03:
            findings.append(Finding("warn", "unexpected_aspect_ratio", f"Page {page_index + 1} is not 16:9."))

        pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72.0, dpi / 72.0), alpha=False)
        png = output_dir / f"page-{page_index + 1:03d}.png"
        pix.save(png)
        image = Image.open(png).convert("RGB")
        gray = ImageOps.grayscale(image)
        ink_pixels = sum(gray.histogram()[:248])
        ink_fraction = ink_pixels / max(1, image.width * image.height)
        if ink_fraction < 0.0004:
            findings.append(Finding("error", "blank_render", f"Page {page_index + 1} appears blank."))

        spans: list[dict[str, Any]] = []
        for block_index, block in enumerate(page.get_text("dict").get("blocks", [])):
            for line_index, line in enumerate(block.get("lines", [])):
                for span in line.get("spans", []):
                    label = _clean(span.get("text", ""))
                    bbox = tuple(float(item) for item in span.get("bbox", (0, 0, 0, 0)))
                    if label and bbox[2] > bbox[0] and bbox[3] > bbox[1]:
                        spans.append({
                            "text": label,
                            "bbox": bbox,
                            "size": float(span.get("size", 0.0)),
                            "block": block_index,
                            "line": line_index,
                        })
        findings.extend(check_text_geometry(spans, width, height))
        page_records.append({
            "page": page_index + 1,
            "png": str(png),
            "width_pt": width,
            "height_pt": height,
            "ink_fraction": round(ink_fraction, 6),
            "text_span_count": len(spans),
        })
        thumb = image.copy()
        thumb.thumbnail((480, 270))
        thumbnails.append((page_index + 1, thumb))

    if thumbnails:
        sheet = Image.new("RGB", (500, len(thumbnails) * 300), "white")
        from PIL import ImageDraw
        draw = ImageDraw.Draw(sheet)
        for row, (page_number, thumb) in enumerate(thumbnails):
            y = row * 300
            sheet.paste(thumb, (10, y + 22))
            draw.text((10, y + 4), f"Page {page_number}", fill="black")
        sheet.save(output_dir / "contact-sheet.png")

    return page_records, findings


def _status(findings: list[Finding]) -> str:
    if any(item.severity == "error" for item in findings):
        return "fail"
    return "warn" if findings else "pass"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", nargs="+", help="Beamer section or TikZ source files")
    parser.add_argument("--pdf", help="Compiled preview or full deck PDF")
    parser.add_argument("--pages", help="One-based pages, for example 3,5-7; default is all pages")
    parser.add_argument("--dpi", type=int, default=160)
    parser.add_argument("--output-dir")
    parser.add_argument("--report")
    parser.add_argument("--logic", choices=("exact", "schematic", "needs-source"), default="needs-source")
    parser.add_argument("--decision", choices=("pending", "keep", "simplify", "split", "reject"), default="pending")
    parser.add_argument("--warnings-as-errors", action="store_true")
    args = parser.parse_args(argv)

    source_paths = [Path(value).resolve() for value in args.sources]
    missing = [str(path) for path in source_paths if not path.exists()]
    if missing:
        print(f"ERROR: source file not found: {missing}", file=sys.stderr)
        return 2

    pdf = Path(args.pdf).resolve() if args.pdf else None
    if pdf and not pdf.exists():
        print(f"ERROR: PDF not found: {pdf}", file=sys.stderr)
        return 2

    default_root = pdf.parent if pdf else source_paths[0].parent
    output_dir = Path(args.output_dir).resolve() if args.output_dir else default_root / "tikz-qa"
    report_path = Path(args.report).resolve() if args.report else output_dir / "tikz-slide-qa.json"

    findings: list[Finding] = []
    source_reports = []
    for path in source_paths:
        source_findings = check_source(path)
        findings.extend(source_findings)
        source_reports.append({"source": str(path), "findings": [asdict(item) for item in source_findings]})

    page_reports: list[dict[str, Any]] = []
    if pdf:
        try:
            page_reports, render_findings = render_pdf(pdf, output_dir, args.pages, args.dpi)
            findings.extend(render_findings)
        except (OSError, ValueError) as exc:
            findings.append(Finding("error", "pdf_qa_failed", str(exc)))

    report = {
        "sources": source_reports,
        "pdf": str(pdf) if pdf else None,
        "pages": page_reports,
        "logic_review": args.logic,
        "design_decision": args.decision,
        "findings": [asdict(item) for item in findings],
        "status": _status(findings),
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"{report['status'].upper()}: {', '.join(str(path) for path in source_paths)}")
    for item in findings:
        print(f"{item.severity.upper()}: {item.code}: {item.message}")
    print(f"QA: {report_path}")

    failed = report["status"] == "fail" or (args.warnings_as_errors and report["status"] == "warn")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

