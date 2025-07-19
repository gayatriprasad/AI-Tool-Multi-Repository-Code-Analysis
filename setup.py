#!/usr/bin/env python3
"""
Setup configuration for AI Multi-Repository Code Analysis Tool
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read long description from README.md if present
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

def read_requirements(filename):
    req_path = Path(__file__).parent / filename
    if req_path.exists():
        return req_path.read_text().strip().split('\n')
    return []

# Base requirements
install_requires = read_requirements("requirements.txt")

# Optional extras
ai_extras = [
    "sentence-transformers>=2.2.0",
    "faiss-cpu>=1.7.3",
    "transformers>=4.21.0",
    "torch>=1.12.0",
    "openai>=1.0.0",
    "networkx>=2.8.0",
    "matplotlib>=3.5.0",
    "plotly>=5.10.0",
    "tree-sitter>=0.20.0",
    "tree-sitter-python>=0.20.0",
    "tree-sitter-javascript>=0.20.0",
    "tree-sitter-typescript>=0.20.0"
]

dev_extras = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "black>=22.0.0",
    "isort>=5.10.0",
    "flake8>=5.0.0",
    "mypy>=0.990",
    "pre-commit>=2.20.0"
]

setup(
    name="ai-multi-repo-analyzer",
    version="1.0.0",
    author="AI Multi-Repository Analysis Team",
    author_email="contact@multirepotool.com",
    description="AI-powered tool for analyzing and querying multiple code repositories using natural language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gayatriprasad/AI-Tool-Multi-Repository-Code-Analysis",
    project_urls={
        "Bug Tracker": "https://github.com/gayatriprasad/AI-Tool-Multi-Repository-Code-Analysis/issues",
        "Documentation": "https://github.com/gayatriprasad/AI-Tool-Multi-Repository-Code-Analysis/docs",
        "Source Code": "https://github.com/gayatriprasad/AI-Tool-Multi-Repository-Code-Analysis",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=install_requires,
    extras_require={
        "ai": ai_extras,
        "dev": dev_extras,
        "all": ai_extras + dev_extras,
    },
    entry_points={
        "console_scripts": [
            "multi-repo-analyzer=multi_repo_analyzer.cli.main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[
        "code-analysis",
        "artificial-intelligence", 
        "natural-language-processing",
        "semantic-search",
        "repository-analysis",
        "developer-tools",
        "multi-repository"
    ]
)
