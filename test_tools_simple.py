#!/usr/bin/env python3
"""Test simple pour vérifier que les tools runtime fonctionnent"""

from lunacore.tools_runtime import make_write_file_tool, make_create_project_folder_tool
from pathlib import Path

def test_tools_simple():
    print("🧪 Test simple des tools runtime")
    
    # Créer les tools
    run_dir = Path("test_tools_simple")
    run_dir.mkdir(exist_ok=True)
    
    write_tool = make_write_file_tool(run_dir, "Superviseur")
    folder_tool = make_create_project_folder_tool(run_dir, "Superviseur")
    
    # Test écriture superviseur (doit marcher)
    result1 = write_tool("plan.json", '{"test": "content"}')
    print(f"✅ Superviseur écrit plan.json: {result1}")
    
    # Test écriture autre agent (doit échouer pour plan.json)
    write_tool_backend = make_write_file_tool(run_dir, "Backend")
    result2 = write_tool_backend("plan.json", '{"hack": "attempt"}')
    print(f"❌ Backend tente plan.json: {result2}")
    
    # Test fichier normal (doit marcher)
    result3 = write_tool_backend("app.py", 'print("Hello")')
    print(f"✅ Backend écrit app.py: {result3}")
    
    print("✅ Tests tools runtime réussis !")

if __name__ == "__main__":
    test_tools_simple()
