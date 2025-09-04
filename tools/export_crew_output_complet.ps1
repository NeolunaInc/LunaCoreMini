#!/usr/bin/env powershell

# Script d'export crew_output avec métadonnées complètes
param(
    [string]$OutputFile = "EXPORT_CREW_OUTPUT_COMPLET_$(Get-Date -Format 'yyyyMMdd_HHmmss').md"
)

$SourcePath = "sandbox\crew_output"

if (-not (Test-Path $SourcePath)) {
    Write-Host "Erreur: $SourcePath n'existe pas!" -ForegroundColor Red
    exit 1
}

Write-Host "Export complet de crew_output..." -ForegroundColor Green

# En-tête
$Content = @"
# 📦 EXPORT COMPLET CREW_OUTPUT

**Date d'export**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
**Source**: $SourcePath
**Système**: $env:COMPUTERNAME

---

## 📊 Statistiques

"@

# Statistiques
$Files = Get-ChildItem -Path $SourcePath -Recurse -File
$TotalFiles = $Files.Count
$TotalSize = ($Files | Measure-Object Length -Sum).Sum
$TotalSizeFormatted = if ($TotalSize -lt 1KB) { "$TotalSize B" } elseif ($TotalSize -lt 1MB) { "{0:N1} KB" -f ($TotalSize / 1KB) } else { "{0:N1} MB" -f ($TotalSize / 1MB) }

$Content += @"
- **Nombre de fichiers**: $TotalFiles
- **Taille totale**: $TotalSizeFormatted
- **Types de fichiers**: $($Files | Group-Object Extension | ForEach-Object { "$($_.Name) ($($_.Count))" } | Join-String -Separator ", ")

---

## 🌳 Structure

"@

# Structure arborescente simple
$Items = Get-ChildItem -Path $SourcePath -Recurse | Sort-Object FullName
foreach ($Item in $Items) {
    $RelPath = $Item.FullName.Replace("$PWD\$SourcePath\", "")
    $Indent = "  " * (($RelPath.Split('\').Count - 1))
    if ($Item.PSIsContainer) {
        $Content += "$Indent📁 $($Item.Name)/`n"
    } else {
        $Size = if ($Item.Length -lt 1KB) { "$($Item.Length)B" } else { "{0:N0}KB" -f ($Item.Length / 1KB) }
        $Content += "$Indent📄 $($Item.Name) ($Size)`n"
    }
}

$Content += @"

---

## 📋 Liste des Fichiers

| Nom | Taille | Date Modif | Extension |
|-----|--------|------------|-----------|
"@

foreach ($File in ($Files | Sort-Object Name)) {
    $Size = if ($File.Length -lt 1KB) { "$($File.Length) B" } else { "{0:N1} KB" -f ($File.Length / 1KB) }
    $Date = $File.LastWriteTime.ToString("yyyy-MM-dd HH:mm")
    $Content += "`n| $($File.Name) | $Size | $Date | $($File.Extension) |"
}

$Content += @"


---

## 📄 Contenu des Fichiers

"@

# Contenu des fichiers
foreach ($File in ($Files | Sort-Object Name)) {
    $Size = if ($File.Length -lt 1KB) { "$($File.Length) B" } else { "{0:N1} KB" -f ($File.Length / 1KB) }
    
    $Content += @"

### 📄 $($File.Name)

**Métadonnées:**
- Taille: $Size
- Dernière modification: $($File.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss"))
- Chemin: $($File.FullName.Replace($PWD, '.'))

**Contenu:**

"@

    # Déterminer le type pour la coloration syntaxique
    $Language = switch ($File.Extension.ToLower()) {
        ".py" { "python" }
        ".md" { "markdown" }
        ".txt" { "text" }
        ".json" { "json" }
        ".yml" { "yaml" }
        ".yaml" { "yaml" }
        default { "text" }
    }
    
    try {
        if ($File.Length -lt 5MB -and $File.Length -gt 0) {
            $FileContent = Get-Content -Path $File.FullName -Raw -Encoding UTF8
            $Content += "````$Language`n$FileContent`n````"
        } elseif ($File.Length -eq 0) {
            $Content += "*[Fichier vide]*"
        } else {
            $Content += "*[Fichier trop volumineux: $Size]*"
        }
    }
    catch {
        $Content += "*[Erreur de lecture: $($_.Exception.Message)]*"
    }
    
    $Content += "`n"
}

# Footer
$Content += @"

---

## 📈 Résumé Final

- ✅ Export terminé avec succès
- 📁 $TotalFiles fichiers exportés
- 💾 Taille totale: $TotalSizeFormatted
- 🕒 Durée: Quelques secondes
- 📅 Date: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

*Généré automatiquement par LunaCore*
"@

# Sauvegarder
try {
    $Content | Out-File -FilePath $OutputFile -Encoding UTF8 -Force
    Write-Host "✅ Export créé: $OutputFile" -ForegroundColor Green
    Write-Host "📊 $TotalFiles fichiers exportés ($TotalSizeFormatted)" -ForegroundColor Cyan
}
catch {
    Write-Host "❌ Erreur: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
