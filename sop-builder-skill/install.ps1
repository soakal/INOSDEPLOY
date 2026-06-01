<#
.SYNOPSIS
    Install the SOP Builder skill into your Cowork user-skills folder.

.DESCRIPTION
    Copies SKILL.md and example_builder.py from this folder into the
    persistent user-skills location so Cowork loads the skill on every session.

    Tries the most common locations in order. If none exist, prints
    instructions for manual placement.

.EXAMPLE
    PS> cd "C:\Users\Deploy\Desktop\SOP Factory\sop-builder-skill"
    PS> .\install.ps1
#>
[CmdletBinding()]
param(
    [string]$Source = $PSScriptRoot
)

$ErrorActionPreference = 'Stop'

# Candidate persistent skill folders, in priority order
$candidates = @(
    "$env:USERPROFILE\.claude\skills",
    "$env:APPDATA\Claude\skills",
    "$env:USERPROFILE\Documents\Claude\skills"
)

$target = $null
foreach ($c in $candidates) {
    $parent = Split-Path $c -Parent
    if (Test-Path -LiteralPath $parent) {
        if (-not (Test-Path -LiteralPath $c)) {
            New-Item -ItemType Directory -Path $c -Force | Out-Null
        }
        $target = $c
        break
    }
}

if (-not $target) {
    Write-Host "Could not find a persistent skills folder. Manual install:" -ForegroundColor Yellow
    Write-Host "  1. Find your Cowork user-skills folder (Settings → Skills should show the path)" -ForegroundColor Yellow
    Write-Host "  2. Create a 'sop-builder' subfolder inside it" -ForegroundColor Yellow
    Write-Host "  3. Copy SKILL.md and example_builder.py from this folder into it" -ForegroundColor Yellow
    Write-Host "  4. Restart Cowork" -ForegroundColor Yellow
    exit 1
}

$dest = Join-Path $target "sop-builder"
Write-Host "Installing to: $dest" -ForegroundColor Cyan

if (Test-Path -LiteralPath $dest) {
    Write-Host "  (folder exists — overwriting)" -ForegroundColor DarkGray
}
New-Item -ItemType Directory -Path $dest -Force | Out-Null

Copy-Item -LiteralPath (Join-Path $Source 'SKILL.md')          -Destination $dest -Force
Copy-Item -LiteralPath (Join-Path $Source 'example_builder.py') -Destination $dest -Force

Write-Host "Installed:" -ForegroundColor Green
Get-ChildItem -LiteralPath $dest | ForEach-Object {
    Write-Host "  $($_.Name)  ($('{0:N0}' -f $_.Length) bytes)" -ForegroundColor Yellow
}
Write-Host ""
Write-Host "Restart Cowork (or start a new conversation) to pick up the new skill." -ForegroundColor Cyan
Write-Host "Then say `"build the SOP`" or `"create an SOP`" to invoke it." -ForegroundColor Cyan
