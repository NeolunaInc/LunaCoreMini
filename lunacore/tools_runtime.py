from pathlib import Path
from crewai.tools import tool

def make_write_file_tool(run_dir: Path):
    @tool("write_file")
    def write_file(filename: str, content: str) -> str:
        """Écrit un fichier dans le projet"""
        path = Path(run_dir) / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return f"✅ {filename} créé ({len(content)} octets)"
    return write_file

@tool("validate_python")
def validate_python_syntax(code: str) -> str:
    """Valide la syntaxe Python"""
    import ast
    try:
        ast.parse(code)
        return "✅ Syntaxe valide"
    except SyntaxError as e:
        return f"❌ Erreur ligne {e.lineno}: {e.msg}"
