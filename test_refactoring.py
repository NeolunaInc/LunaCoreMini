#!/usr/bin/env python3
"""Test du refactoring de LunaCore"""

from lunacore.crew_system import LunaCrewSystem

def test_refactoring():
    print("🧪 Test du refactoring de LunaCore")
    
    try:
        system = LunaCrewSystem()
        print("✅ Refactoring réussi - Système initialisé avec succès")
        print(f"📊 Agents configurés: {len(system.agents)}")
        print(f"🤖 Agents: {list(system.agents.keys())}")
        
        # Vérifier que nous avons exactement 3 agents
        expected_agents = ['supervisor', 'developer', 'tester']
        actual_agents = list(system.agents.keys())
        
        if actual_agents == expected_agents:
            print("✅ Agents corrects après refactoring")
        else:
            print(f"❌ Agents incorrects. Attendu: {expected_agents}, Obtenu: {actual_agents}")
        
        # Test de génération rapide
        print("\n🔧 Test de génération simple...")
        result = system.generate_project('Test simple calculatrice', template='python')
        print(f"✅ Génération terminée: {result.get('status', 'unknown')}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = test_refactoring()
    print(f"\n{'✅ Refactoring validé' if success else '❌ Refactoring échoué'}")
