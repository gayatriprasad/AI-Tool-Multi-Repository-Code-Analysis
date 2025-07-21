import argparse
import json
from pathlib import Path
from multi_repo_analyzer.core.analyzer import MultiRepoAnalyzer

def main():
    parser = argparse.ArgumentParser(description="Multi-Repository Code Analysis CLI")
    parser.add_argument("repo_path", help="Path to the repository to analyze")
    parser.add_argument("--query", help="Natural language question about the codebase")
    parser.add_argument("--report", help="Path to export analysis report (JSON)", default=None)
    parser.add_argument("--no-semantic", action="store_true", help="Disable semantic search indexing")
    parser.add_argument("--no-cache", action="store_true", help="Disable index caching")
    parser.add_argument("--json-output", action="store_true", help="Output response in structured JSON")

    args = parser.parse_args()
    repo_path = Path(args.repo_path).resolve()

    if not repo_path.exists():
        print(f"[Error] Repository path not found: {repo_path}")
        return

    analyzer = MultiRepoAnalyzer(
        enable_semantic_search=not args.no_semantic,
        use_cache=not args.no_cache
    )

    print(f"[CLI] Indexing repository at: {repo_path}")
    analyzer.run(repo_path)

    if args.query:
        print(f"[CLI] Answering question: {args.query}")
        result = analyzer.answer(args.query, json_output=args.json_output)

        if args.json_output and isinstance(result, dict):
            print(json.dumps(result, indent=2))
        else:
            print("\n[Answer]")
            print(result)

if __name__ == "__main__":
    main()
