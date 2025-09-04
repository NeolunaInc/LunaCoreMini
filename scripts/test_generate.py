import sys
from pathlib import Path

# Ensure project root is on sys.path so 'lunacore' package can be imported when the
# script is executed as a script (sys.path[0] would otherwise be the scripts/ folder).
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from lunacore.crew_system import LunaCrewSystem

brief = "Crée une API FastAPI pour gérer une bibliothèque (livres, auteurs, prêts)"
template = "fastapi"

s = LunaCrewSystem()
result = s.generate_project(brief, template)
print('status:', result.get('status'))
print('execution_time:', result.get('execution_time'))
print('agents_count:', result.get('agents_count'))
print('tasks_count:', result.get('tasks_count'))
print('files_count:', len(result.get('files', {})))
for name in list(result.get('files', {}).keys())[:10]:
    print(' -', name)
