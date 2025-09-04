# tools/export.ps1 - Generate EXPORT.txt (Windows/PowerShell)
# Stop on error
$ErrorActionPreference = "Stop"

$root    = (Resolve-Path ".").Path
$export  = Join-Path $root "EXPORT.txt"
$summary = "LunaCore is a multi-agent orchestration system using CrewAI. It combines Llama3.1:8b for development with OpenAI GPT-4o-mini for supervision to generate complete software projects through agent collaboration. This file contains all code, configuration and state for a comprehensive audit."
$now     = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"

# Helpers
function Add-Section([string]$title) { Add-Content $export -Encoding utf8 "`n## $title`n" }
function Rel([string]$p) { 
  if ($p.StartsWith($root)) {
    return $p.Substring($root.Length + 1)
  } else {
    return $p
  }
}
$excludeDirs = @(".git",".venv","__pycache__",".mypy_cache",".pytest_cache",".ruff_cache",
                 ".idea",".vscode","node_modules","dist","build",".cache",".coverage",
                 ".ipynb_checkpoints","sandbox",".streamlit","htmlcov")
function Is-Excluded([string]$p){
  foreach($d in $excludeDirs){
    if($p -match ("\\{0}($|\\)" -f [regex]::Escape($d))) { return $true }
  }
  return $false
}

# Initialize EXPORT.txt
Set-Content $export -Encoding utf8 "# EXPORT LunaCore - $now`n$summary`n"

# 1) Useful tree structure with annotations
Add-Section "Project Structure (with key components)"

# Get all files and directories (excluding excluded ones)
$allFiles = Get-ChildItem -LiteralPath $root -Recurse -Force -File | Where-Object { -not (Is-Excluded $_.FullName) }

# Create a simpler tree view with text description
Add-Content $export -Encoding utf8 "LunaCoreMini Project Structure:"
Add-Content $export -Encoding utf8 ""
Add-Content $export -Encoding utf8 "lunacore/ - Core agent system modules"
Add-Content $export -Encoding utf8 "  crew_system.py - CrewAI multi-agent orchestration"
Add-Content $export -Encoding utf8 "  crew_system_simple.py - Simplified agent system"
Add-Content $export -Encoding utf8 "  logger.py - Logging system"
Add-Content $export -Encoding utf8 "  __init__.py"
Add-Content $export -Encoding utf8 ""
Add-Content $export -Encoding utf8 "scripts/ - Utility scripts"
Add-Content $export -Encoding utf8 "  env_check.py"
Add-Content $export -Encoding utf8 "  import_check.py"
Add-Content $export -Encoding utf8 "  run_in_venv.cmd"
Add-Content $export -Encoding utf8 "  run_in_venv.ps1"
Add-Content $export -Encoding utf8 "  test_generate.py"
Add-Content $export -Encoding utf8 ""
Add-Content $export -Encoding utf8 "tools/"
Add-Content $export -Encoding utf8 "  export.ps1 - Script to generate this EXPORT.txt"
Add-Content $export -Encoding utf8 ""
Add-Content $export -Encoding utf8 "Root files:"
Add-Content $export -Encoding utf8 "  .env - Environment config with API keys (masked)"
Add-Content $export -Encoding utf8 "  .env.template - Template for environment setup"
Add-Content $export -Encoding utf8 "  app_crew.py - Main Streamlit interface"
Add-Content $export -Encoding utf8 "  COMMANDES_RAPIDES.txt - Quick commands reference"
Add-Content $export -Encoding utf8 "  LUNACORE_GUIDE.txt - Detailed usage guide"
Add-Content $export -Encoding utf8 "  PROJET_COMPLETE.md - Project completion details"
Add-Content $export -Encoding utf8 "  README.md - Project documentation"
Add-Content $export -Encoding utf8 "  requirements.txt - Dependencies"

# Also add a list of all files for reference
Add-Content $export -Encoding utf8 "`n### Complete file listing:"
$allFiles | ForEach-Object { 
    $relPath = $_.FullName.Substring($root.Length + 1)
    Add-Content $export -Encoding utf8 "- $relPath" 
}

