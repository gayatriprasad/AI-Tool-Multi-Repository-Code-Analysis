from multi_repo_analyzer.core.entities import RepositoryInfo, CodeEntity

def mock_entity(name="mock_fn", type="function", path="fake.py", doc="does something"):
    return CodeEntity(
        name=name,
        type=type,
        file_path=path,
        docstring=doc,
        calls=[],
        metadata={}
    )

def mock_repo(name="mock-repo", entities=None):
    return RepositoryInfo(
        name=name,
        path="/tmp/mock",
        language="python",
        entities=entities or [mock_entity()],
        dependencies=["requests"],
        file_hash="abc123",
        build_system=None
    )
