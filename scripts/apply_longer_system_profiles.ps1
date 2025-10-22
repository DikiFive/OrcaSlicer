param(
  [Parameter(Mandatory=$false)]
  [string]$AppProfilesRoot = 'F:\OrcaSlicer\resources\profiles'
)

$ErrorActionPreference = 'Stop'

Write-Host '== Apply LONGER system profiles (sync + cache clear) =='
Write-Host "App profiles root: $AppProfilesRoot"

& pwsh -NoProfile -ExecutionPolicy Bypass -File "$PSScriptRoot/sync_longer_profiles_to_app.ps1" -AppProfilesRoot $AppProfilesRoot

& pwsh -NoProfile -ExecutionPolicy Bypass -File "$PSScriptRoot/clear_orca_system_cache.ps1"

Write-Host '== DONE. Please restart OrcaSlicer and re-add system printers if needed. =='