# 2) Python Code (.py)
Add-Section "Python Code (.py)"
$pyFiles = Get-ChildItem -Recurse -Include *.py -File | Where-Object { -not (Is-Excluded $_.FullName) }
foreach($f in $pyFiles){
  Add-Content $export -Encoding utf8 "`n=== $(Rel $f.FullName) ==="
  Get-Content $f.FullName -Raw | Add-Content $export -Encoding utf8
}

# 3) Versions & dependencies
Add-Section "Versions & dependencies"
$pyExe  = Join-Path $root ".venv\Scripts\python.exe"
$pipExe = Join-Path $root ".venv\Scripts\pip.exe"
if(Test-Path $pyExe){ 
  Add-Content $export -Encoding utf8 "### Python version"
  & $pyExe --version 2>&1 | Out-String | Add-Content $export -Encoding utf8
} else { 
  Add-Content $export -Encoding utf8 "WARNING: Not found: .venv\Scripts\python.exe" 
}

if(Test-Path $pipExe){
  Add-Content $export -Encoding utf8 "`n### pip freeze"
  & $pipExe freeze 2>&1 | Out-String | Add-Content $export -Encoding utf8

  Add-Content $export -Encoding utf8 "`n### Key packages (pip show)"
  $pkgs = @("crewai","langchain","streamlit","openai","httpx","pydantic","fastapi","uvicorn")
  foreach($p in $pkgs){
    try { 
      Add-Content $export -Encoding utf8 "--- $p ---"
      & $pipExe show $p 2>&1 | Out-String | Add-Content $export -Encoding utf8
    } catch {
      Add-Content $export -Encoding utf8 "WARNING: Not found: $p"
    }
  }
} else {
  Add-Content $export -Encoding utf8 "WARNING: Not found: .venv\Scripts\pip.exe"
}

Add-Content $export -Encoding utf8 "`n### ollama version"
try { 
  $ollamaVersion = & ollama --version 2>&1 | Out-String
  Add-Content $export -Encoding utf8 $ollamaVersion
  
  # Check for installed Llama model
  Add-Content $export -Encoding utf8 "`n### Ollama installed models"
  try {
    $ollamaModels = & ollama list 2>&1 | Out-String
    Add-Content $export -Encoding utf8 $ollamaModels
    
    # Check if Llama3.1:8b is specifically installed
    if ($ollamaModels -match "llama3.1:8b") {
      Add-Content $export -Encoding utf8 "`nCONFIRMED: Llama3.1:8b is installed in Ollama"
    } else {
      Add-Content $export -Encoding utf8 "`nWARNING: Llama3.1:8b was not found in Ollama models list"
    }
  } catch {
    Add-Content $export -Encoding utf8 "WARNING: Could not retrieve Ollama models list"
  }
} catch { 
  Add-Content $export -Encoding utf8 "WARNING: Not found: ollama" 
}

# 4) Dependency files (requirements/pyproject)
Add-Section "Dependency files (requirements / pyproject)"
$depFiles = @(Get-ChildItem -Recurse -Include requirements*.txt,pyproject.toml,poetry.lock -File | Where-Object { -not (Is-Excluded $_.FullName) })
if($depFiles.Count -eq 0){ 
  Add-Content $export -Encoding utf8 "WARNING: Not found: requirements*.txt / pyproject.toml / poetry.lock" 
}
foreach($f in $depFiles){
  Add-Content $export -Encoding utf8 "`n=== $(Rel $f.FullName) ==="
  Get-Content $f.FullName -Raw | Add-Content $export -Encoding utf8
}

