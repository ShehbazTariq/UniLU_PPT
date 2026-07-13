<#
.SYNOPSIS
  Render paper pages or cropped figure regions with source provenance.

.DESCRIPTION
  Uses Poppler's pdftoppm. Each output is recorded in figure_sources.csv with
  the source PDF, source SHA-256, page, DPI, and crop. The crop format is
  x,y,width,height in rendered pixels at the selected DPI.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File academic-beamer/scripts/extract_pdf_figure.ps1 `
    -Pdf notes/paper.pdf -Pages 4 -Crop '180,260,1650,900' -Prefix architecture

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File academic-beamer/scripts/extract_pdf_figure.ps1 `
    -Pdf notes/paper.pdf -Pages '4,7-8' -OutputDir figures/extracted
#>
param(
  [string]$Root = '',
  [Parameter(Mandatory = $true)]
  [string]$Pdf,
  [Parameter(Mandatory = $true)]
  [string]$Pages,
  [string]$Crop = '',
  [int]$Dpi = 220,
  [string]$OutputDir = 'figures/extracted',
  [string]$Prefix = '',
  [switch]$Force
)

$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($Root)) {
  $scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
  $Root = (Resolve-Path -LiteralPath (Join-Path $scriptDirectory '..\..')).Path
}

function Expand-PageSelection {
  param([string]$Value)
  $selected = New-Object 'System.Collections.Generic.SortedSet[int]'
  foreach ($part in $Value.Split(',')) {
    $token = $part.Trim()
    if ($token -match '^([0-9]+)-([0-9]+)$') {
      $start = [int]$Matches[1]
      $end = [int]$Matches[2]
      if ($start -lt 1 -or $end -lt $start) {
        throw "Invalid page range: $token"
      }
      for ($page = $start; $page -le $end; $page++) {
        [void]$selected.Add($page)
      }
    } elseif ($token -match '^[0-9]+$') {
      $page = [int]$token
      if ($page -lt 1) { throw "Page numbers are one-based: $token" }
      [void]$selected.Add($page)
    } else {
      throw "Invalid page selection token: $token"
    }
  }
  return $selected
}

$rootPath = (Resolve-Path -LiteralPath $Root).Path
if ([System.IO.Path]::IsPathRooted($Pdf)) {
  $pdfCandidate = $Pdf
} else {
  $pdfCandidate = Join-Path $rootPath $Pdf
}
$pdfPath = (Resolve-Path -LiteralPath $pdfCandidate).Path
$poppler = Get-Command pdftoppm -ErrorAction SilentlyContinue
if (-not $poppler) {
  Write-Host 'FAIL: pdftoppm was not found. Install Poppler and add it to PATH.'
  exit 1
}
if ($Dpi -lt 72) {
  Write-Host 'FAIL: DPI must be at least 72.'
  exit 1
}

$outputDirWasRelative = -not [System.IO.Path]::IsPathRooted($OutputDir)
if (-not $outputDirWasRelative) {
  $outputPath = [System.IO.Path]::GetFullPath($OutputDir)
} else {
  $outputPath = [System.IO.Path]::GetFullPath((Join-Path $rootPath $OutputDir))
}
New-Item -ItemType Directory -Path $outputPath -Force | Out-Null

if ([string]::IsNullOrWhiteSpace($Prefix)) {
  $Prefix = [System.IO.Path]::GetFileNameWithoutExtension($pdfPath)
}
$Prefix = ($Prefix -replace '[^A-Za-z0-9_-]', '-').Trim('-')
if ([string]::IsNullOrWhiteSpace($Prefix)) { $Prefix = 'figure' }

$cropArgs = @()
$cropLabel = ''
if (-not [string]::IsNullOrWhiteSpace($Crop)) {
  $parts = @($Crop.Split(',') | ForEach-Object { $_.Trim() })
  if ($parts.Count -ne 4 -or ($parts | Where-Object { $_ -notmatch '^[0-9]+$' })) {
    Write-Host "FAIL: Crop must be x,y,width,height in non-negative rendered pixels."
    exit 1
  }
  $x, $y, $width, $height = $parts | ForEach-Object { [int]$_ }
  if ($width -lt 1 -or $height -lt 1) {
    Write-Host 'FAIL: Crop width and height must be positive.'
    exit 1
  }
  $cropArgs = @('-x', $x, '-y', $y, '-W', $width, '-H', $height)
  $cropLabel = "$x,$y,$width,$height"
}

$sourceHash = (Get-FileHash -LiteralPath $pdfPath -Algorithm SHA256).Hash.ToLowerInvariant()
$manifest = Join-Path $outputPath 'figure_sources.csv'
$records = @()
$pageSelection = @(Expand-PageSelection -Value $Pages)

foreach ($page in $pageSelection) {
  $name = '{0}-page-{1:D3}' -f $Prefix, $page
  if ($cropLabel) { $name += '-crop' }
  $basePath = Join-Path $outputPath $name
  $pngPath = "$basePath.png"
  if ((Test-Path -LiteralPath $pngPath) -and -not $Force) {
    Write-Host "FAIL: output exists: $pngPath (use -Force to replace it)"
    exit 1
  }

  $arguments = @('-f', $page, '-l', $page, '-singlefile', '-r', $Dpi)
  $arguments += $cropArgs
  $arguments += @('-png', $pdfPath, $basePath)
  & $poppler.Source @arguments
  if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $pngPath)) {
    Write-Host "FAIL: pdftoppm did not create $pngPath"
    exit 1
  }

  $records += [pscustomobject]@{
    Asset = $pngPath
    SourcePdf = $pdfPath
    SourceSha256 = $sourceHash
    SourcePage = $page
    Dpi = $Dpi
    CropPixels = $cropLabel
    ExtractedUtc = [DateTime]::UtcNow.ToString('o')
  }
  Write-Host "OK  -> $pngPath"
  if ($outputDirWasRelative) {
    $texPath = (Join-Path $OutputDir "$name.png").Replace('\', '/')
  } else {
    $texPath = $pngPath.Replace('\', '/')
  }
  Write-Host "TeX -> \includegraphics[width=0.85\textwidth]{$texPath}"
}

if (Test-Path -LiteralPath $manifest) {
  $records | Export-Csv -LiteralPath $manifest -NoTypeInformation -Append
} else {
  $records | Export-Csv -LiteralPath $manifest -NoTypeInformation
}
Write-Host "Provenance -> $manifest"
