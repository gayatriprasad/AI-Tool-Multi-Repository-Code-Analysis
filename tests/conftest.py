import pytest
import os

@pytest.fixture(scope="session")
def sample_repo_paths():
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "../examples/sample_repos"))
    return {
        "user": os.path.join(base, "user-service"),
        "product": os.path.join(base, "product-service"),
        "inventory": os.path.join(base, "inventory-service")
    }
