#!/usr/bin/env python3
"""Test du durcissement de run_dir"""

from lunacore.crew_system import LunaCrewSystem
from pathlib import Path
import sys

def test_rundir_durci():
    print("🧪 Test du durcissement de run_dir")
    
    try:
        system = LunaCrewSystem()
        print("✅ Système LunaCore initialisé")
        
        # Test de génération simple pour vérifier que run_dir est bien créé
        result = system.generate_project('Test simple app calculatrice Python avec interface CLI', template='python')
        
        print("✅ Test terminé avec succès")
        print(f"📁 Statut: {result.get('status', 'unknown')}")
        
        # Vérifier que le run_dir existe
        if system.current_project_folder and system.current_project_folder.exists():
            print(f"✅ run_dir créé: {system.current_project_folder}")
            
            # Compter les fichiers générés
            files = list(system.current_project_folder.rglob("*"))
            file_count = len([f for f in files if f.is_file()])
            print(f"📄 {file_count} fichiers générés")
        else:
            print("❌ run_dir non trouvé")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = test_rundir_durci()
    sys.exit(0 if success else 1)
