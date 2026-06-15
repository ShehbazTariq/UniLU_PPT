<#
.SYNOPSIS
  Build the UniLU/SnT Beamer deck reliably.

.DESCRIPTION
  - Closes Adobe (it locks the output PDF and breaks the build).
  - Runs pdflatex TWICE: the title and closing slides use TikZ
    `remember picture`, which always needs two passes (first pass is blank).
  - Reports the output path plus any fatal errors / missing files.

  Run with no arguments from anywhere; it resolves the template root as the
  grandparent of this script (UniLU_PPT/). Override with -Root / -Job.

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

# 2. Two passes (remember picture). First pass output is suppressed.
& pdflatex -interaction=nonstopmode "$Job.tex" 2>&1 | Out-Null
& pdflatex -interaction=nonstopmode "$Job.tex" 2>&1 | Out-Null

# 3. Report.
$pdf = Join-Path $Root "$Job.pdf"
if (Test-Path -LiteralPath $pdf) {
  Write-Host "OK  -> $pdf"
} else {
  Write-Host "FAIL: no PDF produced."
}

$log = "$Job.log"
if (Test-Path -LiteralPath $log) {
  $lines = Get-Content -LiteralPath $log
  $fatal   = $lines | Select-String -Pattern '^!'           # TeX errors
  $missing = $lines | Select-String -Pattern 'No file|not found|Missing'
  if ($fatal)   { Write-Host "`n-- errors --";        $fatal   | ForEach-Object { $_.Line } }
  if ($missing) { Write-Host "`n-- missing files --"; $missing | Select-Object -First 10 | ForEach-Object { $_.Line } }
  if (-not $fatal -and -not $missing) { Write-Host "No fatal errors or missing files in the log." }
}
