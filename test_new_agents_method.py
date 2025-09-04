#!/usr/bin/env python3
"""Test spécifique de la nouvelle méthode test_agents corrigée"""

from lunacore.crew_system import LunaCrewSystem

def test_new_agents_method():
    print("🧪 Test de la nouvelle méthode test_agents corrigée")
    
    # Initialiser le système
    luna = LunaCrewSystem()
    print("✅ Système LunaCore initialisé")
    
    # Tester la méthode test_agents corrigée
    try:
        result = luna.test_agents()
        
        print("\n🎯 Résultats du test des agents:")
        print(f"📊 Status: {result['status']}")
        print(f"👥 Nombre d'agents: {result['agents_count']}")
        print(f"🔧 Modèle LLM: {result['llm_backend']['model']}")
        print(f"🦙 Ollama disponible: {result['llm_backend']['ollama_available']}")
        
        print(f"\n📋 Tests individuels:")
        for agent_name, test_result in result['agent_tests'].items():
            status_icon = "✅" if test_result['status'] == 'success' else "❌"
            duration = test_result.get('duration', 0)
            print(f"  {status_icon} {agent_name}: {duration:.2f}s")
            
            if test_result['status'] == 'failed':
                print(f"      ❌ Erreur: {test_result.get('error', 'Unknown')}")
        
        return result['status'] in ['ok', 'partial']
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_new_agents_method()
    if success:
        print("\n🎉 Test de la méthode test_agents réussi !")
    else:
        print("\n💥 Test de la méthode test_agents échoué !")
        exit(1)
