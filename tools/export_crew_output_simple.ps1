#!/usr/bin/env powershell
<#
.SYNOPSIS
    Export rapide de crew_output
#>

param(
    [string]$OutputFile = "EXPORT_CREW_OUTPUT_$(Get-Date -Format 'yyyyMMdd_HHmmss').md"
)

$SourcePath = "sandbox\crew_output"

if (-not (Test-Path $SourcePath)) {
    Write-Host "❌ Erreur: $SourcePath n'existe pas!" -ForegroundColor Red
    exit 1
}

Write-Host "🚀 Export rapide de crew_output..." -ForegroundColor Green

$Content = @"
# 📦 EXPORT CREW_OUTPUT - $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

## 📁 Fichiers dans crew_output:

"@

$Files = Get-ChildItem -Path $SourcePath -Recurse -File | Sort-Object Name

foreach ($File in $Files) {
    $RelativePath = $File.Name
    $Size = if ($File.Length -lt 1KB) { "$($File.Length) B" } else { "{0:N1} KB" -f ($File.Length / 1KB) }
    
    $Content += @"

### 📄 $RelativePath ($Size)

``````
$(Get-Content -Path $File.FullName -Raw -Encoding UTF8)
``````

"@
}

$Content | Out-File -FilePath $OutputFile -Encoding UTF8
Write-Host "✅ Export créé: $OutputFile" -ForegroundColor Green
