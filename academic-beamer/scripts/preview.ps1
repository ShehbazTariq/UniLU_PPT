<#
.SYNOPSIS
  Build one Beamer section file, or one labeled frame, in isolation.

.DESCRIPTION
  Generates a temporary preview driver at the deck root. The driver loads the
  normal preamble and metadata, then inputs only the requested source file. If
  -FrameLabel is supplied, the driver also uses Beamer's \includeonlyframes.

  This is for fast layout checks while editing. Run the full build.ps1 before
  delivering a deck, because the full deck is still the source of final frame
  numbers, section navigation, references, and closing/title geometry.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File academic-beamer/scripts/preview.ps1 `
    -Source Sections/03_motivation_and_model.tex

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File academic-beamer/scripts/preview.ps1 `
    -Source Sections/03_motivation_and_model.tex -FrameLabel kl-conditions
#>
param(
  [string]$Root = '',
  [Parameter(Mandatory = $true)]
  [string]$Source,
  [string]$FrameLabel = '',
  [string]$Job = '_preview',
  [switch]$Open
)

Get-Process Acrobat, AcroRd32, SumatraPDF, FoxitReader, texworks -ErrorAction SilentlyContinue |
  Stop-Process -Force -ErrorAction SilentlyContinue

if ([string]::IsNullOrWhiteSpace($Root)) {
  $Root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..\..')).Path
} else {
  $Root = (Resolve-Path -LiteralPath $Root).Path
}
Set-Location -LiteralPath $Root

$sourcePath = Join-Path $Root $Source
if (-not (Test-Path -LiteralPath $sourcePath)) {
  Write-Host "FAIL: source file not found: $sourcePath"
  exit 1
}

$sourceForTex = $Source.Replace('\', '/')
$driver = Join-Path $Root "$Job.tex"
$pdf = Join-Path $Root "$Job.pdf"

if (Test-Path -LiteralPath $pdf) {
  Remove-Item -LiteralPath $pdf -Force -ErrorAction SilentlyContinue
}

$driverLines = @()
$driverLines += '\input{Sections/00_preamble}'
if ($FrameLabel.Trim().Length -gt 0) {
  $driverLines += "\includeonlyframes{$FrameLabel}"
}
$driverLines += '\input{Sections/01_metadata}'
$driverLines += ''
$driverLines += '\begin{document}'
$driverLines += "\input{$sourceForTex}"
$driverLines += '\end{document}'

Set-Content -LiteralPath $driver -Value $driverLines -Encoding ASCII

& pdflatex -interaction=nonstopmode "$Job.tex" | Out-Null
& pdflatex -interaction=nonstopmode "$Job.tex" | Out-Null
$exitCode = $LASTEXITCODE

if ((Test-Path -LiteralPath $pdf) -and ($exitCode -eq 0)) {
  Write-Host "OK  -> $pdf"
  if ($FrameLabel.Trim().Length -gt 0) {
    Write-Host "Previewed frame label '$FrameLabel' from $Source"
  } else {
    Write-Host "Previewed source $Source"
  }
} else {
  Write-Host "FAIL: preview build did not complete cleanly (pdflatex exit $exitCode)."
}

$log = "$Job.log"
if (Test-Path -LiteralPath $log) {
  $lines = Get-Content -LiteralPath $log
  $fatal = $lines | Select-String -Pattern '^!'
  $missing = $lines | Select-String -Pattern 'LaTeX Warning: File .* not found'
  if ($fatal) { Write-Host "`n-- errors --"; $fatal | ForEach-Object { $_.Line } }
  if ($missing) { Write-Host "`n-- missing files --"; $missing | Select-Object -First 10 | ForEach-Object { $_.Line } }
  if (-not $fatal -and -not $missing) { Write-Host "No fatal errors or missing files in the preview log." }
}

if ($Open -and (Test-Path -LiteralPath $pdf)) {
  explorer $pdf
}

if (-not ((Test-Path -LiteralPath $pdf) -and ($exitCode -eq 0))) {
  exit 1
}
