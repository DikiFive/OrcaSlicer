param(
    [string]$AppProfilesRoot = 'F:\OrcaSlicer\resources\profiles',
    [string]$UserProfile = "$env:USERPROFILE"
)
$ErrorActionPreference = 'Stop'
$srcVendorJson = Join-Path $AppProfilesRoot 'LONGER.json'
$srcVendorFolder = Join-Path $AppProfilesRoot 'LONGER'
$dstSystemRoot = Join-Path $UserProfile 'AppData\Roaming\OrcaSlicer\system'
$dstVendorJson = Join-Path $dstSystemRoot 'LONGER.json'
$dstVendorFolder = Join-Path $dstSystemRoot 'LONGER'

Write-Host '== Push LONGER to system cache =='
Write-Host "Source index:  $srcVendorJson"
Write-Host "Source folder: $srcVendorFolder"
Write-Host "Dest root:     $dstSystemRoot"

if(!(Test-Path $srcVendorJson)){ throw "Missing source vendor index: $srcVendorJson" }
if(!(Test-Path $srcVendorFolder)){ throw "Missing source vendor folder: $srcVendorFolder" }

# Ensure destination exists
New-Item -ItemType Directory -Force -Path $dstVendorFolder | Out-Null

# Copy index to root (ensures force_update reflects current value)
Copy-Item -Force $srcVendorJson $dstVendorJson

# Copy all vendor files to system folder
robocopy $srcVendorFolder $dstVendorFolder /MIR /NFL /NDL /NJH /NJS /NC /NS | Out-Null

# Report summary
$ver = (Get-Content -Raw $dstVendorJson | ConvertFrom-Json).version
$fu  = (Get-Content -Raw $dstVendorJson | ConvertFrom-Json).force_update
Write-Host "Installed system index version: $ver (force_update=$fu)"
Write-Host 'Files in system vendor folder:'
Get-ChildItem -File -Recurse $dstVendorFolder | Select-Object FullName,Length | Sort-Object FullName | Format-Table -AutoSize

Write-Host '== DONE. Restart OrcaSlicer and re-open Add Printer to verify LONGER appears =='