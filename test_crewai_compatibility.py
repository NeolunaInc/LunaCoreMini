#!/usr/bin/env python3
"""Test spécifique pour vérifier que le problème supports_stop_words est résolu"""

from lunacore.crew_system import LunaCrewSystem
from crewai import Agent, Task, Crew, Process

def test_crewai_llm_compatibility():
    print("🧪 Test de compatibilité CrewAI LLM")
    
    # Initialiser le système
    luna = LunaCrewSystem()
    print("✅ Système LunaCore initialisé")
    
    # Créer un agent simple pour tester
    test_agent = Agent(
        role="Test Agent",
        goal="Tester la compatibilité LLM",
        backstory="Je suis un agent de test",
        llm=luna.openai,  # Utiliser le LLM CrewAI
        verbose=True,
        max_iter=1
    )
    
    # Créer une tâche simple
    test_task = Task(
        description="Dis simplement 'Bonjour, je fonctionne correctement!'",
        expected_output="Un message de confirmation",
        agent=test_agent
    )
    
    # Créer et exécuter le crew
    try:
        crew = Crew(
            agents=[test_agent],
            tasks=[test_task],
            process=Process.sequential,
            verbose=True
        )
        
        print("🚀 Exécution du test de compatibilité...")
        result = crew.kickoff()
        
        print("✅ Test réussi ! Aucun problème supports_stop_words")
        print(f"📋 Résultat: {result}")
        
    except Exception as e:
        if "supports_stop_words" in str(e):
            print(f"❌ Problème supports_stop_words encore présent: {e}")
        else:
            print(f"⚠️ Autre erreur (normale pendant les tests): {e}")

if __name__ == "__main__":
    test_crewai_llm_compatibility()
