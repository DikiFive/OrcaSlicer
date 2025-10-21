param(
  [string]$Vendor = 'LONGER'
)

$ErrorActionPreference = 'Stop'

$systemRoot = Join-Path $env:APPDATA 'OrcaSlicer\system'
$vendorDir = Join-Path $systemRoot $Vendor
$otaDir    = Join-Path $systemRoot 'ota'

Write-Host "System cache root: $systemRoot"
if (Test-Path $vendorDir) {
  Write-Host "Removing vendor cache: $vendorDir"
  Remove-Item $vendorDir -Recurse -Force
} else {
  Write-Host "Vendor cache not found: $vendorDir"
}

if (Test-Path $otaDir) {
  Write-Host "Removing OTA cache: $otaDir"
  Remove-Item $otaDir -Recurse -Force
} else {
  Write-Host "OTA cache not found: $otaDir"
}

Write-Host 'Done. Restart OrcaSlicer to rebuild system cache.'
