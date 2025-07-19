import json
import os

class CacheManager:
    def __init__(self, cache_dir=".cache"):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def get_cache_path(self, file_hash: str) -> str:
        return os.path.join(self.cache_dir, f"{file_hash}.json")

    def save_to_cache(self, repo_info):
        path = self.get_cache_path(repo_info.file_hash)
        with open(path, "w") as f:
            json.dump({
                "name": repo_info.name,
                "path": repo_info.path,
                "language": repo_info.language,
                "file_hash": repo_info.file_hash,
                "entities": [e.to_dict_for_serialization() for e in repo_info.entities],
                "dependencies": repo_info.dependencies,
                "build_system": repo_info.build_system
            }, f)

    def load_from_cache(self, file_hash: str):
        path = self.get_cache_path(file_hash)
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
                from .entities import CodeEntity, RepositoryInfo
                return RepositoryInfo(
                    name=data["name"],
                    path=data["path"],
                    language=data["language"],
                    file_hash=data["file_hash"],
                    entities=[CodeEntity(**e) for e in data["entities"]],
                    dependencies=data["dependencies"],
                    build_system=data["build_system"]
                )
        return None

    def is_cached(self, file_hash: str) -> bool:
        return os.path.exists(self.get_cache_path(file_hash))
