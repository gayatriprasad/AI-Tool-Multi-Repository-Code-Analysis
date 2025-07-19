from multi_repo_analyzer.core.analyzer import MultiRepoAnalyzer
from multi_repo_analyzer.search.semantic import SemanticSearchEngine
import os

BASE_PATH = os.path.join(os.path.dirname(__file__), "sample_repos")
REPO_PATH = os.path.join(BASE_PATH, "user-service")

def main():
    print("🔍 Initializing analyzer with semantic search enabled...")
    analyzer = MultiRepoAnalyzer(enable_semantic_search=True)
    repo_name = analyzer.add_repository(REPO_PATH)

    print(f"✅ Indexed repository: {repo_name}")

    engine: SemanticSearchEngine = analyzer.semantic_search
    if not engine:
        print("⚠️ Semantic engine not initialized. Please check dependencies.")
        return

    # Example query
    query = "How does the login functionality work?"
    print(f"\n💬 Query: {query}\n")

    results = engine.query(query, top_k=3)
    for idx, res in enumerate(results, 1):
        print(f"🔎 Result {idx}")
        print(f"File: {res['file_path']}")
        print(f"Score: {res['score']:.2f}")
        print(f"Context:\n{res['content']}\n")
        print("-" * 60)

if __name__ == "__main__":
    main()
