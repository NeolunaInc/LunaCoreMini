#!/usr/bin/env powershell
<#
.SYNOPSIS
    Export complet du contenu de crew_output
    
.DESCRIPTION
    Exporte tous les fichiers et dossiers du répertoire crew_output
    avec leur contenu, structure et métadonnées
    
.AUTHOR
    LunaCore System
    
.DATE
    $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
#>

# Configuration
$SourcePath = "sandbox\crew_output"
$ExportFile = "EXPORT_CREW_OUTPUT_$(Get-Date -Format 'yyyyMMdd_HHmmss').md"
$FullSourcePath = Join-Path $PWD $SourcePath

Write-Host "🚀 Export du contenu de crew_output" -ForegroundColor Green
Write-Host "📂 Source: $FullSourcePath" -ForegroundColor Cyan
Write-Host "📄 Export: $ExportFile" -ForegroundColor Cyan

# Vérifier que le dossier existe
if (-not (Test-Path $FullSourcePath)) {
    Write-Host "❌ Erreur: Le dossier $SourcePath n'existe pas!" -ForegroundColor Red
    exit 1
}

# Initialiser le fichier d'export
$ExportContent = @"
# 📦 EXPORT CREW_OUTPUT - $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

## 📋 Informations Generales
- **Source**: $SourcePath
- **Date d'export**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
- **Systeme**: $env:COMPUTERNAME
- **Utilisateur**: $env:USERNAME

---

"@

# Fonction pour obtenir la structure arborescente
function Get-TreeStructure {
    param($Path, $Prefix = "")
    
    $Items = Get-ChildItem -Path $Path | Sort-Object Name
    $Structure = ""
    
    for ($i = 0; $i -lt $Items.Count; $i++) {
        $Item = $Items[$i]
        $IsLast = ($i -eq ($Items.Count - 1))
        
        if ($IsLast) {
            $Structure += "$Prefix└── $($Item.Name)`n"
            $NewPrefix = "$Prefix    "
        } else {
            $Structure += "$Prefix├── $($Item.Name)`n"
            $NewPrefix = "$Prefix│   "
        }
        
        if ($Item.PSIsContainer) {
            $Structure += Get-TreeStructure -Path $Item.FullName -Prefix $NewPrefix
        }
    }
    
    return $Structure
}

# Générer la structure arborescente
Write-Host "📊 Génération de la structure arborescente..." -ForegroundColor Yellow
$TreeStructure = Get-TreeStructure -Path $FullSourcePath

$ExportContent += @"
## 🌳 Structure Arborescente

``````
crew_output/
$TreeStructure``````

---

"@

# Fonction pour obtenir les métadonnées d'un fichier
function Get-FileMetadata {
    param($FilePath)
    
    $File = Get-Item $FilePath
    $Extension = $File.Extension
    $Size = $File.Length
    $LastWrite = $File.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss")
    
    return @{
        Extension = $Extension
        Size = $Size
        LastWrite = $LastWrite
        SizeFormatted = if ($Size -lt 1KB) { "$Size B" } 
                       elseif ($Size -lt 1MB) { "{0:N1} KB" -f ($Size / 1KB) }
                       else { "{0:N1} MB" -f ($Size / 1MB) }
    }
}

# Obtenir tous les fichiers
Write-Host "📁 Analyse des fichiers..." -ForegroundColor Yellow
$AllFiles = Get-ChildItem -Path $FullSourcePath -Recurse -File | Sort-Object FullName

# Générer le rapport des fichiers
$ExportContent += @"
## 📊 Rapport des Fichiers

| Fichier | Taille | Derniere Modification | Type |
|---------|--------|---------------------|------|
"@

