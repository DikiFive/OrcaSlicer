[CmdletBinding()]
param(
  [Parameter(Mandatory = $true, HelpMessage = 'Path to installed app resources/profiles, e.g. F:\\OrcaSlicer\\resources\\profiles')]
  [string]$AppProfilesRoot,
  [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

Write-Host '--- Sync LONGER profiles to installed app ---'

$repoRoot = Split-Path -Parent $PSScriptRoot
$srcRoot  = Join-Path $repoRoot 'resources\profiles'
$vendor   = 'LONGER'

$srcVendorDir = Join-Path $srcRoot $vendor
$srcIndexFile = Join-Path $srcRoot 'LONGER.json'

if (-not (Test-Path $srcVendorDir)) { throw "Source vendor dir not found: $srcVendorDir" }
if (-not (Test-Path $srcIndexFile)) { throw "Source index file not found: $srcIndexFile" }

if (-not (Test-Path $AppProfilesRoot)) { throw "App profiles root not found: $AppProfilesRoot" }

$dstVendorDir = Join-Path $AppProfilesRoot $vendor
$dstIndexFile = Join-Path $AppProfilesRoot 'LONGER.json'

Write-Host "Source: $srcVendorDir"
Write-Host "Target: $dstVendorDir"

$ts = Get-Date -Format 'yyyyMMdd-HHmmss'
$backupRoot = Join-Path $AppProfilesRoot '_backup'

if (-not $DryRun) {
  New-Item -ItemType Directory -Force -Path $backupRoot | Out-Null
  if (Test-Path $dstVendorDir) {
    $bk = Join-Path $backupRoot ("$vendor`_$ts")
    Copy-Item $dstVendorDir $bk -Recurse -Force
    Write-Host "Backup created: $bk"
  }
  if (Test-Path $dstIndexFile) {
    Copy-Item $dstIndexFile (Join-Path $backupRoot ("$vendor`_$ts.LONGER.json")) -Force
  }
  # Remove old vendor dir to avoid stale files (e.g., obsolete *Pro* names)
  Remove-Item $dstVendorDir -Recurse -Force -ErrorAction SilentlyContinue
  # Copy fresh vendor dir and index
  Copy-Item $srcVendorDir $dstVendorDir -Recurse -Force
  Copy-Item $srcIndexFile $dstIndexFile -Force

  # Remove legacy '* Pro*.json' files from destination to avoid duplicates
  $legacyPatterns = @(
    (Join-Path $dstVendorDir 'machine\* Pro*.json'),
    (Join-Path $dstVendorDir 'process\* Pro*.json')
  )
  foreach ($pat in $legacyPatterns) {
    Get-ChildItem -Path $pat -ErrorAction SilentlyContinue | ForEach-Object {
      Write-Host "Removing legacy file: $($_.FullName)"
      Remove-Item $_.FullName -Force -ErrorAction SilentlyContinue
    }
  }
} else {
  Write-Host '(DryRun) No changes will be made. Preview only.'
}

# Quick sanity printout
if ($DryRun) {
  Write-Host 'Source vendor files (preview):'
  Get-ChildItem $srcVendorDir -Recurse | Select-Object FullName, Length | Sort-Object FullName | Format-Table -AutoSize | Out-Host
  $srcVersion = (Get-Content $srcIndexFile -Raw | ConvertFrom-Json).version
  Write-Host "Source index version: $srcVersion"
  if (Test-Path $dstVendorDir) {
    Write-Host 'Target vendor dir already exists (will be replaced on real run).'
  } else {
    Write-Host 'Target vendor dir does not exist yet (will be created on real run).'
  }
} else {
  Write-Host 'Target vendor files:'
  Get-ChildItem $dstVendorDir -Recurse | Select-Object FullName, Length | Sort-Object FullName | Format-Table -AutoSize | Out-Host
  if (Test-Path $dstIndexFile) {
    $dstVersion = (Get-Content $dstIndexFile -Raw | ConvertFrom-Json).version
    Write-Host "Installed index version: $dstVersion"
  }
}

Write-Host '--- DONE (sync) ---'
