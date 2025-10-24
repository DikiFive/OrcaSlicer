param(
    [string]$Vendor = "LONGER"
)

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$profilesSrc = Join-Path $repoRoot "resources\profiles"
$systemDest = Join-Path $env:APPDATA "OrcaSlicer\system"

Write-Host "Repo:    $repoRoot"
Write-Host "Source:  $profilesSrc"
Write-Host "Dest:    $systemDest"

New-Item -ItemType Directory -Force -Path $systemDest | Out-Null

# Copy vendor index
$vendorIndexSrc = Join-Path $profilesSrc ("{0}.json" -f $Vendor)
$vendorIndexDst = Join-Path $systemDest ("{0}.json" -f $Vendor)
Copy-Item -Path $vendorIndexSrc -Destination $vendorIndexDst -Force

# Copy vendor folder
$vendorFolderSrc = Join-Path $profilesSrc $Vendor
$vendorFolderDst = Join-Path $systemDest $Vendor
Copy-Item -Path $vendorFolderSrc -Destination $systemDest -Recurse -Force

# Verify
$okIndex = Test-Path $vendorIndexDst
$okCommon = Test-Path (Join-Path $vendorFolderDst "machine\fdm_machine_common.json")
$machineCount = (Get-ChildItem -Path (Join-Path $vendorFolderDst "machine") -Filter "*.json").Count

[pscustomobject]@{
  vendor_index    = $okIndex
  common_exists   = $okCommon
  machine_count   = $machineCount
  timestamp       = (Get-Date)
} | Format-List

Write-Host "Done. Restart OrcaSlicer to load updated profiles." -ForegroundColor Green
return
