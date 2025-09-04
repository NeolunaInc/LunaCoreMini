# Générateur de tree ASCII beautifié pour LunaCore
param(
    [string]$RootPath = ".",
    [switch]$OnlyImportant = $true
)

$excludeDirs = @(".git", ".venv", "__pycache__", ".mypy_cache", ".pytest_cache", 
                 ".ruff_cache", ".idea", ".vscode", "node_modules", "dist", 
                 "build", ".cache", ".coverage", ".ipynb_checkpoints", 
                 ".streamlit", "htmlcov")

$importantExtensions = @(".py", ".md", ".txt", ".yml", ".yaml", ".json", 
                        ".ps1", ".cmd", ".sh", ".toml", ".cfg", ".ini", ".env")

function Is-Excluded {
    param($Path)
    foreach ($exclude in $excludeDirs) {
        if ($Path -like "*\$exclude" -or $Path -like "*\$exclude\*") {
            return $true
        }
    }
    return $false
}

function Is-Important {
    param($File)
    if ($File.PSIsContainer) { return $true }
    
    $ext = $File.Extension.ToLower()
    if ($ext -in $importantExtensions) { return $true }
    
    # Fichiers sans extension mais importants
    $name = $File.Name.ToLower()
    if ($name -in @("dockerfile", "makefile", "requirements", "readme", "license", "gitignore")) {
        return $true
    }
    
    return $false
}

function Get-FileIcon {
    param($File)
    if ($File.PSIsContainer) { return "[DIR]" }
    
    switch ($File.Extension.ToLower()) {
        ".py" { return "[PY] " }
        ".md" { return "[MD] " }
        ".txt" { return "[TXT]" }
        ".json" { return "[JSON]" }
        ".yml" { return "[YML]" }
        ".yaml" { return "[YAML]" }
        ".ps1" { return "[PS1]" }
        ".cmd" { return "[CMD]" }
        ".sh" { return "[SH] " }
        ".env" { return "[ENV]" }
        ".toml" { return "[TOML]" }
        default { return "[FILE]" }
    }
}

function Get-FileDescription {
    param($File, $RelativePath)
    
    if ($File.PSIsContainer) { return "" }
    
    # Descriptions spécifiques basées sur le nom et chemin
    switch -Regex ($RelativePath) {
        "crew_system\.py$" { return "# Core multi-agent orchestration system" }
        "crew_system_simple\.py$" { return "# Simplified agent system for debugging" }
        "llm_orchestrator\.py$" { return "# LLM routing and complexity analysis" }
        "tools_runtime\.py$" { return "# Runtime tools with ACL and role binding" }
        "logger\.py$" { return "# Advanced logging system" }
        "error_handler\.py$" { return "# Error handling and retry mechanisms" }
        "app_crew\.py$" { return "# Main Streamlit interface" }
        "requirements\.txt$" { return "# Python dependencies" }
        "README\.md$" { return "# Project documentation" }
        "\.env$" { return "# Environment configuration (API keys)" }
        "test_.*\.py$" { return "# Test script" }
        "export.*\.ps1$" { return "# Export utility script" }
        default { return "" }
    }
}

function Build-Tree {
    param($Path, $Prefix = "", $IsLast = $true, $Level = 0)
    
    if ($Level -gt 10) { return "" }  # Éviter la récursion infinie
    
    $items = Get-ChildItem -Path $Path -Force | Where-Object { 
        -not (Is-Excluded $_.FullName) -and 
        ($OnlyImportant -eq $false -or (Is-Important $_))
    } | Sort-Object { $_.PSIsContainer }, Name
    
    $result = ""
    
    for ($i = 0; $i -lt $items.Count; $i++) {
        $item = $items[$i]
        $isLastItem = ($i -eq ($items.Count - 1))
        
        $connector = if ($isLastItem) { "+-- " } else { "|-- " }
        $icon = Get-FileIcon $item
        
        $relativePath = $item.FullName.Replace("$((Get-Location).Path)\", "")
        $description = Get-FileDescription $item $relativePath
        
        $displayName = "$icon $($item.Name)"
        if ($description) {
            $displayName += " $description"
        }
        
        $result += "$Prefix$connector$displayName`n"
        
        if ($item.PSIsContainer) {
            $newPrefix = if ($isLastItem) { "$Prefix    " } else { "$Prefix|   " }
            $result += Build-Tree -Path $item.FullName -Prefix $newPrefix -IsLast $isLastItem -Level ($Level + 1)
        }
    }
    
    return $result
}

# Générer le tree
Write-Host "Génération du tree beautifié..." -ForegroundColor Green

$treeContent = @"
## Structure Complete du Projet (Fichiers Importants)

```
[DIR] LunaCoreMini_v2/
$(Build-Tree -Path $RootPath)```

### Legende des Types :
- [PY]   Fichiers Python (.py)
- [MD]   Documentation Markdown (.md)  
- [TXT]  Fichiers texte (.txt)
- [JSON] Configuration JSON (.json)
- [YML]  Configuration YAML (.yml/.yaml/.toml)
- [PS1]  Scripts PowerShell (.ps1)
- [CMD]  Scripts Batch (.cmd)
- [ENV]  Fichiers d'environnement (.env)
- [DIR]  Dossiers

### Modules Python Principaux :
- **crew_system.py** : Orchestration multi-agents avec CrewAI
- **llm_orchestrator.py** : Routage intelligent LLM (Llama/OpenAI)
- **tools_runtime.py** : Outils runtime avec ACL et binding de roles
- **logger.py** : Systeme de logs avance avec tracking d'agents
- **error_handler.py** : Gestion robuste des erreurs et retry

### Configuration Systeme :
- **.env** : Cles API et configuration LLM
- **requirements.txt** : Dependances Python completes
- **app_crew.py** : Interface Streamlit principale

"@

Write-Output $treeContent

Write-Host "Tree généré avec succès !" -ForegroundColor Green
