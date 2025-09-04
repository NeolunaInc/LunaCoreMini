@echo off
REM Wrapper to call the PowerShell helper and forward all args, avoiding -File parsing issues.
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0run_in_venv.ps1" %*
endlocal
