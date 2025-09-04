"""
LunaCore CrewAI - Interface Streamlit
Application multi-agents pour génération de code
"""

import streamlit as st
import time
import zipfile
import io
from pathlib import Path
import traceback

# Import du système CrewAI
try:
    from lunacore.crew_system import LunaCrewSystem
except ImportError as e:
    st.error(f"❌ Erreur d'import: {e}")
    st.stop()

# Configuration de la page
st.set_page_config(
    page_title="LunaCore CrewAI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .agent-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #FF6B6B;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown("""
<div class="main-header">
    <h1>🤖 LunaCore CrewAI</h1>
    <p>Système multi-agents intelligent • Llama3.1:8b + OpenAI GPT-4</p>
</div>
""", unsafe_allow_html=True)

# Sidebar - Configuration et informations
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Status des agents
    if st.button("🔍 Vérifier les connexions", use_container_width=True):
        with st.spinner("Vérification en cours..."):
            try:
                crew_system = LunaCrewSystem()
                st.success(f"✅ {len(crew_system.agents)} agents initialisés")
                st.success("✅ Llama3.1:8b connecté")
                st.success("✅ OpenAI GPT-4 connecté")
                
                # Afficher les agents
                st.subheader("🤖 Agents disponibles")
                agents_info = {
                    "supervisor": "🧠 Superviseur (OpenAI)",
                    "main_developer": "💻 Dev Principal (Llama)",
                    "backend_developer": "🔧 Dev Backend (Llama)",
                    "tester": "🧪 Testeur (Llama)",
                    "documenter": "📚 Documentaliste (Llama)"
                }
                
                for agent_key, description in agents_info.items():
                    if agent_key in crew_system.agents:
                        st.write(f"✅ {description}")
                    else:
                        st.write(f"❌ {description}")
                        
            except Exception as e:
                st.error(f"❌ Erreur de connexion: {e}")
                st.error("Vérifiez votre fichier .env et que Ollama est démarré")
    
    st.divider()
    
    # Informations sur le workflow
    st.subheader("📋 Workflow des agents")
    st.markdown("""
    **1. 🧠 Superviseur (OpenAI)**
    - Analyse le brief
    - Conçoit l'architecture
    - Guide les développeurs
    
    **2. 💻 Développeur Principal**
    - Implémente le code principal
    - Crée la structure de base
    
    **3. 🔧 Développeur Backend**
    - APIs et endpoints
    - Services et middleware
    
    **4. 🧪 Testeur**
    - Tests unitaires
    - Tests d'intégration
    
    **5. 📚 Documentaliste**
    - README et documentation
    - Requirements.txt
    """)
    
    st.divider()
    
    # Templates disponibles
    st.subheader("📦 Templates disponibles")
    st.write("• **FastAPI** - API REST moderne")
    st.write("• **Streamlit** - Dashboard interactif")
    st.write("• **Flask** - API web légère")
    st.write("• **CLI** - Application ligne de commande")
    st.write("• **Library** - Bibliothèque Python")

# Onglets pour l'interface principale
tab_generate, tab_logs = st.tabs(["🚀 Génération", "📊 Logs"])

# Onglet de génération
with tab_generate:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Décrivez votre projet")
        
        # Templates rapides
        quick_templates = {
            "Custom": "",
            "API REST avec FastAPI": "Crée une API REST avec FastAPI, authentification JWT, CRUD pour gérer des utilisateurs et des articles de blog, avec validation Pydantic et documentation automatique",
            "Dashboard Streamlit": "Crée un dashboard Streamlit pour visualiser des données de ventes avec graphiques interactifs, filtres par date et région, et export PDF",
            "CLI Python": "Crée un outil CLI Python pour gérer des fichiers avec commandes pour lister, copier, supprimer, avec argparse et gestion d'erreurs",
            "Bot Discord": "Crée un bot Discord avec commandes pour modération, musique et jeux, utilisant discord.py avec gestion des événements",
            "Scraper Web": "Crée un scraper web avec BeautifulSoup pour extraire des données de sites e-commerce, avec gestion des proxies et sauvegarde CSV/JSON"
        }
        
        selected_template = st.selectbox(
            "🚀 Templates rapides (optionnel)",
            list(quick_templates.keys())
        )
        
        # Brief du projet
        if selected_template != "Custom":
            brief = st.text_area(
                "Brief du projet",
                value=quick_templates[selected_template],
                height=120,
                help="Vous pouvez modifier ce template selon vos besoins"
            )
        else:
            brief = st.text_area(
                "Brief du projet",
                height=120,
                placeholder="Décrivez en détail le projet que vous souhaitez générer...\n\nExemple: Crée une API REST avec FastAPI pour gérer une bibliothèque. Inclus authentification JWT, CRUD pour livres et auteurs, recherche par titre/auteur, système de prêt avec dates, et documentation Swagger automatique.",
                help="Plus vous êtes précis, meilleur sera le résultat !"
            )
        
        # Paramètres du projet
        col1a, col1b = st.columns(2)
        
        with col1a:
            template_type = st.selectbox(
                "🏗️ Type de template",
                ["fastapi", "streamlit", "flask", "cli", "library"],
                help="Le type de projet détermine la structure et les dépendances"
            )
        
        with col1b:
            project_name = st.text_input(
                "📁 Nom du projet (optionnel)",
                placeholder="mon_super_projet",
                help="Laissez vide pour génération automatique"
            )

    with col2:
        st.subheader("🔄 Processus de génération")
        
        st.markdown("""
        ```mermaid
        graph TD
            A[📝 Brief] --> B[🧠 Architecture OpenAI]
            B --> C[💻 Code Principal Llama]
            B --> D[🔧 Backend Llama]
            C --> E[🧪 Tests Llama]
            D --> E
            E --> F[📚 Documentation Llama]
            F --> G[✅ Projet Complet]
            
            style A fill:#e1f5fe
            style B fill:#fff3e0
            style C fill:#f3e5f5
            style D fill:#f3e5f5
            style E fill:#e8f5e8
            style F fill:#fff8e1
            style G fill:#e0f2f1
        ```
        """)
        
        st.info("""
        **💡 Conseils pour un bon brief:**
        
        • Soyez spécifique sur les fonctionnalités
        • Mentionnez les technologies préférées
        • Décrivez les cas d'usage principaux
        • Précisez le type d'interface (API, CLI, web)
        """)

# Zone de génération
st.divider()

# Bouton de génération principal
generate_button = st.button(
    "🚀 Générer le projet avec CrewAI",
    type="primary",
    use_container_width=True,
    disabled=not brief.strip()
)

if generate_button:
    # Conteneurs pour l'affichage en temps réel
    status_container = st.empty()
    progress_container = st.empty()
    logs_container = st.expander("📜 Logs détaillés des agents", expanded=True)
    results_container = st.container()
    
    # Variables de suivi
    logs = []
    start_time = time.time()
    
    def add_log(message, level="info"):
        """Ajoute un log avec timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        icon = "ℹ️" if level == "info" else "✅" if level == "success" else "❌"
        logs.append(f"[{timestamp}] {icon} {message}")
        
        with logs_container:
            st.code("\n".join(logs[-15:]), language=None)
    
    try:
        # Phase 1: Initialisation
        with status_container:
            st.info("🔧 Initialisation du système CrewAI...")
        
        with progress_container:
            progress_bar = st.progress(0)
        
        add_log("Démarrage de LunaCore CrewAI")
        add_log("Initialisation des agents multi-agents")
        
        # Créer le système
        crew_system = LunaCrewSystem()
        progress_bar.progress(20)
        add_log(f"Système initialisé avec {len(crew_system.agents)} agents", "success")
        
        # Phase 2: Planification
        status_container.info("🧠 Le superviseur OpenAI analyse le brief...")
        progress_bar.progress(30)
        add_log("OpenAI Superviseur: Analyse du brief et conception de l'architecture")
        
        # Phase 3: Génération
        status_container.info("💻 Les agents Llama génèrent le code...")
        progress_bar.progress(50)
        add_log("Llama Dev Principal: Implémentation du code principal")
        add_log("Llama Dev Backend: Création des composants backend")
        add_log("Llama Testeur: Génération des tests")
        add_log("Llama Documentaliste: Rédaction de la documentation")
        
        # Lancement de la génération réelle
        result = crew_system.generate_project(brief, template_type)
        
        # Phase 4: Finalisation
        progress_bar.progress(100)
        
        if result["status"] == "success":
            status_container.success(f"✅ Projet généré en {result['execution_time']}s !")
            add_log(f"Génération terminée avec succès", "success")
            add_log(f"Fichiers créés: {len(result['files'])}", "success")
            add_log(f"Temps d'exécution: {result['execution_time']}s", "success")
            
            # Affichage des résultats
            with results_container:
                st.subheader("🎉 Projet généré avec succès !")
                
                # Métriques
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("📁 Fichiers", len(result['files']))
                with col2:
                    st.metric("🤖 Agents", result['agents_count'])
                with col3:
                    st.metric("📋 Tâches", result['tasks_count'])
                with col4:
                    st.metric("⏱️ Temps", f"{result['execution_time']}s")
                
                # Aperçu des fichiers générés
                if result['files']:
                    st.subheader("📄 Fichiers générés")
                    
                    # Créer des onglets pour les fichiers
                    file_names = list(result['files'].keys())
                    if file_names:
                        # Limiter à 5 onglets pour l'affichage
                        display_files = file_names[:5]
                        tabs = st.tabs([f"📄 {name}" for name in display_files])
                        
                        for idx, (filename, content) in enumerate([(f, result['files'][f]) for f in display_files]):
                            with tabs[idx]:
                                # Déterminer le langage pour la coloration syntaxique
                                if filename.endswith('.py'):
                                    language = "python"
                                elif filename.endswith('.md'):
                                    language = "markdown"
                                elif filename.endswith('.txt'):
                                    language = "text"
                                elif filename.endswith(('.json', '.yaml', '.yml')):
                                    language = "json"
                                else:
                                    language = "text"
                                
                                st.code(content, language=language)
                                
                                # Bouton de téléchargement individuel
                                st.download_button(
                                    f"⬇️ Télécharger {filename}",
                                    data=content,
                                    file_name=filename,
                                    key=f"download_{idx}"
                                )
                    
                    # Bouton de téléchargement ZIP
                    st.subheader("📦 Téléchargement")
                    
                    # Créer le ZIP
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        for filename, content in result['files'].items():
                            zipf.writestr(filename, content)
                    
                    project_name_final = project_name if project_name else f"lunacore_project_{int(time.time())}"
                    
                    st.download_button(
                        "🗜️ Télécharger tout le projet (ZIP)",
                        data=zip_buffer.getvalue(),
                        file_name=f"{project_name_final}.zip",
                        mime="application/zip",
                        use_container_width=True
                    )
                    
                    # Instructions de déploiement
                    st.subheader("🚀 Instructions de déploiement")
                    deploy_instructions = f"""
**1. Extraire le projet :**
```bash
# Décompresser le fichier ZIP
unzip {project_name_final}.zip
cd {project_name_final}
```

**2. Installer les dépendances :**
```bash
# Créer un environnement virtuel
python -m venv .venv

# Activer l'environnement (Windows)
.venv\\Scripts\\Activate

# Installer les dépendances
pip install -r requirements.txt
```

**3. Lancer le projet :**
```bash
# Pour FastAPI
uvicorn main:app --reload

# Pour Streamlit
streamlit run app.py

# Pour CLI
python main.py --help
```
                    """
                    st.markdown(deploy_instructions)
                
                else:
                    st.warning("Aucun fichier généré. Vérifiez le brief et réessayez.")
        
        else:
            status_container.error("❌ Erreur lors de la génération")
            add_log(f"Erreur: {result.get('error', 'Erreur inconnue')}", "error")
            st.error(f"Détails: {result.get('error', 'Erreur inconnue')}")
    
    except Exception as e:
        status_container.error("❌ Erreur critique")
        add_log(f"Erreur critique: {str(e)}", "error")
        st.error(f"Erreur: {str(e)}")
        st.error("Vérifiez que Ollama est démarré et que votre clé OpenAI est configurée")
        
        # Affichage de la stack trace en mode debug
        with st.expander("🔍 Détails techniques (debug)"):
            st.code(traceback.format_exc())

# Onglet des logs
with tab_logs:
    st.subheader("📊 Logs du système")
    
    # Import du module de journalisation
    from lunacore.logger import get_logger
    
    # Boutons de filtrage
    st.write("Filtrer par type:")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        show_info = st.checkbox("ℹ️ Info", value=True)
    with col2:
        show_warning = st.checkbox("⚠️ Warning", value=True)
    with col3:
        show_error = st.checkbox("❌ Error", value=True)
    with col4:
        show_success = st.checkbox("✅ Success", value=True)
    
    # Bouton de rafraîchissement
    if st.button("🔄 Rafraîchir les logs", use_container_width=True):
        st.success("Logs rafraîchis")
    
    # Récupération et affichage des logs
    try:
        luna_logger = get_logger()
        logs = luna_logger.get_logs()
        
        if logs:
            # Création d'un tableau pour les logs
            filtered_logs = []
            for log in logs:
                level = log.get('level', 'INFO')
                if (level == "INFO" and show_info) or \
                   (level == "WARNING" and show_warning) or \
                   (level == "ERROR" and show_error) or \
                   (level == "SUCCESS" and show_success):
                    filtered_logs.append(log)
            
            if filtered_logs:
                # En-têtes du tableau
                st.write("### Derniers logs")
                
                # Tableau des logs
                data = []
                for log in filtered_logs:
                    icon = "ℹ️" if log['level'] == "INFO" else "⚠️" if log['level'] == "WARNING" else "❌" if log['level'] == "ERROR" else "✅"
                    data.append({
                        "Heure": log['timestamp'],
                        "Type": f"{icon} {log['level']}",
                        "Catégorie": log['category'],
                        "Message": log['message']
                    })
                
                st.table(data)
            else:
                st.info("Aucun log correspondant aux filtres sélectionnés.")
        else:
            st.info("Aucun log disponible pour le moment.")
    except Exception as e:
        st.error(f"Erreur lors de la récupération des logs: {e}")
        with st.expander("Détails"):
            st.code(traceback.format_exc())

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    <p>🤖 <strong>LunaCore CrewAI</strong> v1.0 • Propulsé par CrewAI, Llama3.1:8b et OpenAI GPT-4</p>
    <p>Généré avec ❤️ par l'équipe LunaCore</p>
</div>
""", unsafe_allow_html=True)
