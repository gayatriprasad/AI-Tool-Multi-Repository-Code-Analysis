from multi_repo_analyzer.core.analyzer import MultiRepoAnalyzer

def test_semantic_search_query_returns_results(sample_repo_paths):
    analyzer = MultiRepoAnalyzer(enable_semantic_search=True)
    analyzer.add_repository(sample_repo_paths["user"])

    engine = analyzer.semantic_search
    assert engine is not None

    results = engine.query("How does login work?")
    assert isinstance(results, list)
    assert len(results) > 0
    assert "content" in results[0]
