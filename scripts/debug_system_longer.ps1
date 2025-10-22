param(
    [string]$UserProfile = "$env:USERPROFILE"
)
$ErrorActionPreference = 'Continue'
$sys = Join-Path $UserProfile 'AppData\Roaming\OrcaSlicer\system\LONGER'
$app = 'F:\OrcaSlicer\resources\profiles\LONGER'
Write-Host "System vendor path: $sys"
Write-Host "App vendor path:    $app"

function Show-FileInfo([string]$label, [string]$path){
    Write-Host "--- $label ---"
    if(Test-Path $path){
        $it = Get-Item $path
        Write-Host ("{0}  {1} bytes" -f $it.FullName, $it.Length)
        try {
            $raw = Get-Content -Raw $path -ErrorAction Stop
            $snippet = if($raw.Length -gt 256){ $raw.Substring(0,256) } else { $raw }
            Write-Host "First 256 chars:"
            Write-Host $snippet
        } catch {
            Write-Host "Failed to read: $_"
        }
    } else {
        Write-Host "Missing: $path"
    }
}

# Inspect key files
Show-FileInfo 'System root LONGER.json' (Join-Path $UserProfile 'AppData\\Roaming\\OrcaSlicer\\system\\LONGER.json')
Show-FileInfo 'System LONGER.json' (Join-Path $sys 'LONGER.json')
Show-FileInfo 'System machine/LONGER LK10.json' (Join-Path $sys 'machine/LONGER LK10.json')
Show-FileInfo 'App machine/LONGER LK10.json' (Join-Path $app 'machine/LONGER LK10.json')
Show-FileInfo 'App LONGER.json' (Join-Path $app '..\LONGER.json')
