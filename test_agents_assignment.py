#!/usr/bin/env python3
"""Test rapide des agents et de leur assignation LLM"""

from lunacore.crew_system import LunaCrewSystem
from lunacore.llm_orchestrator import LLMOrchestrator
from pathlib import Path

def test_agents_assignment():
    print("🧪 Test d'assignation des LLM aux agents")
    
    # Initialiser le système
    luna = LunaCrewSystem()
    
    # Créer un orchestrateur pour tester l'assignation
    orchestrator = LLMOrchestrator(
        run_dir=Path('test_agents'),
        llama_available=luna.llama_available,
        openai_available=True
    )
    
    # Test avec brief simple (complexité faible)
    decision_simple = orchestrator.decide("Create a simple calculator")
    luna._assign_llms_to_agents(decision_simple)
    
    print(f"📊 Brief simple - Complexité: {decision_simple.complexity}")
    print("🤖 Assignation des agents:")
    for agent_name, agent in luna.agents.items():
        llm_type = "OpenAI" if hasattr(agent.llm, '_client') else "Ollama" 
        print(f"  - {agent_name}: {agent.role} → {llm_type}")
    
    print("\n" + "="*50)
    
    # Test avec brief complexe
    decision_complex = orchestrator.decide("Create a complex multi-tenant OAuth2 system with PostgreSQL and real-time features")
    luna._assign_llms_to_agents(decision_complex)
    
    print(f"📊 Brief complexe - Complexité: {decision_complex.complexity}")
    print("🤖 Assignation des agents:")
    for agent_name, agent in luna.agents.items():
        llm_type = "OpenAI" if hasattr(agent.llm, '_client') else "Ollama"
        print(f"  - {agent_name}: {agent.role} → {llm_type}")

if __name__ == "__main__":
    test_agents_assignment()
