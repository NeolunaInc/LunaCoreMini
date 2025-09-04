#!/usr/bin/env python3
"""Test du routeur LLM intégré"""

from lunacore.crew_system import LunaCrewSystem
from lunacore.llm_orchestrator import LLMOrchestrator
from pathlib import Path

def test_routing():
    print("🧪 Test du routeur LLM intégré")
    
    # Initialiser le système
    luna = LunaCrewSystem()
    print("✅ Système LunaCore initialisé")
    
    # Test de l'orchestrateur LLM
    orchestrator = LLMOrchestrator(
        run_dir=Path('test_run'),
        llama_available=luna.llama_available,
        openai_available=True
    )
    
    # Test avec un brief simple
    brief = "Create a simple FastAPI app with a map"
    decision = orchestrator.decide(brief)
    
    print(f"✅ Décision de routage pour: '{brief}'")
    print(f"📊 Complexité: {decision.complexity}")
    print(f"📋 Planner: {decision.planner}")
    print(f"🔧 Backend: {decision.backend}")
    print(f"🎨 Frontend: {decision.frontend}")
    print(f"📊 Data: {decision.data}")
    print(f"🧪 Tests: {decision.tests}")
    print(f"💡 Raison: {decision.reason}")
    
    # Test avec un brief complexe
    brief_complex = "Create a complex multi-tenant OAuth2 system with PostgreSQL, real-time websockets, Stripe payments, Docker, and comprehensive test coverage"
    decision_complex = orchestrator.decide(brief_complex)
    
    print(f"\n✅ Décision de routage pour brief complexe:")
    print(f"📊 Complexité: {decision_complex.complexity}")
    print(f"📋 Planner: {decision_complex.planner}")
    print(f"🔧 Backend: {decision_complex.backend}")
    print(f"🎨 Frontend: {decision_complex.frontend}")
    print(f"📊 Data: {decision_complex.data}")
    print(f"🧪 Tests: {decision_complex.tests}")
    print(f"💡 Raison: {decision_complex.reason}")

if __name__ == "__main__":
    test_routing()
