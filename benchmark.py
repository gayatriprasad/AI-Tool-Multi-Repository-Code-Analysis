import time
from multi_repo_analyzer.core.analyzer import MultiRepoAnalyzer
from multi_repo_analyzer.analysis.advanced_cross_repo import perform_comprehensive_analysis

REPOS = [
    "examples/sample_repos/user-service",
    "examples/sample_repos/product-service",
    "examples/sample_repos/inventory-service"
]

if __name__ == "__main__":
    start = time.time()

    analyzer = MultiRepoAnalyzer(enable_semantic_search=False)
    for path in REPOS:
        analyzer.add_repository(path)

    results = perform_comprehensive_analysis(analyzer.repositories)
    duration = time.time() - start

    print(f"⏱️ Analysis completed in {duration:.2f} seconds")
    print(f"Security Score: {results['security_analysis']['security_score']}")
    print(f"Performance Score: {results['performance_analysis']['performance_score']}")
