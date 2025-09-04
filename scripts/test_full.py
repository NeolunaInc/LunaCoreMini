#!/usr/bin/env python3
"""
Test complet du système LunaCore
"""

import sys
import os
# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from lunacore.crew_system import LunaCrewSystem
from lunacore.logger import get_logger

def test_full_system():
    """Test complet du système"""
    print("🔬 Test complet du système LunaCore")
    print("=" * 50)
    
    try:
        # Initialisation
        print("1. Initialisation du système...")
        system = LunaCrewSystem()
        print("✅ Système initialisé")
        
        # Test des agents
        print("\n2. Test des agents...")
        result = system.test_agents()
        
        print(f"📊 Résultats des tests:")
        print(f"   - Status: {result['status']}")
        print(f"   - Agents: {result['agents_count']}")
        print(f"   - Ollama: {'✅' if result['llm_backend']['ollama_available'] else '❌'}")
        print(f"   - OpenAI: {'✅' if result['llm_backend']['model'] != 'none' else '❌'}")
        
        print(f"\n📋 Tests individuels:")
        for agent_name, test_result in result['agent_tests'].items():
            status_icon = "✅" if test_result['status'] == 'success' else "❌"
            duration = test_result['duration']
            print(f"   {status_icon} {agent_name}: {duration:.2f}s")
            
            if test_result['status'] == 'failed':
                print(f"      Error: {test_result.get('error', 'Unknown')}")
        
        # Résumé des activités des agents
        print("\n3. Résumé des activités...")
        logger = get_logger()
        summary = logger.get_agent_summary()
        
        print(f"📈 Activités totales: {summary['total_activities']}")
        for agent_name, metrics in summary['agent_metrics'].items():
            success_rate = (metrics['successful'] / metrics['total_actions'] * 100) if metrics['total_actions'] > 0 else 0
            print(f"   {agent_name}: {success_rate:.1f}% succès ({metrics['successful']}/{metrics['total_actions']})")
        
        # Export de session
        print("\n4. Export de la session...")
        export_result = logger.export_session()
        print(f"📁 Logs exportés:")
        print(f"   - Logs système: {export_result['log_file']}")
        print(f"   - Activités agents: {export_result['agent_activities']}")
        
        return result
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = test_full_system()
    if result:
        print(f"\n🎉 Test terminé avec succès - Status: {result['status']}")
    else:
        print("\n💥 Test échoué")
        sys.exit(1)
