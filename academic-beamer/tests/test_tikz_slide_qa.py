import importlib.util
from pathlib import Path
import sys


SCRIPT = Path(__file__).parents[1] / "scripts" / "tikz_slide_qa.py"
SPEC = importlib.util.spec_from_file_location("tikz_slide_qa", SCRIPT)
assert SPEC and SPEC.loader
tikz_slide_qa = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = tikz_slide_qa
SPEC.loader.exec_module(tikz_slide_qa)


def _write(tmp_path, text):
    path = tmp_path / "slide.tex"
    path.write_text(text, encoding="utf-8")
    return path


def test_source_lint_accepts_positioned_edge_label(tmp_path):
    path = _write(
        tmp_path,
        r"""
\begin{tikzpicture}[node distance=12mm]
  \node[text width=2cm] (a) {Quantum state};
  \node[right=of a] (b) {Measurement};
  \draw[->] (a) -- node[above,midway] {channel} (b);
\end{tikzpicture}
""",
    )
    assert tikz_slide_qa.check_source(path) == []


def test_source_lint_reports_overlay_and_layout_risks(tmp_path):
    path = _write(
        tmp_path,
        r"""
\begin{tikzpicture}[scale=0.7]
  \node {This is a deliberately long node label that should be wrapped or moved out of the diagram};
  \draw (a) -- node {feedback} (b);
  \only<2>{\draw (b) -- (a);}
  \tiny
\end{tikzpicture}
""",
    )
    codes = {finding.code for finding in tikz_slide_qa.check_source(path)}
    assert "long_unwrapped_node" in codes
    assert "unpositioned_edge_label" in codes
    assert "overlay_geometry_in_only" in codes
    assert "scale_without_transform_shape" in codes
    assert "tiny_text" in codes


def test_footer_and_overlap_geometry_checks():
    spans = [
        {"text": "body", "bbox": (10.0, 90.0, 35.0, 98.0), "size": 10.0, "block": 0, "line": 0},
        {"text": "overlap", "bbox": (12.0, 91.0, 33.0, 98.0), "size": 10.0, "block": 1, "line": 0},
    ]
    codes = {finding.code for finding in tikz_slide_qa.check_text_geometry(spans, 160.0, 100.0)}
    assert "body_text_in_footer_band" in codes
    assert "text_overlap" in codes


def test_page_selection_is_one_based_and_supports_ranges():
    assert tikz_slide_qa.parse_pages("1,3-4", 5) == [0, 2, 3]

