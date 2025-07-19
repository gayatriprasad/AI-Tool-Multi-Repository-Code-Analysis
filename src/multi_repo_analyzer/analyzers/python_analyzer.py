import os
from typing import List
from ..core.entities import CodeEntity

class PythonAnalyzer:

    @staticmethod
    def analyze_file(file_path: str) -> List[CodeEntity]:
        entities = []

        try:
            with open(file_path, "r") as f:
                lines = f.readlines()

            for idx, line in enumerate(lines):
                line = line.strip()
                if line.startswith("def "):
                    fn_name = line.split("def ")[1].split("(")[0]
                    entity = CodeEntity(
                        name=fn_name,
                        type="function",
                        file_path=file_path,
                        line_number=idx + 1,
                        docstring=None,
                        calls=[]
                    )
                    print(f"✅ Found function: {fn_name} in {file_path}")
                    entities.append(entity)

        except Exception as e:
            print(f"⚠️ Failed to analyze {file_path}: {e}")

        return entities

    @staticmethod
    def detect_dependencies(repo_path: str) -> List[str]:
        """Stub dependency detector"""
        return []

    @staticmethod
    def get_supported_extensions() -> List[str]:
        return [".py"]

    @staticmethod
    def should_analyze_file(file_path: str) -> bool:
        return file_path.endswith(".py")
