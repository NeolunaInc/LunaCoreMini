# 🤖 LunaCore CrewAI - Système Multi-Agents de Génération de Code

[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![CrewAI](https://img.shields.io/badge/CrewAI-0.175.0-green.svg)](https://docs.crewai.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**LunaCore** est un système révolutionnaire de génération de code utilisant une équipe d'agents IA spécialisés. Llama3.1:8b développe, OpenAI GPT-4 supervise, et ensemble ils créent des applications complètes et fonctionnelles.

## ✨ Fonctionnalités Principales

### 🧠 **Intelligence Multi-Agents**
- **Architecture hiérarchique** avec coordination intelligente
- **5 agents spécialisés** : Superviseur, Développeur, Backend, Testeur, Documentaliste
- **Collaboration dynamique** entre les agents pour des résultats optimaux

### 💻 **Génération de Code Avancée**
- **Llama3.1:8b** comme développeur principal (code tout le projet)
- **OpenAI GPT-4** comme architecte superviseur (guidance stratégique)
- **Code prêt à l'emploi** avec structure professionnelle
- **Support multi-frameworks** (FastAPI, Streamlit, Flask, CLI, Libraries)

### 🎯 **Interface Utilisateur Intuitive**
- **Interface Streamlit moderne** avec feedback en temps réel
- **Templates rapides** pour démarrer instantanément
- **Logs des agents** pour suivre le processus de création
- **Téléchargement direct** des projets générés

### 🚀 **Projets Complets Générés**
- **Code source complet** structuré et documenté
- **Tests automatiques** avec pytest
- **Documentation complète** (README, docstrings)
- **Fichiers de configuration** (requirements.txt, .env templates)

## 🚀 Installation et Démarrage

### Prérequis
- **Python 3.13+** installé sur votre système
- **Ollama** avec le modèle Llama3.1:8b
- **Clé API OpenAI** pour le superviseur
- **Git** pour la gestion de version (optionnel)

### Installation d'Ollama
```bash
# 1. Télécharger Ollama depuis https://ollama.ai/download
# 2. Installer le modèle Llama3.1:8b
ollama pull llama3.1:8b

# 3. Vérifier l'installation
ollama list
```

### Activation rapide (Windows PowerShell)

Un helper PowerShell est fourni pour activer la `.venv` et exécuter des commandes avec l'environnement virtuel :

```powershell
# Crée .venv si nécessaire et lance Streamlit
.\scripts\run_in_venv.ps1 -Create -- streamlit run app_crew.py

# Lance Streamlit si .venv existe déjà
.\scripts\run_in_venv.ps1 -- streamlit run app_crew.py
```

### Configuration du Projet
```bash
# 1. Cloner le repository
git clone https://github.com/NeolunaInc/LunaCoreMini.git
cd LunaCoreMini

# 2. Créer l'environnement virtuel
python -m venv .venv

# 3. Activer l'environnement (Windows)
.venv\Scripts\Activate

# 4. Activer l'environnement (Linux/Mac)
source .venv/bin/activate

# 5. Installer les dépendances
pip install -r requirements.txt
```

### Configuration des Variables d'Environnement
Créer un fichier `.env` à la racine du projet :
```env
# Clé API OpenAI (obligatoire)
OPENAI_API_KEY=votre_clé_openai_ici

# Configuration Ollama (optionnel, par défaut localhost:11434)
OLLAMA_HOST=http://localhost:11434
```

### Lancement de l'Application
```bash
# Méthode recommandée (utilise le Python de l'environnement virtuel)
.venv\Scripts\python.exe -m streamlit run app_crew.py

# Méthode alternative (si PATH configuré)
streamlit run app_crew.py

# Avec port personnalisé
streamlit run app_crew.py --server.port 8502
```

L'application sera accessible sur : **http://localhost:8501**

## 🏗️ Architecture du Système

```
LunaCoreMini_v2/
├── 📁 .venv/                      # Environnement virtuel Python
├── 📄 .env                        # Variables d'environnement (clés API)
├── 📄 .gitignore                  # Fichiers ignorés par Git
├── 🚀 app_crew.py                 # Interface Streamlit principale
├── 📋 requirements.txt            # Dépendances Python
├── 📖 README.md                   # Documentation principale
├── 📝 LUNACORE_GUIDE.txt         # Guide complet d'utilisation
│
├── 📁 lunacore/                   # Package principal LunaCore
│   ├── 📄 __init__.py
│   └── 🤖 crew_system.py         # Système multi-agents CrewAI
│
└── 📁 sandbox/
    └── 📁 crew_output/           # Projets générés par les agents
        ├── main.py               # Code principal généré
        ├── requirements.txt      # Dépendances du projet
        ├── README.md            # Documentation générée
        └── tests/               # Tests automatiques
```

## 🤖 Équipe d'Agents Spécialisés

### 🧠 **Superviseur Architecte** (OpenAI GPT-4)
- **Rôle** : Conception d'architecture et déblocage
- **Responsabilités** :
  - Analyse du brief et planification
  - Guidance stratégique des autres agents
  - Résolution de problèmes complexes
  - Ne code pas, guide uniquement

### 💻 **Développeur Principal** (Llama3.1:8b)
- **Rôle** : Implémentation complète du code
- **Responsabilités** :
  - Écriture de tout le code source
  - Structure et organisation du projet
  - Implémentation des fonctionnalités principales
  - Gestion des dépendances

### 🔧 **Développeur Backend** (Llama3.1:8b)
- **Rôle** : Spécialiste des composants serveur
- **Responsabilités** :
  - APIs REST et endpoints
  - Gestion des bases de données
  - Authentification et sécurité
  - Services et middleware

### 🧪 **Ingénieur QA** (Llama3.1:8b)
- **Rôle** : Tests et validation
- **Responsabilités** :
  - Tests unitaires avec pytest
  - Tests d'intégration
  - Fixtures et mocks
  - Validation du code

### 📚 **Rédacteur Technique** (Llama3.1:8b)
- **Rôle** : Documentation complète
- **Responsabilités** :
  - README détaillés
  - Docstrings dans le code
  - Guides d'utilisation
  - Exemples et tutoriels

## 📋 Templates Supportés

| Template | Description | Technologies | Use Cases |
|----------|-------------|--------------|-----------|
| **fastapi** | API REST moderne | FastAPI, Pydantic, SQLAlchemy | APIs robustes, microservices |
| **streamlit** | Applications web interactives | Streamlit, Pandas, Plotly | Dashboards, data apps |
| **flask** | API web légère | Flask, SQLAlchemy | APIs simples, prototypes |
| **cli** | Applications console | Click, Typer | Outils en ligne de commande |
| **library** | Bibliothèques réutilisables | Pure Python | Packages, modules |

1. **Superviseur (OpenAI GPT-4)** - Architecture et guidance
2. **Développeur Principal (Llama3.1:8b)** - Implémentation complète
3. **Développeur Backend (Llama3.1:8b)** - APIs et services
4. **Testeur (Llama3.1:8b)** - Tests unitaires et intégration
5. **Documentaliste (Llama3.1:8b)** - Documentation technique

## 📖 Utilisation

1. **Lancez l'interface** : `streamlit run app_crew.py`
2. **Décrivez votre projet** dans le brief
3. **Choisissez un template** (FastAPI, Streamlit, CLI, etc.)
4. **Cliquez sur "Générer"** et regardez les agents travailler
5. **Téléchargez** le projet généré complet

## 🔧 Configuration

### Variables d'environnement (.env)
```env
OPENAI_API_KEY=your_openai_api_key_here
OLLAMA_BASE_URL=http://localhost:11434  # Optionnel
```

### Prérequis
- Python 3.8+
- Ollama avec Llama3.1:8b installé
- Clé API OpenAI
- Accès internet

## 📚 Exemples de projets générés

- **API REST FastAPI** avec authentification JWT
- **Dashboard Streamlit** avec visualisations
- **CLI Python** avec argparse et typer
- **Bot Discord** avec commands et events
- **Bibliothèque Python** avec packaging complet

## 🛠️ Développement

Pour contribuer au projet :

```bash
# Cloner et installer en mode développement
git clone <repo_url>
cd LunaCore_CrewAI
python -m venv .venv
.venv\Scripts\Activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Si disponible

# Lancer les tests
pytest tests/

# Formater le code
black .
```

## 🤝 Support

## 📝 Guide d'Utilisation

### Étape 1 : Décrire Votre Projet
Dans l'interface Streamlit, décrivez précisément ce que vous voulez créer :

**Exemples de briefs efficaces :**
```text
"Crée une API REST FastAPI avec authentification JWT, CRUD pour un blog, 
et endpoints pour gérer articles, utilisateurs et commentaires"

"Développe un dashboard Streamlit pour analyser des données de ventes 
avec graphiques interactifs, filtres par date et export CSV"

"Code un bot Discord avec commandes pour modération, musique et 
système de niveaux avec base de données SQLite"
```

### Étape 2 : Choisir le Template
Sélectionnez le type de projet adapté à vos besoins dans le menu déroulant.

### Étape 3 : Lancer la Génération
1. Cliquez sur "🚀 Générer avec CrewAI"
2. Observez le flux des agents en temps réel
3. Les agents collaborent pour créer votre projet

### Étape 4 : Récupérer les Résultats
- **Visualisation** : Examinez le code dans les onglets
- **Téléchargement** : Récupérez le projet complet (ZIP)
- **Fichiers locaux** : Trouvez-les dans `sandbox/crew_output/`

## 💡 Exemples de Projets Générés

### API FastAPI Blog
```python
# Brief : "API REST pour un blog avec authentification"
# Résultat : Application FastAPI complète avec :
- Authentification JWT
- CRUD pour articles et utilisateurs  
- Validation Pydantic
- Base de données SQLAlchemy
- Tests pytest
- Documentation OpenAPI
```

### Dashboard Analytics
```python
# Brief : "Dashboard pour analyser des ventes"
# Résultat : Application Streamlit avec :
- Import/export CSV
- Graphiques interactifs Plotly
- Filtres par date et catégorie
- Métriques KPI
- Interface responsive
```

### CLI Tool
```python
# Brief : "Outil CLI pour gérer des fichiers"
# Résultat : Application console avec :
- Interface Click/Typer
- Commandes et sous-commandes
- Validation des arguments
- Aide contextuelle
- Configuration par fichier
```

## 🛠️ Commandes Essentielles

### Gestion de l'Environnement
```bash
# Activer l'environnement virtuel
.venv\Scripts\Activate

# Lancer LunaCore
.venv\Scripts\python.exe -m streamlit run app_crew.py

# Désactiver l'environnement
deactivate

# Mettre à jour les dépendances
pip install --upgrade -r requirements.txt
```

### Git et Versioning
```bash
# Workflow de développement
git add .
git commit -m "feat: Description des changements"
git push origin main

# Créer une nouvelle fonctionnalité
git checkout -b feature/nom-fonctionnalite
# ... développement ...
git push origin feature/nom-fonctionnalite
```

### Tests et Diagnostic
```bash
# Vérifier l'installation
python -c "from lunacore.crew_system import LunaCrewSystem; print('✅ LunaCore OK')"

# Tester CrewAI
python -c "import crewai; print('✅ CrewAI:', crewai.__version__)"

# Vérifier Ollama
ollama list
```

## 🚨 Dépannage

### Problèmes Courants

**❌ "No module named 'crewai'"**
```bash
# Solution 1 : Vérifier l'environnement virtuel
.venv\Scripts\Activate
pip list | findstr crewai

# Solution 2 : Réinstaller CrewAI  
pip uninstall crewai
pip install crewai

# Solution 3 : Utiliser le Python de l'environnement
.venv\Scripts\python.exe -m streamlit run app_crew.py
```

**❌ "Streamlit command not found"**
```bash
# Utiliser le chemin complet
.venv\Scripts\python.exe -m streamlit run app_crew.py
```

**❌ "Port already in use"**
```bash
# Utiliser un port différent
streamlit run app_crew.py --server.port 8502
```

### Support et Documentation

📖 **Documentation complète** : Voir `LUNACORE_GUIDE.txt`

## 🤝 Contribution

Les contributions sont les bienvenues ! 

### Comment Contribuer
1. **Fork** le repository
2. **Créer** une branche pour votre fonctionnalité
3. **Committer** vos changements
4. **Pousser** vers votre fork
5. **Créer** une Pull Request

### Types de Contributions
- 🐛 **Bug fixes** : Correction de bugs
- ✨ **Features** : Nouvelles fonctionnalités
- 📚 **Documentation** : Amélioration de la doc
- 🎨 **UI/UX** : Améliorations de l'interface
- 🧪 **Tests** : Ajout de tests

## 📞 Support

- **Issues** : Signaler des bugs ou demander des fonctionnalités
- **Discussions** : Questions et idées d'amélioration  
- **Wiki** : Documentation technique détaillée

## 📄 Licence

MIT License - Voir le fichier LICENSE pour les détails.

---

*Généré avec ❤️ par LunaCore CrewAI - Le futur de la génération de code collaborative*
