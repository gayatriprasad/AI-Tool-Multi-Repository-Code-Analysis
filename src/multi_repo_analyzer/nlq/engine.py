from multi_repo_analyzer.search.semantic import SemanticSearchEngine
from multi_repo_analyzer.nlq.intent_classifier import classify_intent
from multi_repo_analyzer.core.types import CodeChunk

class NLQEngine:
    def __init__(self):
        pass

    def answer(self, query: str, chunks: list[CodeChunk], semantic: SemanticSearchEngine, json_output=False):
        intent = classify_intent(query)
        print(f"[NLQ Engine] Intent classified as: {intent}")

        handler_map = {
            "describe_authentication": self._handle_auth,
            "list_db_interactions": self._handle_db
        }

        if intent in handler_map:
            return handler_map[intent](query, semantic, json_output=json_output)
        return f"Sorry, I couldn't understand or support this question yet. Intent: {intent}"

    def _handle_auth(self, query, semantic: SemanticSearchEngine, json_output=False):
        results = semantic.search(query, top_k=5)
        if json_output:
            return {
                "intent": "describe_authentication",
                "matches": results
            }
        if not results:
            return "No authentication-related logic found."
        return self._format_results("Authentication-related code found:", results)

    def _handle_db(self, query, semantic: SemanticSearchEngine, json_output=False):
        results = semantic.search(query, top_k=5)
        if json_output:
            return {
                "intent": "list_db_interactions",
                "matches": results
            }
        if not results:
            return "No database interaction code found."
        return self._format_results("Database interaction code found:", results)

    def _format_results(self, header: str, results: list[dict]) -> str:
        lines = [header]
        for r in results:
            lines.append(f"{r['file']} (lines {r['start_line']}-{r['end_line']}): {r['summary']}")
        return "\n".join(lines)
