from ..core.entities import CodeEntity
from typing import List

class JavaScriptTypeScriptAnalyzer:
    def analyze(self, repo_path: str) -> List[CodeEntity]:
        # Minimal stub
        return [
            CodeEntity(
                name="getProduct",
                type="function",
                file_path="product-service/product.js",
                line_number=1,
                docstring="Fetch product details",
                calls=[]
            )
        ]
