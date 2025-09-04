<#
run_in_venv.ps1 - Minimal helper to create/activate workspace .venv and run a command

Usage:
  # Run a command with the workspace .venv activated (does NOT create .venv)
  .\scripts\run_in_venv.ps1 -- python -V

  # Create .venv if it does not exist, then run the command
  .\scripts\run_in_venv.ps1 -Create -- python -V
#>

# Manual argument parsing to avoid PowerShell parameter binding issues when invoked
# as: powershell -File scripts\run_in_venv.ps1 -Create -- some command

function Write-Info { param([string]$m) Write-Host "[venv-helper] $m" -ForegroundColor Cyan }
function Write-ErrorAndExit { param([string]$m) Write-Host "[venv-helper] $m" -ForegroundColor Red; exit 1 }

# Parse $args to detect -Create and the command to run. We accept -Create (case-insensitive).
$createFlag = $false
$cmdArgs = @()
foreach ($a in $args) {
    if ($a -match '^(--|-){1,2}create$') { $createFlag = $true; continue }
    if ($a -eq '--') { continue }
    $cmdArgs += $a
}

$cwd = (Get-Location).Path
$venvActivate = Join-Path $cwd ".venv\Scripts\Activate.ps1"

if (-not (Test-Path $venvActivate)) {
    if ($createFlag) {
        Write-Info ".venv not found - creating with: python -m venv .venv"
        $py = Get-Command python -ErrorAction SilentlyContinue
        if (-not $py) { Write-ErrorAndExit "Python executable not found in PATH. Install Python or create .venv manually." }
        & python -m venv .venv
        if (-not (Test-Path $venvActivate)) { Write-ErrorAndExit "Failed to create .venv. Check that Python can create virtual environments." }
    } else {
        Write-Info ".venv not found in workspace. To create it automatically, run with -Create." 
        exit 0
    }
}

# Activate the virtual environment in this script scope
. $venvActivate
Write-Info ".venv activated"

if ($cmdArgs.Count -gt 0) {
    $cmd = $cmdArgs -join ' '
    Write-Info "Executing: $cmd"
    try {
        Invoke-Expression $cmd
    } catch {
        Write-ErrorAndExit "Command failed: $($_.Exception.Message)"
    }
} else {
    Write-Info "No command provided. .venv is activated in this script scope. To run a command, pass it after --"
}

exit 0
