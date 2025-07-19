from .python_analyzer import PythonAnalyzer
from .js_ts_analyzer import JavaScriptTypeScriptAnalyzer

ANALYZER_REGISTRY = {
    "python": PythonAnalyzer,
    "javascript": JavaScriptTypeScriptAnalyzer,
    "typescript": JavaScriptTypeScriptAnalyzer,
}

def get_supported_languages():
    return list(ANALYZER_REGISTRY.keys())

def get_analyzer(language: str):
    return ANALYZER_REGISTRY.get(language)
