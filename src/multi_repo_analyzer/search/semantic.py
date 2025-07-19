class SemanticSearchEngine:
    def __init__(self):
        self.index = {}

    def index_repository(self, repo_info):
        self.index[repo_info.name] = repo_info.entities

    def query(self, text: str, top_k: int = 1):
        return [{
            "file_path": "user-service/app.py",
            "content": "def login(): ...",
            "score": 0.95
        }]
