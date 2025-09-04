#!/usr/bin/env python3
"""
Test spécifique pour vérifier que les annotations de rôle fonctionnent
"""

from lunacore.crew_system import LunaCrewSystem
from lunacore.tools_runtime import make_write_file_tool, make_create_project_folder_tool

def test_tool_annotations():
    """Test des annotations _lunacore_role"""
    print("🧪 Test des annotations de rôle des tools...")
    
    # Test des tools individuels
    write_tool = make_write_file_tool("test_project", "Superviseur")
    folder_tool = make_create_project_folder_tool("test_project", "Superviseur")
    
    print(f"  write_tool._lunacore_role = {getattr(write_tool, '_lunacore_role', 'NOT_FOUND')}")
    print(f"  write_tool._lunacore_kind = {getattr(write_tool, '_lunacore_kind', 'NOT_FOUND')}")
    print(f"  folder_tool._lunacore_role = {getattr(folder_tool, '_lunacore_role', 'NOT_FOUND')}")
    print(f"  folder_tool._lunacore_kind = {getattr(folder_tool, '_lunacore_kind', 'NOT_FOUND')}")
    
    # Test de la fonction _tool_role
    system = LunaCrewSystem()
    
    write_role = system._tool_role(write_tool)
    folder_role = system._tool_role(folder_tool)
    
    print(f"  system._tool_role(write_tool) = {write_role}")
    print(f"  system._tool_role(folder_tool) = {folder_role}")
    
    if write_role == "Superviseur" and folder_role == "Superviseur":
        print("✅ Annotations fonctionnent correctement !")
        return True
    else:
        print("❌ Problème avec les annotations")
        return False

if __name__ == "__main__":
    success = test_tool_annotations()
    print(f"\n🎯 Résultat: {'✅ SUCCÈS' if success else '❌ ÉCHEC'}")
