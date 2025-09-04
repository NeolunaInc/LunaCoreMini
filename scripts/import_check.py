import sys
from pathlib import Path

# Ensure project root is on sys.path so 'lunacore' package can be imported when the
# script is executed from the scripts/ folder.
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from lunacore.crew_system import LunaCrewSystem


if __name__ == '__main__':
    LunaCrewSystem()
    print('Import OK')
