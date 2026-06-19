<#
.SYNOPSIS
  Build the UniLU/SnT Beamer deck reliably.

.DESCRIPTION
  - Closes Adobe (it locks the output PDF and breaks the build).
  - Deletes the previous PDF first, so a failed compile cannot leave a stale
    PDF behind and masquerade as success.
  - Runs pdflatex TWICE: the title and closing slides use TikZ
    `remember picture`, which always needs two passes (first pass is blank).
  - Reports success only when the second pass exits 0 AND a fresh PDF exists,
    then surfaces real TeX errors and genuinely missing input/graphics files
    (biblatex/biber info lines are intentionally not treated as errors).

  Run with no arguments from anywhere; it resolves the template root as the
  grandparent of this script (UniLU_PPT/). Override with -Root / -Job.

  Works with either `pwsh` (PowerShell 7) or `powershell` (Windows PowerShell 5.1):
    pwsh        academic-beamer/scripts/build.ps1
    powershell  -ExecutionPolicy Bypass -File academic-beamer/scripts/build.ps1

.EXAMPLE
  pwsh academic-beamer/scripts/build.ps1
  pwsh academic-beamer/scripts/build.ps1 -Job example
#>
param(
  [string]$Root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..\..')).Path,
  [string]$Job  = 'example'
)

# 1. Release the PDF if a viewer is holding it open.
Get-Process Acrobat, AcroRd32, SumatraPDF -ErrorAction SilentlyContinue |
  Stop-Process -Force -ErrorAction SilentlyContinue

Set-Location -LiteralPath $Root

$pdf = Join-Path $Root "$Job.pdf"

# 2. Remove stale output so a previous build cannot masquerade as success.
if (Test-Path -LiteralPath $pdf) {
  Remove-Item -LiteralPath $pdf -Force -ErrorAction SilentlyContinue
}

# 3. Two passes (remember picture). First pass output is suppressed.
#    stdout is discarded; the exit code of each pass is captured.
& pdflatex -interaction=nonstopmode "$Job.tex" | Out-Null
& pdflatex -interaction=nonstopmode "$Job.tex" | Out-Null
$exitCode = $LASTEXITCODE

# 4. Report. Success requires BOTH a clean exit and a freshly written PDF.
if ((Test-Path -LiteralPath $pdf) -and ($exitCode -eq 0)) {
  Write-Host "OK  -> $pdf"
} else {
  Write-Host "FAIL: build did not complete cleanly (pdflatex exit $exitCode)."
}

$log = "$Job.log"
if (Test-Path -LiteralPath $log) {
  $lines = Get-Content -LiteralPath $log
  # Real TeX errors start with '!'. Genuinely missing inputs/graphics are
  # reported by LaTeX as 'File ... not found' warnings. biblatex/biber emit
  # 'Info: ... not found' / 'No file *.bbl' lines that are NOT errors, so they
  # are deliberately excluded here.
  $fatal   = $lines | Select-String -Pattern '^!'
  $missing = $lines | Select-String -Pattern 'LaTeX Warning: File .* not found'
  if ($fatal)   { Write-Host "`n-- errors --";        $fatal   | ForEach-Object { $_.Line } }
  if ($missing) { Write-Host "`n-- missing files --"; $missing | Select-Object -First 10 | ForEach-Object { $_.Line } }
  if (-not $fatal -and -not $missing) { Write-Host "No fatal errors or missing files in the log." }
}

# Propagate failure to the caller (CI, chained commands).
if (-not ((Test-Path -LiteralPath $pdf) -and ($exitCode -eq 0))) { exit 1 }
