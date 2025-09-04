# Export crew_output - Version Simple et Robuste

$SourcePath = "sandbox\crew_output"
$OutputFile = "EXPORT_CREW_OUTPUT_FINAL_$(Get-Date -Format 'yyyyMMdd_HHmmss').md"

if (-not (Test-Path $SourcePath)) {
    Write-Host "Erreur: $SourcePath n'existe pas!" -ForegroundColor Red
    exit 1
}

Write-Host "Export de crew_output..." -ForegroundColor Green

$Header = @"
# EXPORT CREW_OUTPUT

Date: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Source: $SourcePath

---

"@

$Content = $Header

# Obtenir tous les fichiers
$Files = Get-ChildItem -Path $SourcePath -File | Sort-Object Name

$Content += "## Fichiers exportes ($($Files.Count) fichiers):`n`n"

foreach ($File in $Files) {
    $Size = if ($File.Length -lt 1KB) { "$($File.Length) B" } else { "{0:N1} KB" -f ($File.Length / 1KB) }
    $Content += "### $($File.Name) ($Size)`n`n"
    
    try {
        if ($File.Length -gt 0 -and $File.Length -lt 1MB) {
            $FileContent = Get-Content -Path $File.FullName -Raw -Encoding UTF8
            $Content += "````text`n$FileContent`n```````n`n"
        } elseif ($File.Length -eq 0) {
            $Content += "[Fichier vide]`n`n"
        } else {
            $Content += "[Fichier trop volumineux]`n`n"
        }
    }
    catch {
        $Content += "[Erreur de lecture]`n`n"
    }
}

$Footer = @"
---

Export termine: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Genere par LunaCore
"@

$Content += $Footer

# Sauvegarder
try {
    $Content | Out-File -FilePath $OutputFile -Encoding UTF8
    Write-Host "Export cree: $OutputFile" -ForegroundColor Green
}
catch {
    Write-Host "Erreur: $($_.Exception.Message)" -ForegroundColor Red
}
