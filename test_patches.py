#!/usr/bin/env python3
"""Test spécifique pour valider tous les patches appliqués"""

from lunacore.crew_system import LunaCrewSystem

def test_patches():
    print("🧪 Test de validation de tous les patches")
    
    # Initialiser le système
    luna = LunaCrewSystem()
    print("✅ Système LunaCore initialisé")
    
    # Test 1: Brief simple avec Streamlit pour vérifier l'injection du brief
    brief_simple = "Create a simple Streamlit map application showing Paris with folium"
    
    print(f"\n📋 Test avec brief: {brief_simple}")
    
    try:
        result = luna.generate_project(brief_simple, template="streamlit")
        
        print("\n🎯 Résultats de génération:")
        print(f"📊 Status: {result['status']}")
        print(f"⏱️ Temps d'exécution: {result['execution_time']}s")
        print(f"📁 Fichiers générés: {len(result['files'])}")
        print(f"🤖 Agents utilisés: {result['agents_count']}")
        print(f"📋 Tâches exécutées: {result['tasks_count']}")
        
        # Vérifier si routing.json existe
        if 'routing.json' in result['files']:
            print("✅ Fichier routing.json créé")
        
        # Vérifier si plan.json existe
        if 'plan.json' in result['files']:
            print("✅ Fichier plan.json créé par le superviseur")
            # Vérifier que le plan contient des éléments liés au brief
            plan_content = result['files']['plan.json']
            if 'streamlit' in plan_content.lower() or 'map' in plan_content.lower() or 'folium' in plan_content.lower():
                print("✅ Le plan.json est bien basé sur le brief (mots-clés trouvés)")
            else:
                print("⚠️ Le plan.json pourrait être générique")
        
        # Afficher les fichiers générés
        if result['files']:
            print("\n📁 Fichiers créés:")
            for filename, content in result['files'].items():
                size = len(content) if isinstance(content, str) else 0
                print(f"  - {filename} ({size} caractères)")
                
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_patches()
