from multi_repo_analyzer.core.analyzer import MultiRepoAnalyzer

def test_add_repository_loads_entities(sample_repo_paths):
    analyzer = MultiRepoAnalyzer(enable_semantic_search=False)
    repo_name = analyzer.add_repository(sample_repo_paths["user"])

    assert repo_name == "user-service"
    assert repo_name in analyzer.repositories
    assert len(analyzer.repositories[repo_name].entities) > 0
