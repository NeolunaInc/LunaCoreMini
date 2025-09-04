#!/usr/bin/env python3
"""
Test spécifique pour vérifier la robustesse des tools du Superviseur
"""

from lunacore.crew_system import LunaCrewSystem
import time

def test_tools_robustness():
    """Test la vérification de robustesse des tools"""
    print("🧪 Test de la vérification de robustesse des tools...")
    
    try:
        # Initialiser le système
        system = LunaCrewSystem()
        
        # Simuler une assignation de tools (ce qui va déclencher la vérification)
        print("\n📋 Test d'assignation de tools...")
        
        # Lancer un test minimal pour voir les logs de vérification
        result = system.generate_project(
            brief="App simple test", 
            template="python"
        )
        
        print("✅ Test terminé avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur durant le test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_tools_robustness()
    print(f"\n🎯 Résultat du test: {'✅ SUCCÈS' if success else '❌ ÉCHEC'}")
