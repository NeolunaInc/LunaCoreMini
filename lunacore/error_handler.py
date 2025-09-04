def safe_execute(func, *args, fallback=None, error_msg="operation", **kwargs):
    """Exécute une fonction avec gestion d'erreur simple"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print(f"❌ Erreur {error_msg}: {e}")
        return fallback

def with_timeout(func, timeout_seconds=30):
    """Wrapper simple pour timeout (pas d'implémentation complexe)"""
    return func

def handle_llm_error(e):
    """Gestion simple des erreurs LLM"""
    return f"Erreur LLM: {e}"

# Classes d'erreur simples
class LunaError(Exception): pass
class AgentError(LunaError): pass  
class LLMError(LunaError): pass
class TimeoutError(LunaError): pass

class ErrorContext:
    def __init__(self, operation, timeout=None):
        self.operation = operation
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"❌ Erreur dans {self.operation}: {exc_val}")
        return False
