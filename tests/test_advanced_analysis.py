from multi_repo_analyzer.analysis.advanced_cross_repo import perform_comprehensive_analysis
from multi_repo_analyzer.core.analyzer import MultiRepoAnalyzer

def test_comprehensive_analysis_outputs_scores(sample_repo_paths):
    analyzer = MultiRepoAnalyzer(enable_semantic_search=False)
    for path in sample_repo_paths.values():
        analyzer.add_repository(path)
    
    results = perform_comprehensive_analysis(analyzer.repositories)
    
    assert "security_analysis" in results
    assert "performance_analysis" in results
    assert isinstance(results["security_analysis"]["security_score"], float)
    assert isinstance(results["performance_analysis"]["performance_score"], float)
