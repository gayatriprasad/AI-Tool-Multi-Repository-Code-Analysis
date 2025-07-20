import os
import pickle
import hashlib
from multi_repo_analyzer.core.types import CodeChunk
from multi_repo_analyzer.search.embedding import load_embedding_model
from multi_repo_analyzer.search.embedding import embed_chunks
import numpy as np


class SemanticSearchEngine:
    def __init__(self, model=None, use_cache=True, cache_dir=".cache"):
        
        self.model = model or load_embedding_model()
        self.index = []
        self.use_cache = use_cache
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)


    def _get_cache_path(self, repo_path: str):
        key = hashlib.md5(repo_path.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{key}.pkl")

    def save_index(self, repo_path: str):
        if not self.index:
            return
        path = self._get_cache_path(repo_path)
        with open(path, "wb") as f:
            pickle.dump(self.index, f)

    def load_index(self, repo_path: str):
        path = self._get_cache_path(repo_path)
        if os.path.exists(path):
            with open(path, "rb") as f:
                self.index = pickle.load(f)
                return True
        return False

    def index_codebase(self, repo_path: str, code_chunks):
        if self.use_cache and self.load_index(repo_path):
            print("[Index Persistence] Loaded index from cache.")
            return
        print("[Semantic Indexing] Computing fresh index...")
        self.index = embed_chunks(code_chunks, self.model)
        if self.use_cache:
            self.save_index(repo_path)

    def search(self, query: str, top_k: int = 5):
        if not self.index:
            print("[Semantic Search] No index found. Run indexing first.")
            return []

        query_vec = self.model.encode(query)
        scores = [np.dot(query_vec, vec["embedding"]) for vec in self.index]
        top_indices = np.argsort(scores)[::-1][:top_k]

        results = []
        for i in top_indices:
            item = self.index[i]
            chunk: CodeChunk = item["chunk"]
            results.append({
                "file": chunk.file,
                "start_line": chunk.start_line,
                "end_line": chunk.end_line,
                "summary": chunk.content[:200].strip().replace("\n", " "),
                "score": float(scores[i])  # 👈 Cast to built-in float
            })

        return results
