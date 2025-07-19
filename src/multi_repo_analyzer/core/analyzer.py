# src/multi_repo_analyzer/core/analyzer.py 
"""
Updated main analyzer with JavaScript/TypeScript support and enhanced cross-repository analysis
"""

import os
import hashlib
import logging
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path

from .entities import CodeEntity, RepositoryInfo
from .cache import CacheManager
from ..analyzers import get_analyzer, get_supported_languages, ANALYZER_REGISTRY
from .enhanced_cross_repo import analyze_cross_repository_enhanced

logger = logging.getLogger(__name__)

class MultiRepoAnalyzer:
    """Enhanced multi-repository analyzer with expanded language support"""
    
    def __init__(self, enable_semantic_search: bool = True):
        self.cache = CacheManager()
        self.repositories: Dict[str, RepositoryInfo] = {}
        
        # Initialize semantic search if requested and dependencies available
        self.semantic_search = None
        if enable_semantic_search:
            try:
                from ..search.semantic import SemanticSearchEngine
                self.semantic_search = SemanticSearchEngine()
                logger.info("Semantic search enabled")
            except ImportError as e:
                logger.warning(f"Semantic search disabled due to missing dependencies: {e}")
        
        # Track supported languages
        self.supported_languages = get_supported_languages()
        logger.info(f"Supported languages: {', '.join(self.supported_languages)}")
    
    def add_repository(self, repo_path: str, index_for_search: bool = True) -> str:
        """Add a repository for analysis with enhanced language detection"""
        repo_path = Path(repo_path).resolve()
        
        if not repo_path.exists():
            raise FileNotFoundError(f"Repository path not found: {repo_path}")
        
        # Enhanced language detection
        detected_languages = self._detect_languages(repo_path)
        primary_language = detected_languages[0] if detected_languages else 'unknown'
        
        if primary_language not in self.supported_languages:
            logger.warning(f"Primary language '{primary_language}' not fully supported. Using basic analysis.")
            # Fall back to Python analyzer for basic functionality
            primary_language = 'python'
        
        # Create repository info
        repo_info = RepositoryInfo(
            name=repo_path.name,
            path=str(repo_path),
            language=primary_language,
            file_hash=self._compute_repo_hash(repo_path)
        )
        
        # Check cache first
        # Force re-analysis for debugging
        logger.warning(f"⚠️  Skipping cache for {repo_info.name}, forcing fresh analysis")
        repo_info = self._analyze_repository(repo_info, detected_languages)
        self.cache.save_to_cache(repo_info)


        self.repositories[repo_info.name] = repo_info
        
        # Index for semantic search if enabled
        if index_for_search and self.semantic_search:
            self.semantic_search.index_repository(repo_info)
        
        return repo_info.name
    
    def _detect_languages(self, repo_path: Path) -> List[str]:
        """Enhanced language detection supporting multiple languages"""
        file_counts = {}
        
        # Count files by extension
        for file_path in repo_path.rglob('*'):
            if file_path.is_file() and not any(part.startswith('.') for part in file_path.parts):
                suffix = file_path.suffix.lower()
                file_counts[suffix] = file_counts.get(suffix, 0) + 1
        
        # Language mapping
        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'typescript', 
            '.tsx': 'typescript',
            '.mjs': 'javascript',
            '.cjs': 'javascript',
            '.java': 'java',
            '.go': 'go',
            '.rs': 'rust',
            '.cpp': 'cpp',
            '.c': 'c',
            '.cs': 'csharp',
            '.php': 'php',
            '.rb': 'ruby'
        }
        
        # Count by language
        language_counts = {}
        for ext, count in file_counts.items():
            if ext in language_map:
                lang = language_map[ext]
                language_counts[lang] = language_counts.get(lang, 0) + count
        
        # Sort by file count
        sorted_languages = sorted(language_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Return languages in order of prevalence
        return [lang for lang, count in sorted_languages if count > 0]
    
    def _analyze_repository(self, repo_info: RepositoryInfo, detected_languages: List[str]) -> RepositoryInfo:
        """Analyze repository with multi-language support"""
        logger.info(f"Analyzing repository: {repo_info.name}")
        
        all_entities = []
        all_dependencies = []
        
        # Analyze with each detected language analyzer
        for language in detected_languages:
            if language in self.supported_languages:
                try:
                    analyzer = get_analyzer(language)
                    
                    # Detect dependencies
                    deps = analyzer.detect_dependencies(repo_info.path)
                    all_dependencies.extend(deps)
                    
                    # Analyze files
                    entities = self._analyze_repository_files(Path(repo_info.path), analyzer)
                    all_entities.extend(entities)
                    
                    logger.info(f"  {language}: {len(entities)} entities, {len(deps)} dependencies")
                    
                except Exception as e:
                    logger.error(f"Failed to analyze with {language} analyzer: {e}")
        
        # Update repository info
        repo_info.entities = all_entities
        repo_info.dependencies = list(set(all_dependencies))  # Remove duplicates
        repo_info.build_system = self._detect_build_system(Path(repo_info.path))
        
        # Enhanced analysis for specific languages
        if 'javascript' in detected_languages or 'typescript' in detected_languages:
            repo_info = self._enhance_js_ts_analysis(repo_info)
        
        logger.info(f"Completed analysis: {len(all_entities)} total entities")
        return repo_info
    
    def _analyze_repository_files(self, repo_path: Path, analyzer) -> List[CodeEntity]:
        """Analyze files with the given analyzer"""
        entities = []
        supported_extensions = analyzer.get_supported_extensions()
        
        for file_path in repo_path.rglob('*'):
            if (file_path.is_file() and 
                file_path.suffix in supported_extensions and
                analyzer.should_analyze_file(str(file_path))):
                
                try:
                    file_entities = analyzer.analyze_file(str(file_path))
                    entities.extend(file_entities)
                except Exception as e:
                    logger.debug(f"Failed to analyze {file_path}: {e}")
        
        return entities
    
    def _enhance_js_ts_analysis(self, repo_info: RepositoryInfo) -> RepositoryInfo:
        """Enhanced analysis for JavaScript/TypeScript repositories"""
        try:
            from ..analyzers.javascript import JSTypeScriptEnhancedAnalyzer
            
            enhanced_analyzer = JSTypeScriptEnhancedAnalyzer()
            
            # Detect frameworks
            frameworks = enhanced_analyzer.detect_frameworks(repo_info.path)
            if frameworks:
                repo_info.dependencies.extend([f"framework:{fw}" for fw in frameworks])
                logger.info(f"Detected frameworks: {', '.join(frameworks)}")
            
            # Get package info
            package_info = enhanced_analyzer.get_package_info(repo_info.path)
            if package_info:
                # Add package.json metadata
                repo_info.dependencies.append(f"package_name:{package_info.get('name', 'unknown')}")
                if 'version' in package_info:
                    repo_info.dependencies.append(f"version:{package_info['version']}")
        
        except ImportError:
            logger.debug("Enhanced JS/TS analysis not available")
        
        return repo_info
    
    def _detect_build_system(self, repo_path: Path) -> Optional[str]:
        """Enhanced build system detection"""
        build_files = {
            'package.json': 'npm',
            'yarn.lock': 'yarn',
            'pnpm-lock.yaml': 'pnpm',
            'requirements.txt': 'pip',
            'pyproject.toml': 'poetry',
            'setup.py': 'setuptools',
            'Pipfile': 'pipenv',
            'pom.xml': 'maven',
            'build.gradle': 'gradle',
            'Cargo.toml': 'cargo',
            'go.mod': 'go_modules',
            'Makefile': 'make',
            'CMakeLists.txt': 'cmake'
        }
        
        for build_file, system in build_files.items():
            if (repo_path / build_file).exists():
                return system
        
        return None
    
    def _compute_repo_hash(self, repo_path: Path) -> str:
        """Compute hash of repository for caching"""
        hash_md5 = hashlib.md5()
        
        for file_path in sorted(repo_path.rglob('*')):
            if file_path.is_file() and not any(part.startswith('.') for part in file_path.parts):
                try:
                    # Include file path and modification time
                    hash_md5.update(str(file_path.relative_to(repo_path)).encode())
                    hash_md5.update(str(file_path.stat().st_mtime).encode())
                except Exception:
                    continue
        
        return hash_md5.hexdigest()
    
    def semantic_query(self, query: str, top_k: int = 10, filter_type: Optional[str] = None) -> List[Tuple[CodeEntity, float]]:
        """Perform semantic search across all repositories"""
        if not self.semantic_search:
            raise ValueError("Semantic search not available. Install required dependencies.")
        
        return self.semantic_search.search(query, top_k, filter_type)
    
    def find_similar_code(self, entity: CodeEntity, top_k: int = 5) -> List[Tuple[CodeEntity, float]]:
        """Find code entities similar to the given entity"""
        if not self.semantic_search:
            raise ValueError("Semantic search not available. Install required dependencies.")
        
        return self.semantic_search.find_similar_entities(entity, top_k)
    
    def get_repository_summary(self, repo_name: str) -> Dict[str, Any]:
        """Get enhanced summary information about a repository"""
        if repo_name not in self.repositories:
            raise ValueError(f"Repository not found: {repo_name}")
        
        repo = self.repositories[repo_name]
        entity_counts = {}
        
        for entity in repo.entities:
            entity_counts[entity.type] = entity_counts.get(entity.type, 0) + 1
        
        # Framework detection for JS/TS repos
        frameworks = []
        if repo.language in ['javascript', 'typescript']:
            frameworks = [dep.split(':')[1] for dep in repo.dependencies if dep.startswith('framework:')]
        
        return {
            'name': repo.name,
            'language': repo.language,
            'build_system': repo.build_system,
            'dependencies': [dep for dep in repo.dependencies if not dep.startswith('framework:') and not dep.startswith('package_name:')],
            'frameworks': frameworks,
            'entity_counts': entity_counts,
            'total_entities': len(repo.entities),
            'semantic_search_indexed': self.semantic_search and repo.name in self.semantic_search.indexed_repos,
            'supported_languages': self.supported_languages
        }
    
    def find_entities_by_name(self, entity_name: str, repo_name: Optional[str] = None, entity_type: Optional[str] = None) -> List[CodeEntity]:
        """Enhanced entity search with type filtering"""
        results = []
        
        repos_to_search = [repo_name] if repo_name else self.repositories.keys()
        
        for repo_name in repos_to_search:
            if repo_name in self.repositories:
                repo = self.repositories[repo_name]
                for entity in repo.entities:
                    name_match = entity_name.lower() in entity.name.lower()
                    type_match = entity_type is None or entity.type == entity_type
                    
                    if name_match and type_match:
                        results.append(entity)
        
        return results
    
    def analyze_cross_repo_dependencies(self) -> Dict[str, Any]:
        """Enhanced cross-repository analysis"""
        try:
            # Use enhanced cross-repo analyzer
            enhanced_analysis = analyze_cross_repository_enhanced(self.repositories)
            return enhanced_analysis
        except Exception as e:
            logger.error(f"Enhanced cross-repo analysis failed: {e}")
            # Fallback to basic analysis
            return self._basic_cross_repo_analysis()
    
    def _basic_cross_repo_analysis(self) -> Dict[str, List[str]]:
        """Basic cross-repository dependency analysis (fallback)"""
        cross_deps = {}
        
        for repo_name, repo in self.repositories.items():
            cross_deps[repo_name] = []
            
            # Look for imports that might reference other repositories
            for entity in repo.entities:
                if entity.type == "import":
                    for other_repo_name, other_repo in self.repositories.items():
                        if other_repo_name != repo_name:
                            # Simple heuristic: check if import name contains other repo name
                            if other_repo_name.lower() in entity.name.lower():
                                cross_deps[repo_name].append(other_repo_name)
        
        return {'basic_dependencies': cross_deps}
    
    def get_api_endpoints(self, repo_name: Optional[str] = None) -> List[CodeEntity]:
        """Get API endpoints from repositories"""
        endpoints = []
        
        repos_to_search = [repo_name] if repo_name else self.repositories.keys()
        
        for repo_name in repos_to_search:
            if repo_name in self.repositories:
                repo = self.repositories[repo_name]
                repo_endpoints = [entity for entity in repo.entities if entity.type == 'api_endpoint']
                endpoints.extend(repo_endpoints)
        
        return endpoints
    
    def get_react_components(self, repo_name: Optional[str] = None) -> List[CodeEntity]:
        """Get React components from repositories"""
        components = []
        
        repos_to_search = [repo_name] if repo_name else self.repositories.keys()
        
        for repo_name in repos_to_search:
            if repo_name in self.repositories:
                repo = self.repositories[repo_name]
                repo_components = [entity for entity in repo.entities if entity.type == 'react_component']
                components.extend(repo_components)
        
        return components
    
    def get_language_statistics(self) -> Dict[str, Any]:
        """Get statistics about languages used across repositories"""
        stats = {
            'languages_used': {},
            'total_entities_by_language': {},
            'repositories_by_language': {},
        }
        
        for repo_name, repo in self.repositories.items():
            lang = repo.language
            
            # Count repositories by language
            if lang not in stats['repositories_by_language']:
                stats['repositories_by_language'][lang] = []
            stats['repositories_by_language'][lang].append(repo_name)
            
            # Count entities by language
            if lang not in stats['total_entities_by_language']:
                stats['total_entities_by_language'][lang] = 0
            stats['total_entities_by_language'][lang] += len(repo.entities)
            
            # Count entity types by language
            if lang not in stats['languages_used']:
                stats['languages_used'][lang] = {}
            
            for entity in repo.entities:
                if entity.type not in stats['languages_used'][lang]:
                    stats['languages_used'][lang][entity.type] = 0
                stats['languages_used'][lang][entity.type] += 1
        
        return stats
    
    def save_search_index(self, path: str):
        """Save the semantic search index to disk"""
        if self.semantic_search:
            self.semantic_search.save_index(path)
            logger.info(f"Saved search index to {path}")
        else:
            logger.warning("No semantic search index to save")
    
    def load_search_index(self, path: str):
        """Load the semantic search index from disk"""
        if not self.semantic_search:
            try:
                from ..search.semantic import SemanticSearchEngine
                self.semantic_search = SemanticSearchEngine()
            except ImportError as e:
                logger.error(f"Cannot load search index due to missing dependencies: {e}")
                return
        
        self.semantic_search.load_index(path)
        logger.info(f"Loaded search index from {path}")
    
    def export_analysis_report(self, output_path: str) -> str:
        """Export comprehensive analysis report"""
        report = {
            'summary': {
                'total_repositories': len(self.repositories),
                'supported_languages': self.supported_languages,
                'total_entities': sum(len(repo.entities) for repo in self.repositories.values())
            },
            'repositories': {},
            'language_statistics': self.get_language_statistics(),
            'cross_repository_analysis': self.analyze_cross_repo_dependencies(),
            'api_endpoints': [entity.to_dict_for_serialization() for entity in self.get_api_endpoints()],
            'react_components': [entity.to_dict_for_serialization() for entity in self.get_react_components()]
        }
        
        # Add detailed repository information
        for repo_name, repo in self.repositories.items():
            report['repositories'][repo_name] = {
                'summary': self.get_repository_summary(repo_name),
                'entities': [entity.to_dict_for_serialization() for entity in repo.entities]
            }
        
        # Write report to file
        import json
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Analysis report exported to {output_path}")
        return output_path