# 5) Critical config
Add-Section "Critical config"
# .env (masked)
$envPath = Join-Path $root ".env"
if(Test-Path $envPath){
  Add-Content $export -Encoding utf8 "`n=== .env (masked) ==="
  $maskKeywords = "KEY|TOKEN|SECRET|PASSWORD|PWD|ACCESS|PRIVATE|CERT|API|CLIENT_SECRET|AUTH|HMAC|JWT"
  Get-Content $envPath | ForEach-Object {
    if($_ -match "^\s*#"){ 
      $_ 
    }
    elseif($_ -match "^\s*([^=]+)\s*=\s*(.*)"){
      $k = $Matches[1]; $v = $Matches[2]
      if($k -match $maskKeywords -or $v -match $maskKeywords){ "$k=[SECRET MASKED]" } else { "$k=$v" }
    } else { 
      $_ 
    }
  } | Add-Content $export -Encoding utf8
}else{
  Add-Content $export -Encoding utf8 "WARNING: Not found: .env"
}
# Other critical files - ensuring encoding is correct
$critGlobs = @("README.md","LUNACORE_GUIDE.txt","PROJET_COMPLETE.md",
               "agents.yaml","tasks.yaml","config.yaml",".env.template",
               "streamlit_app.py","app.py","tests\*.py")
foreach($g in $critGlobs){
  $files = @(Get-ChildItem -Recurse -File -Include $g | Where-Object { -not (Is-Excluded $_.FullName) })
  if($files.Count -eq 0){ 
    Add-Content $export -Encoding utf8 "WARNING: Not found: $g" 
  }
  foreach($f in $files){
    Add-Content $export -Encoding utf8 "`n=== $(Rel $f.FullName) ==="
    # Read with UTF-8 encoding and write with UTF-8 encoding to prevent character issues
    try {
      $content = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)
      Add-Content $export -Encoding utf8 $content
    }
    catch {
      # Fallback to Get-Content if the above method fails
      Get-Content $f.FullName -Raw -Encoding utf8 | Add-Content $export -Encoding utf8
    }
  }
}

# 6) Logs
Add-Section "Logs"
$logs = @(Get-ChildItem -Recurse -File -Include *.log,log.txt,output.txt | Where-Object { -not (Is-Excluded $_.FullName) })
if($logs.Count -eq 0){ 
  Add-Content $export -Encoding utf8 "WARNING: Not found: logs" 
}
foreach($f in $logs){
  Add-Content $export -Encoding utf8 "`n=== $(Rel $f.FullName) ==="
  Get-Content $f.FullName -Raw | Add-Content $export -Encoding utf8
}

# Add key files explanation section
Add-Section "Key Files Overview"
Add-Content $export -Encoding utf8 @"
LunaCoreMini is built around several critical components that work together:

1. **lunacore/crew_system.py**
   - Core orchestration system using CrewAI framework
   - Implements multi-agent architecture with Llama3.1:8b and OpenAI GPT-4
   - Manages delegation, project folder creation, and file generation
   - Contains tools for agent collaboration and fallback mechanisms

2. **lunacore/crew_system_simple.py**
   - Simplified version of the agent system for debugging
   - Provides basic functionality without complex delegation
   - Useful when the main system encounters issues

3. **lunacore/logger.py**
   - Custom logging system with memory and file-based logs
   - Supports different log levels (info, warning, error, success)
   - Provides structured logs for the UI

4. **app_crew.py**
   - Streamlit user interface for the LunaCore system
   - Provides project creation, template selection, and output viewing
   - Includes real-time logging and project download features

5. **.env / .env.template**
   - Configuration for API keys and service endpoints
   - Contains settings for OpenAI, Ollama, and other services

6. **scripts/**
   - Utility scripts for environment setup and testing
   - Contains helpers for virtual environment activation

7. **requirements.txt**
   - Lists all dependencies with specific versions
   - Includes CrewAI, LangChain, Streamlit, and other libraries
"@

Add-Content $export -Encoding utf8 "`n## LLM Models Configuration"
Add-Content $export -Encoding utf8 @"
LunaCoreMini uses the following LLM models:

- **Llama3.1:8b** (via Ollama): Used for code generation and implementation tasks
- **OpenAI GPT-4o-mini**: Used for supervision, architecture design, and task orchestration

The system is designed to work primarily with local models via Ollama for development tasks,
while using OpenAI models sparingly for higher-level oversight and coordination.
"@

Add-Content $export -Encoding utf8 "`n-- END OF EXPORT --"
Write-Host "OK -> $export"
