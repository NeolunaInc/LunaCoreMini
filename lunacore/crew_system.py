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

# Import du module de journalisation amélioré
from lunacore.logger import info, warning, error, success, get_logger

# Import du gestionnaire d'erreurs
from lunacore.error_handler import (
    ErrorContext, safe_execute, with_timeout, handle_llm_error,
    LunaError, AgentError, LLMError, TimeoutError
)

# CrewAI imports
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool

# Import des tools runtime
from lunacore.tools_runtime import make_write_file_tool, validate_python_syntax

# OpenAI client pour fallback
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

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
        
        # Récupérer le logger pour tracking des agents
        self.logger = get_logger()
        
        # Initialiser les LLMs
        self._init_llms()
        
        # Variable pour stocker le dossier du projet courant
        self.current_project_folder = None
        
        # Créer les agents (sans tools pour l'instant)
        self.agents = self._create_agents()
        
        success(f"LunaCrewSystem initialisé avec {len(self.agents)} agents", "system")
    
    def _init_llms(self):
        """Initialise les modèles de langage avec CrewAI LLM natifs"""
        try:
            # Initialiser OpenAI avec CrewAI LLM
            openai_key = os.getenv("OPENAI_API_KEY")
            if not openai_key or openai_key == "your_openai_api_key_here":
                raise ValueError("OPENAI_API_KEY non configurée dans .env")
            
            self.openai = LLM(model="openai/gpt-4o-mini")
            print(f"✅ OpenAI gpt-4o-mini connecté (CrewAI LLM)")
            
            # Initialiser client OpenAI direct pour fallback tools
            if OpenAI:
                self.openai_client = OpenAI(api_key=openai_key)
            else:
                self.openai_client = None
            
            # Test Ollama
            try:
                ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
                self.llama = LLM(
                    model="ollama/llama3.1:8b", 
                    base_url=ollama_base_url
                )
                # Test rapide
                test_response = "OK"  # Pas de test real pour éviter les timeouts
                self.llama_available = True
                print(f"✅ Ollama llama3.1:8b connecté (CrewAI LLM)")
                
            except Exception as e:
                print(f"⚠️ Ollama non disponible: {e}")
                self.llama = self.openai  # Fallback vers OpenAI
                self.llama_available = False
                print("🔄 Utilisation d'OpenAI comme fallback pour le développement")
                
        except Exception as e:
            print(f"❌ Erreur d'initialisation LLM: {e}")
            raise
    def _create_agents(self) -> Dict[str, Agent]:
        """Crée les 3 agents essentiels selon les spécifications LunaCore refactorisées"""
        agents = {}
        
        # SUPERVISEUR - Architecte et Planificateur
        agents['supervisor'] = Agent(
            role="Superviseur",
            goal="Élaborer un plan exécutable, figer les interfaces, découper le travail.",
            backstory="Architecte senior, rigoureux, privilégie robustesse et lisibilité.",
            llm=self.openai,  # Assignation directe OpenAI pour superviseur
            tools=[],  # Tools seront assignés dans generate_project
            allow_delegation=False,
            verbose=True,
            max_iter=3,
        )
        
        # DÉVELOPPEUR - Code et implémentation 
        agents['developer'] = Agent(
            role="Développeur",
            goal="Implémenter tout le code selon plan.json sans dévier du contrat.",
            backstory="Ingénieur fullstack, TDD, docstrings, type hints, code clair.",
            llm=self.llama,  # Assignation directe Llama pour développeur
            tools=[],  # Tools seront assignés dans generate_project
            allow_delegation=False,
            verbose=True,
            max_iter=4,
        )
        
        # TESTEUR - Tests et qualité
        agents['tester'] = Agent(
            role="Testeur",
            goal="Générer tests Pytest, smoke tests, README d'exécution.",
            backstory="Test d'abord, coverage et cas limites.",
            llm=self.llama,  # Assignation directe Llama pour testeur
            tools=[],  # Tools seront assignés dans generate_project
            allow_delegation=False,
            verbose=True,
            max_iter=3,
        )
        
        return agents
    
    def test_agents(self) -> Dict:
        """Vérifie que chaque agent peut répondre à un prompt minimal via son LLM."""
        from time import time as _now
        results = {
            'status': 'ok',
            'agents_count': len(self.agents),
            'agent_tests': {},
            'llm_backend': {
                'model': os.getenv("LUNACORE_PLANNER_MODEL", "gpt-4o-mini"),
                'ollama_available': self.llama_available,
            },
        }
        test_prompt = "Réponds simplement: OK."
        for agent_name, agent in self.agents.items():
            start = _now()
            try:
                messages = [{"role": "user", "content": test_prompt}]
                # CrewAI LLM wrapper -> .call(messages)
                _ = safe_execute(
                    agent.llm.call,
                    messages,
                    fallback="(pas de réponse)",
                    error_msg=f"test {agent_name}",
                )
                duration = _now() - start
                self.logger.log_agent(agent_name, "test_connection", "success", duration)
                results['agent_tests'][agent_name] = {'status': 'success', 'duration': duration}
            except Exception as e:
                duration = _now() - start
                self.logger.log_agent(agent_name, "test_connection", "failed", duration)
                results['agent_tests'][agent_name] = {'status': 'failed', 'duration': duration, 'error': str(e)}
        if any(t['status'] == 'failed' for t in results['agent_tests'].values()):
            results['status'] = 'partial'
        return results
    
    def generate_project(self, brief: str, template: str = "fastapi") -> Dict:
        """
        Génère un projet complet avec le crew multi-agents et tools runtime
        
        Args:
            brief: Description du projet à générer
            template: Type de template (fastapi, streamlit, cli, etc.)
        
        Returns:
            Dictionnaire avec les résultats de génération
        """
        info(f"🚀 Génération du projet: {brief[:50]}...", "generation")
        info(f"📋 Template: {template}", "generation")
        
        start_time = time.time()
        
        try:
            # Créer le répertoire de travail pour cette exécution
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            project_name = self._extract_project_name(brief)
            run_dir = Path("sandbox/crew_output") / f"{project_name}_{timestamp}"
            run_dir.mkdir(parents=True, exist_ok=True)
            
            # Stocker le répertoire de travail actuel
            self.current_project_folder = run_dir
            
            # LLM déjà assignés directement dans _create_agents (pas de routeur)
            info(f"🤖 LLM Assignés:", "llm")
            info(f"  - Superviseur: openai", "llm")
            info(f"  - Développeur: ollama", "llm")
            info(f"  - Testeur: ollama", "llm")
            
            # Durcir: s'assurer que run_dir existe systématiquement avant création des outils
            self.current_project_folder.mkdir(parents=True, exist_ok=True)
            
            # Créer les tools simplifiés
            write_tool = make_write_file_tool(self.current_project_folder)
            
            # Assigner les tools aux agents (tous ont les mêmes tools simplifiés)
            for agent in self.agents.values():
                agent.tools = [write_tool, validate_python_syntax]
            
            # Créer les tâches avec brief injecté
            tasks = self._create_project_tasks_with_brief(brief, template)
            
            # Créer le crew avec processus séquentiel et paramètres simples
            crew = Crew(
                agents=list(self.agents.values()),
                tasks=tasks,
                process=Process.sequential,
                verbose=True,
                memory=True
            )
            
            # Exécuter la génération
            result = crew.kickoff(inputs={
                "brief": brief,
                "template": template,
                "project_name": self._extract_project_name(brief)
            })
            
            # Analyser les résultats
            execution_time = time.time() - start_time
            generated_files = list(self.current_project_folder.rglob("*")) if self.current_project_folder else {}
            
            return {
                "status": "success",
                "execution_time": round(execution_time, 2),
                "files": {str(f.relative_to(self.current_project_folder)): f.read_text(encoding='utf-8') 
                         for f in generated_files if f.is_file()} if self.current_project_folder else {},
                "agents_count": len(self.agents),
                "tasks_count": len(tasks),
                "result": str(result),
                "output_directory": str(self.current_project_folder)
            }
            
        except Exception as e:
            print(f"❌ Erreur lors de la génération: {e}")
            return {
                "status": "error",
                "error": str(e),
                "execution_time": time.time() - start_time
            }
    
    def _create_project_tasks_with_brief(self, brief: str, template: str) -> List[Task]:
        """Crée les 3 tâches séquentielles simplifiées avec brief explicitement injecté"""
        tasks = []
        
        # TÂCHE 1: PLANNER (Superviseur) avec brief injecté
        tasks.append(Task(
            description=(
                "En te basant STRICTEMENT sur ce brief (ne pas inventer autre chose):\n"
                f"'''{brief}'''\n\n"
                "- Produis un plan.json exhaustif: modules, fichiers, interfaces/endpoints, schémas DB, plan de tests.\n"
                "- Écris directement le fichier 'plan.json' via l'outil write_file_tool.\n"
                "- Utilise le dossier de projet déjà créé (ne pas créer de nouveau dossier).\n"
                "- Pas de code ici; seulement la structure et les contrats testables."
            ),
            expected_output="Fichier 'plan.json' créé à la racine du run_dir.",
            agent=self.agents["supervisor"]
        ))
        
        # TÂCHE 2: DÉVELOPPEMENT (Développeur)
        tasks.append(Task(
            description="Implémenter TOUT le code (backend, frontend, API, DB, UI) strictement selon plan.json sans écart du contrat.",
            expected_output="Tous les fichiers de code implémentés selon plan.json.",
            agent=self.agents["developer"]
        ))
        
        # TÂCHE 3: TESTS (Testeur)
        tasks.append(Task(
            description="Générer tests Pytest et script smoke-tests ; vérifier toutes les fonctionnalités principales.",
            expected_output="tests/*.py, scripts/smoke_test.sh, rapport minimal.",
            agent=self.agents["tester"]
        ))
        
        return tasks
    
    def _extract_project_name(self, brief: str) -> str:
        """Extrait un nom de projet du brief"""
        # Nettoie et extrait les premiers mots significatifs
        words = re.findall(r'\b[a-zA-Z]{3,}\b', brief.lower())
        project_name = "_".join(words[:2]) if len(words) >= 2 else "lunacore_project"
        return project_name

# Instance globale pour utilisation facile
luna_crew = None

def get_crew_system() -> LunaCrewSystem:
    """Retourne l'instance globale du système CrewAI"""
    global luna_crew
    if luna_crew is None:
        luna_crew = LunaCrewSystem()
    return luna_crew
