import importlib.util
from pathlib import Path
import sys


SCRIPT = Path(__file__).parents[1] / "scripts" / "deck_audit.py"
SPEC = importlib.util.spec_from_file_location("deck_audit", SCRIPT)
assert SPEC and SPEC.loader
deck_audit = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = deck_audit
SPEC.loader.exec_module(deck_audit)


def _write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _codes(report):
    return {finding["code"] for finding in report["findings"]}


def test_discovers_inputs_in_deck_order(tmp_path):
    root = _write(
        tmp_path / "deck.tex",
        r"""
\input{Sections/first}
\input{Sections/second}
""",
    )
    first = _write(tmp_path / "Sections" / "first.tex", "% first\n")
    second = _write(tmp_path / "Sections" / "second.tex", "% second\n")
    assert deck_audit.discover_sources([root]) == [root, first, second]


def test_does_not_count_frames_defined_in_template_preamble(tmp_path):
    root = _write(
        tmp_path / "deck.tex",
        "\\input{Sections/00_preamble}\n\\input{Sections/content}\n",
    )
    _write(
        tmp_path / "Sections" / "00_preamble.tex",
        r"\newcommand{\divider}{\begin{frame}[plain]X\end{frame}}",
    )
    _write(
        tmp_path / "Sections" / "content.tex",
        r"""
\section{Evidence}
\begin{frame}{The evidence supports the stated operating range}X\end{frame}
""",
    )
    report = deck_audit.build_report([root])
    assert report["metrics"]["source_frame_count"] == 1
    assert report["metrics"]["content_source_frame_count"] == 1


def test_reports_generic_static_dense_and_missing_content(tmp_path):
    root = _write(
        tmp_path / "deck.tex",
        r"""
\section{Results}
\begin{frame}{Results}
\begin{itemize}
\item A
\item B
\item C
\item D
\item E
\item F
\item G
\end{itemize}
\includegraphics{figures/not-there.pdf}
\missingfigure{pending}
\end{frame}
""",
    )
    report = deck_audit.build_report([root])
    assert {
        "generic_frame_title",
        "static_visible_list",
        "high_bullet_density",
        "missing_asset",
        "unresolved_placeholder",
    } <= _codes(report)
    assert report["status"] == "warn"


def test_accepts_action_title_incremental_list_and_existing_asset(tmp_path):
    _write(tmp_path / "figures" / "result.pdf", "placeholder")
    root = _write(
        tmp_path / "deck.tex",
        r"""
\section{Evidence}
\begin{frame}{The measured gain persists across the tested loss range}
\begin{itemize}[<+->]
\item A
\item B
\end{itemize}
\includegraphics{figures/result.pdf}
\end{frame}
""",
    )
    report = deck_audit.build_report([root])
    assert report["status"] == "pass"
    assert report["findings"] == []


def test_static_legend_can_be_intentionally_allowed(tmp_path):
    root = _write(
        tmp_path / "deck.tex",
        r"""
\section{Model}
\begin{frame}{Line styles distinguish measured and simulated curves}
% audit: allow-static-list
\begin{itemize}
\item Solid: measured
\item Dashed: simulated
\end{itemize}
\end{frame}
""",
    )
    report = deck_audit.build_report([root])
    assert "static_visible_list" not in _codes(report)


def test_missing_example_asset_can_be_intentionally_allowed(tmp_path):
    root = _write(
        tmp_path / "deck.tex",
        r"""
\section{Figures}
\begin{frame}{Missing figures remain visible during drafting}
% audit: allow-missing-asset
\includegraphics{figures/deliberately-missing.pdf}
\end{frame}
""",
    )
    report = deck_audit.build_report([root])
    assert "missing_asset" not in _codes(report)


def test_column_overflow_is_a_hard_error(tmp_path):
    root = _write(
        tmp_path / "deck.tex",
        r"""
\section{Comparison}
\begin{frame}{Both methods expose the same scaling bottleneck}
\begin{column}{0.55\textwidth}A\end{column}
\begin{column}{0.55\textwidth}B\end{column}
\end{frame}
""",
    )
    report = deck_audit.build_report([root])
    assert "column_width_overflow" in _codes(report)
    assert report["status"] == "fail"


def test_timing_uses_source_frames_not_overlays(tmp_path):
    frames = "\n".join(
        rf"\begin{{frame}}{{Claim {index} establishes the next step}}X\end{{frame}}"
        for index in range(3)
    )
    root = _write(tmp_path / "deck.tex", "\\section{Argument}\n" + frames)
    report = deck_audit.build_report([root], duration_minutes=15)
    assert report["metrics"]["content_source_frame_count"] == 3
    assert report["metrics"]["timing"]["recommended_range"] == [10, 15]
    assert "timing_budget_mismatch" in _codes(report)


def test_log_reports_fatal_undefined_and_large_overfull(tmp_path):
    log = _write(
        tmp_path / "deck.log",
        "! Undefined control sequence.\n"
        "LaTeX Warning: Reference `x' undefined.\n"
        "Overfull \\hbox (12.5pt too wide) in paragraph\n",
    )
    findings = deck_audit.inspect_log(log, tmp_path)
    assert {item.code for item in findings} == {
        "tex_error",
        "undefined_reference",
        "large_overfull_hbox",
    }
