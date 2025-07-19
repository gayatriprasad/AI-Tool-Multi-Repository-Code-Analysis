from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class CodeEntity:
    name: str
    type: str
    file_path: str
    line_number: int
    docstring: Optional[str] = None
    calls: Optional[List[str]] = field(default_factory=list)

    def to_dict_for_serialization(self):
        return {
            "name": self.name,
            "type": self.type,
            "file_path": self.file_path,
            "line_number": self.line_number,
            "docstring": self.docstring,
            "calls": self.calls,
        }

@dataclass
class RepositoryInfo:
    name: str
    path: str
    language: str
    file_hash: str
    entities: List[CodeEntity] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    build_system: Optional[str] = None
