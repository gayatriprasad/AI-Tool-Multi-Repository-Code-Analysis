import re
from typing import List

INTENT_RULES = {
    "summarize_repo": [
        "summarize", "overview", "explain.*repo", "what.*does.*repo.*do"
    ],
    "get_api_endpoints": [
        "api", "endpoint", "rest.*expose", "routes", "available.*methods"
    ],
    "trace_data_flow": [
        "data flow", "how.*data.*moves", "track.*data", "input.*to.*output"
    ],
    "trace_control_flow": [
        "control flow", "call chain", "execution path", "sequence of calls"
    ],
    "find_entity_usage": [
        "where.*(class|function|variable|entity).*used",
        "usage of", "references to", "who uses"
    ],
    "describe_authentication": [
        "login", "authentication", "auth flow", "jwt", "verify credentials"
    ]
}

def classify_intent(query: str) -> str:
    q = query.lower()
    if "login" in q or "authentication" in q:
        return "describe_authentication"
    elif "product" in q and "database" in q or "table" in q:
        return "list_db_interactions"
    else:
        return "unknown_intent"


# Example for testing
if __name__ == "__main__":
    test_queries = [
        "Summarize this repo",
        "What APIs do we expose?",
        "Where is login handled?",
        "How does data flow in this system?",
        "Explain control flow",
        "How is the product entity used?",
        "Tell me about JWT verification"
    ]
    for q in test_queries:
        print(f"{q} -> {classify_intent(q)}")