foreach ($File in $AllFiles) {
    $RelativePath = $File.FullName.Replace($FullSourcePath, "").TrimStart('\')
    $Metadata = Get-FileMetadata -FilePath $File.FullName
    
    $ExportContent += "`n| $RelativePath | $($Metadata.SizeFormatted) | $($Metadata.LastWrite) | $($Metadata.Extension) |"
}

$ExportContent += @"


---

## 📄 Contenu des Fichiers

"@

# Exporter le contenu de chaque fichier
Write-Host "📝 Export du contenu des fichiers..." -ForegroundColor Yellow

foreach ($File in $AllFiles) {
    $RelativePath = $File.FullName.Replace($FullSourcePath, "").TrimStart('\')
    $Metadata = Get-FileMetadata -FilePath $File.FullName
    
    Write-Host "   📄 $RelativePath ($($Metadata.SizeFormatted))" -ForegroundColor Gray
    
    $ExportContent += @"

### 📄 $RelativePath

**Metadonnees:**
- **Taille**: $($Metadata.SizeFormatted)
- **Derniere modification**: $($Metadata.LastWrite)
- **Extension**: $($Metadata.Extension)

**Contenu:**

"@

    try {
        # Déterminer le type de fichier pour la coloration syntaxique
        $Language = switch ($Metadata.Extension.ToLower()) {
            ".py" { "python" }
            ".js" { "javascript" }
            ".ts" { "typescript" }
            ".md" { "markdown" }
            ".json" { "json" }
            ".yml" { "yaml" }
            ".yaml" { "yaml" }
            ".xml" { "xml" }
            ".html" { "html" }
            ".css" { "css" }
            ".txt" { "text" }
            default { "text" }
        }
        
        # Lire le contenu du fichier
        if ($File.Length -lt 10MB) {  # Limiter pour eviter les fichiers trop volumineux
            $Content = Get-Content -Path $File.FullName -Raw -Encoding UTF8
            $ExportContent += "````$Language`n$Content`n````n"
        } else {
            $ExportContent += "*[Fichier trop volumineux pour etre affiche ($($Metadata.SizeFormatted))]*`n"
        }
    }
    catch {
        $ExportContent += "*[Erreur lors de la lecture du fichier: $($_.Exception.Message)]*`n"
    }
    
    $ExportContent += "`n---`n"
}

# Ajouter un résumé final
$TotalFiles = $AllFiles.Count
$TotalSize = ($AllFiles | Measure-Object Length -Sum).Sum
$TotalSizeFormatted = if ($TotalSize -lt 1KB) { "$TotalSize B" } 
                     elseif ($TotalSize -lt 1MB) { "{0:N1} KB" -f ($TotalSize / 1KB) }
                     else { "{0:N1} MB" -f ($TotalSize / 1MB) }

$ExportContent += @"

## 📈 Résumé de l'Export

- **Nombre total de fichiers**: $TotalFiles
- **Taille totale**: $TotalSizeFormatted
- **Date d'export**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
- **Durée d'export**: Terminé avec succès

---

*Export généré automatiquement par LunaCore System*
"@

# Sauvegarder le fichier d'export
Write-Host "💾 Sauvegarde de l'export..." -ForegroundColor Yellow
try {
    $ExportContent | Out-File -FilePath $ExportFile -Encoding UTF8
    Write-Host "✅ Export terminé avec succès!" -ForegroundColor Green
    Write-Host "📄 Fichier créé: $ExportFile" -ForegroundColor Cyan
    Write-Host "📊 $TotalFiles fichiers exportés ($TotalSizeFormatted)" -ForegroundColor Cyan
}
catch {
    Write-Host "❌ Erreur lors de la sauvegarde: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Proposer d'ouvrir le fichier
$OpenFile = Read-Host "`n🔍 Voulez-vous ouvrir le fichier d'export? (o/N)"
if ($OpenFile -eq "o" -or $OpenFile -eq "O" -or $OpenFile -eq "oui") {
    Start-Process $ExportFile
}

Write-Host "`n🎉 Export crew_output terminé!" -ForegroundColor Green
