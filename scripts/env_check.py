import sys

def safe_import(name):
    try:
        m = __import__(name)
        v = getattr(m, '__version__', repr(m))
        return f"{name}: {v}"
    except Exception as e:
        return f"{name}: import error: {e}"

print('python:', sys.executable)
print('python_version:', sys.version)
print(safe_import('crewai'))
print(safe_import('streamlit'))
print(safe_import('ollama'))
print(safe_import('openai'))
