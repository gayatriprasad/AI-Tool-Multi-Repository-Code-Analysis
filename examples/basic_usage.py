from multi_repo_analyzer.core.analyzer import MultiRepoAnalyzer
from multi_repo_analyzer.analysis.advanced_cross_repo import perform_comprehensive_analysis

import os

# Path to sample repos
BASE_PATH = os.path.join(os.path.dirname(__file__), "sample_repos")

REPO_PATHS = [
    os.path.join(BASE_PATH, "user-service"),
    os.path.join(BASE_PATH, "product-service"),
    os.path.join(BASE_PATH, "inventory-service"),
]

def main():
    analyzer = MultiRepoAnalyzer(enable_semantic_search=False)

    print("🔍 Adding sample repositories...")
    for repo_path in REPO_PATHS:
        repo_name = analyzer.add_repository(repo_path)
        print(f"  ✅ Added: {repo_name}")

    print("\n⚙️ Running comprehensive cross-repo analysis...")
    results = perform_comprehensive_analysis(analyzer.repositories)

    print("\n📊 Summary:")
    print(f"  Security Score: {results['security_analysis']['security_score']}/100")
    print(f"  Performance Score: {results['performance_analysis']['performance_score']}/100")
    print(f"  Architecture Score: {results['architectural_analysis']['architecture_quality_score']}/100")
    print(f"  Risk Score: {results['risk_assessment']['overall_risk_score']}/100 ({results['risk_assessment']['risk_level']})")

    print("\n🚨 Top Security Issues:")
    for issue in results['security_analysis']['issues'][:3]:
        print(f"  [{issue['severity'].upper()}] {issue['type']} in {issue['file_path']} @ line {issue['line_number']}")

    print("\n🚧 Top Performance Issues:")
    for issue in results['performance_analysis']['issues'][:3]:
        print(f"  [{issue['impact'].upper()}] {issue['type']} in {issue['file_path']}")

    print("\n🏗️ Architectural Patterns Detected:")
    for pattern in results['architectural_analysis']['detected_patterns']:
        print(f"  {pattern['pattern_type']} (confidence: {pattern['confidence']:.2f})")

    print("\n✅ Done.")

if __name__ == "__main__":
    main()
