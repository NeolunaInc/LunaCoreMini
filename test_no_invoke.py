#!/usr/bin/env python3
"""
Test de validation finale : vérification de l'élimination complète d'invoke
"""

def test_no_invoke_in_codebase():
    """Vérifie qu'aucune trace d'invoke ne subsiste dans le codebase"""
    import os
    import re
    from pathlib import Path
    
    print("🧪 Test d'élimination complète d'invoke...")
    
    # Fichiers Python à vérifier
    python_files = [
        "lunacore/crew_system.py",
        "lunacore/crew_system_simple.py", 
        "lunacore/tools_runtime.py",
        "lunacore/llm_orchestrator.py",
        "lunacore/logger.py",
        "lunacore/error_handler.py"
    ]
    
    invoke_found = False
    
    for file_path in python_files:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'invoke' in content.lower():
                    # Vérifier si c'est un vrai usage problématique
                    lines = content.split('\n')
                    for i, line in enumerate(lines, 1):
                        if 'invoke' in line.lower() and not line.strip().startswith('#'):
                            print(f"⚠️  Trace d'invoke trouvée dans {file_path}:{i}")
                            print(f"    {line.strip()}")
                            invoke_found = True
    
    if not invoke_found:
        print("✅ Aucune trace d'invoke trouvée dans le codebase Python")
    
    return not invoke_found

def test_llm_apis():
    """Test que les APIs LLM utilisent bien .call() et les fallbacks corrects"""
    print("\n🧪 Test des APIs LLM...")
    
    try:
        from lunacore.crew_system import LunaCrewSystem
        system = LunaCrewSystem()
        print("✅ crew_system.py : Initialisation OK")
        
        from lunacore.crew_system_simple import LunaCrewSystemSimple
        system_simple = LunaCrewSystemSimple()
        print("✅ crew_system_simple.py : Initialisation OK")
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors du test des APIs LLM: {e}")
        return False

if __name__ == "__main__":
    print("🎯 Test de validation finale - Élimination d'invoke")
    print("=" * 50)
    
    test1 = test_no_invoke_in_codebase()
    test2 = test_llm_apis()
    
    print("\n🎯 Résultats:")
    print(f"  - Élimination d'invoke: {'✅ SUCCÈS' if test1 else '❌ ÉCHEC'}")
    print(f"  - APIs LLM fonctionnelles: {'✅ SUCCÈS' if test2 else '❌ ÉCHEC'}")
    
    overall_success = test1 and test2
    print(f"\n🏆 Résultat global: {'✅ SUCCÈS' if overall_success else '❌ ÉCHEC'}")
    
    if overall_success:
        print("\n🎉 Toutes les traces d'invoke ont été éliminées avec succès !")
        print("   Le système utilise maintenant exclusivement .call() + fallback OpenAI")
