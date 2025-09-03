"""
LunaCore CrewAI System
Multi-agent code generation with CrewAI framework
"""

import os
import re
import ast
import time
from pathlib import Path
from typing import List, Dict, Optional
from dotenv import load_dotenv

# CrewAI imports
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool

# LangChain imports
from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

class LunaCrewSystem:
    """
    Système multi-agents avec CrewAI pour génération de projets complets
    
    Architecture:
    - OpenAI GPT-4 : Superviseur/Architecte (planification, guidance)
    - Llama3.1:8b : Développeurs spécialisés (implémentation)
    """
    
    def __init__(self):
        """Initialise le système CrewAI avec tous les agents"""
        self.llama_model = "llama3.1:8b"
        self.openai_model = "gpt-4o-mini"
        
        # Initialiser les LLMs
        self._init_llms()
        
        # Créer les outils
        self.tools = self._create_tools()
        
        # Créer les agents
        self.agents = self._create_agents()
        
        print(f"✅ LunaCrewSystem initialisé avec {len(self.agents)} agents")
    
    def _init_llms(self):
        """Initialise les modèles de langage"""
        try:
            # Ollama pour Llama3.1:8b
            ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            self.llama = Ollama(
                model=self.llama_model,
                base_url=ollama_base_url,
                temperature=0.7
            )
            self.llama_available = True
            print(f"✅ Llama3.1:8b connecté via {ollama_base_url}")
            
        except Exception as e:
            print(f"⚠️ Ollama non disponible: {e}")
            # Fallback vers OpenAI
            self.llama = None
            self.llama_available = False
            
        try:
            # OpenAI pour supervision
            openai_key = os.getenv("OPENAI_API_KEY")
            if not openai_key or openai_key == "your_openai_api_key_here":
                raise ValueError("OPENAI_API_KEY non configurée dans .env")
            
            self.openai = ChatOpenAI(
                model=self.openai_model,
                temperature=0.2,
                api_key=openai_key
            )
            print(f"✅ OpenAI {self.openai_model} connecté")
            
            # Si Ollama n'est pas disponible, utilise OpenAI pour tout
            if not self.llama_available:
                self.llama = ChatOpenAI(
                    model="gpt-4o-mini",
                    temperature=0.5,
                    api_key=openai_key
                )
                print("🔄 Utilisation d'OpenAI comme fallback pour le développement")
            
        except Exception as e:
            print(f"❌ Erreur d'initialisation OpenAI: {e}")
            raise
    
    def _create_tools(self):
        """Crée les outils personnalisés pour les agents"""
        
        @tool
        def write_file_tool(filename: str, content: str) -> str:
            """Écrit du contenu dans un fichier"""
            try:
                # Créer le répertoire si nécessaire
                output_dir = Path("sandbox/crew_output")
                output_dir.mkdir(parents=True, exist_ok=True)
                
                file_path = output_dir / filename
                file_path.write_text(content, encoding='utf-8')
                
                lines = len(content.splitlines())
                return f"✅ Fichier {filename} créé ({lines} lignes)"
            except Exception as e:
                return f"❌ Erreur lors de l'écriture de {filename}: {e}"
        
        @tool
        def validate_python_syntax(code: str) -> str:
            """Valide la syntaxe Python d'un code"""
            try:
                ast.parse(code)
                return "✅ Syntaxe Python valide"
            except SyntaxError as e:
                return f"❌ Erreur de syntaxe: {e.msg} (ligne {e.lineno})"
        
        @tool
        def ask_supervisor_help(problem: str, context: str) -> str:
            """Demande de l'aide au superviseur OpenAI"""
            try:
                prompt = f"""
                Un agent développeur a besoin d'aide:
                
                PROBLÈME: {problem}
                CONTEXTE: {context}
                
                Fournis une guidance claire et actionnable (pas de code, juste l'approche/stratégie).
                Sois concis et pratique.
                """
                
                response = self.openai.invoke(prompt)
                return f"💡 Conseil du superviseur: {response.content}"
            except Exception as e:
                return f"❌ Erreur de communication avec le superviseur: {e}"
        
        return [write_file_tool, validate_python_syntax, ask_supervisor_help]
    
    def _create_agents(self) -> Dict[str, Agent]:
        """Crée tous les agents du système"""
        agents = {}
        
        # 🧠 SUPERVISEUR (OpenAI) - Architecture et guidance uniquement
        agents['supervisor'] = Agent(
            role="Architecte et Superviseur Senior",
            goal="Concevoir l'architecture du projet et guider les développeurs",
            backstory="""
            Tu es un architecte logiciel senior avec 15+ ans d'expérience.
            Tu NE CODES PAS - tu conçois, planifies et guides les autres agents.
            Tu interviens pour débloquer les situations complexes.
            """,
            llm=self.openai,
            verbose=True,
            allow_delegation=True,
            max_iter=2
        )
        
        # 💻 DÉVELOPPEUR PRINCIPAL (Llama) - Implémentation complète
        agents['main_developer'] = Agent(
            role="Développeur Full-Stack Principal",
            goal="Implémenter le code principal du projet de A à Z",
            backstory="""
            Tu es un développeur expert qui maîtrise Python, FastAPI, Streamlit, etc.
            Tu écris du code propre, fonctionnel et bien structuré.
            Tu implémentes les fichiers principaux (main.py, app.py, etc.).
            """,
            llm=self.llama,
            tools=self.tools,
            verbose=True,
            max_iter=4,
            memory=True
        )
        
        # 🔧 DÉVELOPPEUR BACKEND (Llama) - APIs et services
        agents['backend_developer'] = Agent(
            role="Développeur Backend Spécialisé",
            goal="Créer les APIs, endpoints et services backend",
            backstory="""
            Tu es spécialisé en développement backend.
            Tu crées les APIs REST, gères les bases de données et les services.
            Tu maîtrises FastAPI, Flask, SQLAlchemy, etc.
            """,
            llm=self.llama,
            tools=self.tools,
            verbose=True,
            max_iter=3
        )
        
        # 🧪 TESTEUR (Llama) - Tests automatisés
        agents['tester'] = Agent(
            role="Ingénieur QA et Tests",
            goal="Créer une suite de tests complète et robuste",
            backstory="""
            Tu es expert en tests automatisés avec pytest.
            Tu crées des tests unitaires, d'intégration et fonctionnels.
            Tu assures la qualité et la fiabilité du code.
            """,
            llm=self.llama,
            tools=self.tools,
            verbose=True,
            max_iter=2
        )
        
        # 📚 DOCUMENTALISTE (Llama) - Documentation technique
        agents['documenter'] = Agent(
            role="Rédacteur Technique",
            goal="Créer une documentation claire et complète",
            backstory="""
            Tu rédiges des documentations techniques excellentes.
            Tu crées des README, docstrings et guides d'utilisation.
            Tu expliques clairement comment utiliser le projet.
            """,
            llm=self.llama,
            tools=self.tools,
            verbose=True,
            max_iter=2
        )
        
        return agents
    
    def generate_project(self, brief: str, template: str = "fastapi") -> Dict:
        """
        Génère un projet complet avec le crew multi-agents
        
        Args:
            brief: Description du projet à générer
            template: Type de template (fastapi, streamlit, cli, etc.)
        
        Returns:
            Dictionnaire avec les résultats de génération
        """
        print(f"🚀 Génération du projet: {brief[:50]}...")
        print(f"📋 Template: {template}")
        
        start_time = time.time()
        
        try:
            # Créer les tâches
            tasks = self._create_project_tasks(brief, template)
            
            # Créer le crew avec processus hiérarchique
            crew = Crew(
                agents=list(self.agents.values()),
                tasks=tasks,
                process=Process.hierarchical,
                manager_llm=self.openai,  # OpenAI gère le processus
                verbose=True,
                memory=True,
                max_rpm=10
            )
            
            # Exécuter la génération
            result = crew.kickoff(inputs={
                "brief": brief,
                "template": template,
                "project_name": self._extract_project_name(brief)
            })
            
            # Analyser les résultats
            execution_time = time.time() - start_time
            generated_files = self._scan_output_directory()
            
            return {
                "status": "success",
                "execution_time": round(execution_time, 2),
                "files": generated_files,
                "agents_count": len(self.agents),
                "tasks_count": len(tasks),
                "result": str(result),
                "output_directory": "sandbox/crew_output"
            }
            
        except Exception as e:
            print(f"❌ Erreur lors de la génération: {e}")
            return {
                "status": "error",
                "error": str(e),
                "execution_time": time.time() - start_time
            }
    
    def _create_project_tasks(self, brief: str, template: str) -> List[Task]:
        """Crée les tâches pour le projet"""
        tasks = []
        
        # TÂCHE 1: Architecture (Superviseur OpenAI)
        tasks.append(Task(
            description=f"""
            Analyse le brief et conçois l'architecture complète:
            
            BRIEF: {brief}
            TEMPLATE: {template}
            
            Définis:
            1. Structure des fichiers et dossiers
            2. Composants principaux nécessaires
            3. Dépendances et technologies
            4. Plan d'implémentation étape par étape
            
            NE CODE PAS - fournis uniquement le plan architectural.
            """,
            agent=self.agents['supervisor'],
            expected_output="Plan d'architecture détaillé avec structure de fichiers"
        ))
        
        # TÂCHE 2: Implémentation principale (Llama)
        tasks.append(Task(
            description=f"""
            Implémente le fichier principal du projet selon l'architecture.
            
            Crée le fichier principal (main.py, app.py selon le template) avec:
            - Code complet et fonctionnel
            - Imports et dépendances
            - Structure de base du projet
            - Configuration nécessaire
            
            Template: {template}
            
            Utilise l'outil write_file_tool pour créer le fichier.
            """,
            agent=self.agents['main_developer'],
            expected_output="Fichier principal implémenté",
            context=[tasks[0]]
        ))
        
        # TÂCHE 3: Backend/API (si applicable)
        if template in ["fastapi", "flask", "django"]:
            tasks.append(Task(
                description="""
                Implémente les composants backend selon l'architecture:
                - Endpoints API nécessaires
                - Modèles de données
                - Middleware et configuration
                - Gestion des erreurs
                
                Utilise write_file_tool pour créer les fichiers backend.
                """,
                agent=self.agents['backend_developer'],
                expected_output="Composants backend implémentés",
                context=[tasks[0]]
            ))
        
        # TÂCHE 4: Tests
        tasks.append(Task(
            description="""
            Crée une suite de tests pour le projet:
            - Tests unitaires des fonctions principales
            - Tests d'intégration si nécessaire
            - Fichiers de test avec pytest
            - Configuration de test
            
            Utilise write_file_tool pour créer test_*.py
            """,
            agent=self.agents['tester'],
            expected_output="Suite de tests complète",
            context=tasks[-2:]
        ))
        
        # TÂCHE 5: Documentation
        tasks.append(Task(
            description="""
            Crée la documentation complète:
            - requirements.txt avec toutes les dépendances
            - README.md avec instructions d'installation/utilisation
            - Docstrings dans le code si nécessaire
            - Exemples d'utilisation
            
            Utilise write_file_tool pour créer la documentation.
            """,
            agent=self.agents['documenter'],
            expected_output="Documentation complète",
            context=tasks
        ))
        
        return tasks
    
    def _extract_project_name(self, brief: str) -> str:
        """Extrait un nom de projet du brief"""
        # Nettoie et extrait les premiers mots significatifs
        words = re.findall(r'\b[a-zA-Z]{3,}\b', brief.lower())
        project_name = "_".join(words[:2]) if len(words) >= 2 else "lunacore_project"
        return project_name
    
    def _scan_output_directory(self) -> Dict[str, str]:
        """Scanne le répertoire de sortie pour les fichiers générés"""
        output_dir = Path("sandbox/crew_output")
        files = {}
        
        if output_dir.exists():
            for file_path in output_dir.rglob("*"):
                if file_path.is_file():
                    try:
                        content = file_path.read_text(encoding='utf-8')
                        relative_path = str(file_path.relative_to(output_dir))
                        files[relative_path] = content
                    except Exception as e:
                        files[str(file_path.name)] = f"Erreur de lecture: {e}"
        
        return files

    def test_agents(self) -> Dict:
        """Test rapide de tous les agents"""
        try:
            return {
                "status": "success",
                "agents_count": len(self.agents),
                "llm_backend": "Llama3.1:8b" if self.llama_available else "OpenAI",
                "tools_count": len(self.tools),
                "agents": list(self.agents.keys())
            }
        except Exception as e:
            return {
                "status": "error", 
                "error": str(e)
            }

# Instance globale pour utilisation facile
luna_crew = None

def get_crew_system() -> LunaCrewSystem:
    """Retourne l'instance globale du système CrewAI"""
    global luna_crew
    if luna_crew is None:
        luna_crew = LunaCrewSystem()
    return luna_crew
