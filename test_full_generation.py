#!/usr/bin/env python3
"""Test complet du système LunaCore avec routeur intégré"""

from lunacore.crew_system import LunaCrewSystem

def test_generation():
    print("🚀 Test de génération complète avec routeur LLM")
    
    # Initialiser le système
    luna = LunaCrewSystem()
    print("✅ Système LunaCore initialisé")
    
    # Brief de test simple
    brief = "Create a simple map application using Streamlit that shows a basic map"
    
    print(f"📋 Brief: {brief}")
    
    # Génération du projet
    try:
        result = luna.generate_project(brief, template="streamlit")
        
        print("\n🎯 Résultats de génération:")
        print(f"📊 Status: {result['status']}")
        print(f"⏱️ Temps d'exécution: {result['execution_time']}s")
        print(f"📁 Fichiers générés: {len(result['files'])}")
        print(f"🤖 Agents utilisés: {result['agents_count']}")
        print(f"📋 Tâches exécutées: {result['tasks_count']}")
        
        # Afficher les fichiers générés
        if result['files']:
            print("\n📁 Fichiers créés:")
            for filename, content in result['files'].items():
                size = len(content) if isinstance(content, str) else 0
                print(f"  - {filename} ({size} caractères)")
                
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_generation()
