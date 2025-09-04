#!/usr/bin/env python3
"""
Test simple pour vérifier la vérification de robustesse des tools
"""

from lunacore.crew_system import LunaCrewSystem

def test_tools_verification():
    """Test rapide pour voir les logs de vérification"""
    print("🧪 Test de la vérification de robustesse des tools...")
    
    try:
        # Initialiser le système
        system = LunaCrewSystem()
        
        # Créer un projet temporaire pour déclencher l'assignation des tools
        print("\n📋 Assignation des tools en cours...")
        system.current_project_folder = "test_projet"
        
        # Créer les tools bindés par rôle (comme dans generate_project)
        from lunacore.tools_runtime import (
            make_write_file_tool, make_create_project_folder_tool, 
            make_ask_supervisor_help_tool, validate_python_syntax_tool
        )
        
        supervisor_tools = [
            make_create_project_folder_tool(system.current_project_folder, "Superviseur"),
            make_write_file_tool(system.current_project_folder, "Superviseur"),
            make_ask_supervisor_help_tool(system.openai, getattr(system, "openai_client", None)),
            validate_python_syntax_tool,
        ]
        
        # Assigner les tools
        system.agents["supervisor"].tools = supervisor_tools
        
        # Maintenant faire la vérification manuellement
        from lunacore.logger import info, warning, success
        
        print("\n🔧 Vérification manuelle des tools:")
        for idx, tool in enumerate(supervisor_tools):
            tool_name = getattr(tool, 'name', 'unknown')
            tool_type = type(tool).__name__
            
            # Essayer d'extraire le rôle
            tool_role = "unknown"
            if hasattr(tool, '__closure__') and tool.__closure__:
                for cell in tool.__closure__:
                    try:
                        cell_value = cell.cell_contents
                        if isinstance(cell_value, str) and any(role in cell_value for role in ["Superviseur", "Backend", "Frontend", "Data", "QA"]):
                            tool_role = cell_value
                            break
                        if cell_value in ["Superviseur", "Backend", "Frontend", "Data", "QA"]:
                            tool_role = cell_value
                            break
                    except:
                        continue
            
            print(f"  [{idx+1}] {tool_name} (type: {tool_type}, rôle: {tool_role})")
        
        print("✅ Test terminé avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur durant le test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_tools_verification()
    print(f"\n🎯 Résultat: {'✅ SUCCÈS' if success else '❌ ÉCHEC'}")
