"""
Job Description Parser - Intelligent JD Feature Extraction

Converts unstructured job descriptions into structured, machine-readable JSON.
Uses rule-based parsing and lightweight NLP (no external APIs or LLMs).

Module: src.features.jd_parser
"""

import json
import logging
import re
from pathlib import Path
from typing import Dict, List, Set, Any, Optional, Tuple
from dataclasses import dataclass, asdict, field
from collections import defaultdict

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class JDFeatures:
    """Structured job description features"""
    
    # Basic role information
    role_title: str = ""
    company_name: str = ""
    location: str = ""
    employment_type: str = ""
    
    # Experience requirements (range with notes)
    required_experience_min: int = 0
    required_experience_max: int = 0
    experience_notes: str = ""
    
    # Skill categories
    must_have_skills: List[str] = field(default_factory=list)
    preferred_skills: List[str] = field(default_factory=list)
    explicitly_unwanted_skills: List[str] = field(default_factory=list)
    
    # Domain expertise
    required_domains: List[str] = field(default_factory=list)
    required_tools: List[str] = field(default_factory=list)
    required_frameworks: List[str] = field(default_factory=list)
    
    # Soft skills and competencies
    required_soft_skills: List[str] = field(default_factory=list)
    required_responsibilities: List[str] = field(default_factory=list)
    
    # Keyword categories for scoring
    evaluation_keywords: Set[str] = field(default_factory=set)
    production_keywords: Set[str] = field(default_factory=set)
    retrieval_keywords: Set[str] = field(default_factory=set)
    vector_database_keywords: Set[str] = field(default_factory=set)
    ranking_keywords: Set[str] = field(default_factory=set)
    startup_keywords: Set[str] = field(default_factory=set)
    open_source_keywords: Set[str] = field(default_factory=set)
    
    # Anti-patterns (disqualifiers)
    anti_patterns: Dict[str, str] = field(default_factory=dict)
    
    # Metadata
    raw_text: str = ""
    parse_timestamp: str = ""
    confidence_score: float = 1.0


class JDParser:
    """
    Rule-based job description parser.
    
    Extracts structured features from unstructured job descriptions.
    Uses pattern matching, keyword extraction, and heuristics.
    """
    
    # Canonical skill vocabulary for clean extraction
    CANONICAL_SKILLS = {
        # Programming languages
        "python", "java", "c++", "go", "rust", "typescript", "javascript",
        "scala", "kotlin", "c#", "r", "julia", "bash", "shell", "sql",
        
        # Vector databases and search infrastructure
        "faiss", "pinecone", "milvus", "qdrant", "weaviate", "elasticsearch",
        "opensearch", "annoy", "lsh", "hnsw", "pgvector",
        "vector database", "vector db", "embedding index", "similarity index",
        "ann index", "approximate nearest neighbor",
        
        # Search and retrieval concepts
        "retrieval", "semantic search", "hybrid search", "dense retrieval",
        "sparse retrieval", "bm25", "lexical search", "neural retrieval",
        "cross-encoder", "bi-encoder", "dense embedding", "sparse embedding",
        "ranking system", "search system", "recommendation system",
        "candidate retrieval", "information retrieval", "ir system",
        "retrieval quality", "search quality", "ranking quality",
        
        # Embedding models and frameworks
        "sentence-transformers", "openai embeddings", "azure openai", "cohere",
        "anthropic", "bge", "e5", "nomic embed", "jina embeddings",
        "contrastive search", "embeddings", "embedding model",
        
        # Evaluation metrics and frameworks
        "ndcg", "mrr", "map", "mean average precision", "mean reciprocal rank",
        "precision@k", "recall@k", "dcg", "idcg", "evaluation framework",
        "evaluation metrics", "evaluation", "metric", "ranking quality",
        "offline evaluation", "online evaluation", "online metric",
        "a/b test", "ab test", "a/b testing", "ab testing",
        
        # ML/AI frameworks and tools
        "pytorch", "tensorflow", "jax", "huggingface", "transformers",
        "scikit-learn", "sklearn", "xgboost", "lightgbm", "catboost",
        "keras", "torch", "fastapi", "flask", "django",
        
        # LLM and integration
        "langchain", "llama-index", "haystack", "vllm", "ollama",
        "openai", "gpt", "claude", "llm", "large language model",
        "fine-tuning", "fine-tune", "prompt engineering", "rag",
        "retrieval-augmented", "rag system",
        
        # Infrastructure and deployment
        "production", "docker", "kubernetes", "aws", "gcp", "azure",
        "ci/cd", "deployment", "scaling", "distributed systems",
        "microservices", "serverless", "inference", "serving", "real-time",
        
        # Databases and data
        "postgres", "postgresql", "mysql", "mongodb", "redis", "dynamodb",
        "s3", "data pipeline", "etl", "feature engineering",
        
        # Other technical concepts
        "system design", "architecture", "design patterns", "algorithms",
        
        # Soft skills and methodologies
        "open source", "github", "git", "agile", "scrum", "leadership",
        "collaboration", "communication", "ownership", "execution",
        "decision making", "product thinking",
    }
    
    # Keyword definitions for different scoring categories
    EVALUATION_KEYWORDS = {
        "ndcg", "mean reciprocal rank", "mrr", "map", "mean average precision",
        "precision@k", "precision@10", "recall@k", "recall@10", "dcg",
        "offline evaluation", "online evaluation", "a/b test", "ab test",
        "a/b testing", "ab testing", "offline benchmark", "online metric",
        "evaluation framework", "eval framework", "evaluation metrics",
        "ranking quality", "retrieval quality", "search quality"
    }
    
    PRODUCTION_KEYWORDS = {
        "production", "deployed", "serving", "scalable", "inference",
        "live users", "real users", "pipeline", "real-time", "realtime",
        "scale", "shipped", "shipping", "released", "launch",
        "production deployment", "in production", "deployed to production",
        "serving models", "inference engine", "production system"
    }
    
    RETRIEVAL_KEYWORDS = {
        "retrieval", "semantic search", "hybrid search", "recommendation",
        "matching", "search ranking", "search system", "information retrieval",
        "ir system", "ranker", "ranking system", "query", "document retrieval",
        "candidate retrieval", "retrieval system", "similarity search"
    }
    
    VECTOR_DATABASE_KEYWORDS = {
        "faiss", "pinecone", "milvus", "qdrant", "weaviate", "elasticsearch",
        "opensearch", "vector db", "vector database", "embedding index",
        "similarity index", "ann index", "annoy", "lsh", "hnsw"
    }
    
    RANKING_KEYWORDS = {
        "ranking", "learning to rank", "ltr", "l2r", "rank", "scoring",
        "learner to rank", "rank algorithm", "ranker", "ranking model",
        "ranking system", "xgboost", "lightgbm", "rank loss", "pointwise",
        "pairwise", "listwise", "ranking loss"
    }
    
    STARTUP_KEYWORDS = {
        "founding", "founding engineer", "startup", "early stage",
        "zero to one", "shipped", "mvp", "minimum viable product",
        "growth stage", "scaling", "rapid growth", "fast pace",
        "startup experience", "early", "founder", "co-founder"
    }
    
    OPEN_SOURCE_KEYWORDS = {
        "github", "open source", "oss", "contributor", "maintainer",
        "pull request", "pr", "commit", "repository", "repo", "git",
        "open source contribution", "github activity", "opensource",
        "open-source"
    }
    
    # Tools and frameworks
    VECTOR_DB_TOOLS = {
        "faiss", "pinecone", "milvus", "qdrant", "weaviate",
        "elasticsearch", "opensearch", "annoy", "pgvector"
    }
    
    LLM_FRAMEWORKS = {
        "langchain", "llama-index", "haystack", "transformers",
        "huggingface", "pytorch", "tensorflow", "jax", "vllm",
        "ollama", "openai", "anthropic", "cohere"
    }
    
    # Anti-patterns (things to watch for)
    ANTI_PATTERNS = {
        "pure_research": {
            "keywords": {"academic", "research only", "research lab", "pure research"},
            "description": "Pure research background without production deployment"
        },
        "langchain_only": {
            "keywords": {"langchain", "openai", "gpt"},
            "description": "Recent (< 12 months) LangChain/OpenAI experience without pre-LLM ML"
        },
        "no_recent_coding": {
            "keywords": {"architect", "tech lead", "principal", "staff", "manager"},
            "description": "No production coding in 18+ months (moved to architecture/management)"
        },
        "title_chaser": {
            "keywords": {"senior", "staff", "principal"},
            "description": "Career path suggests title-optimization rather than growth"
        },
        "framework_only": {
            "keywords": {"tutorial", "demo", "example", "blog"},
            "description": "Focus on framework tutorials rather than systems thinking"
        }
    }
    
    def __init__(self):
        """Initialize parser"""
        self.features = JDFeatures()
    
    def parse_docx(self, filepath: Path) -> JDFeatures:
        """
        Parse job description from DOCX file.
        
        Args:
            filepath: Path to .docx file
            
        Returns:
            JDFeatures object with extracted information
        """
        try:
            from docx import Document
        except ImportError:
            raise ImportError("python-docx required. Install with: pip install python-docx")
        
        try:
            doc = Document(filepath)
            text = "\n".join([p.text for p in doc.paragraphs])
            logger.info(f"Loaded DOCX from {filepath}, {len(text)} characters")
            return self.parse(text)
        except Exception as e:
            logger.error(f"Error reading DOCX {filepath}: {e}")
            raise
    
    def parse(self, text: str) -> JDFeatures:
        """
        Parse job description text.
        
        Args:
            text: Raw job description text
            
        Returns:
            JDFeatures object with extracted information
        """
        self.features = JDFeatures()
        self.features.raw_text = text
        
        # Lowercase for matching (preserve original for extraction)
        text_lower = text.lower()
        
        # Extract basic information
        self._extract_basic_info(text)
        
        # Extract experience requirements
        self._extract_experience(text_lower)
        
        # Extract skills
        self._extract_skills(text_lower)

        # NEW
        self._cleanup_skill_lists()

        self._extract_technical_details(text_lower)
        
        # Extract soft skills
        self._extract_soft_skills(text)
        
        # Extract keywords by category
        self._extract_keywords(text_lower)
        
        # Detect anti-patterns
        self._detect_anti_patterns(text_lower)
        
        # Calculate confidence
        self.features.confidence_score = self._calculate_confidence()
        
        logger.info(f"Parsed JD: {self.features.role_title}, confidence: {self.features.confidence_score:.2f}")
        return self.features
    
    def _extract_basic_info(self, text: str) -> None:
        """Extract role title, company, location, employment type"""
        
        # Extract role title (look for "Job Description:" or similar)
        role_match = re.search(r'(?:Job Description|Position|Role)[:\s]+([^\n]+)', text, re.IGNORECASE)
        if role_match:
            self.features.role_title = role_match.group(1).strip()
        
        # Extract company name
        company_match = re.search(r'(?:Company|Organization)[:\s]+([^\n]+)', text, re.IGNORECASE)
        if company_match:
            self.features.company_name = company_match.group(1).strip()
        
        # Extract location
        location_match = re.search(r'(?:Location)[:\s]+([^\n]+)', text, re.IGNORECASE)
        if location_match:
            self.features.location = location_match.group(1).strip()
        
        # Extract employment type
        if re.search(r'full[- ]?time', text, re.IGNORECASE):
            self.features.employment_type = "Full-time"
        elif re.search(r'part[- ]?time', text, re.IGNORECASE):
            self.features.employment_type = "Part-time"
        elif re.search(r'contract', text, re.IGNORECASE):
            self.features.employment_type = "Contract"
    
    def _extract_experience(self, text_lower: str) -> None:
        """Extract minimum and maximum years of experience"""
        
        # Match patterns like "5-9 years", "5 to 9 years", etc.
        patterns = [
            r'(\d+)\s*(?:to|-)\s*(\d+)\s*years',
            r'(\d+)\s*(?:\+|plus)\s*years',
            r'(\d+)\s*years?\s+of\s+experience'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                if len(match.groups()) == 2:
                    self.features.required_experience_min = int(match.group(1))
                    self.features.required_experience_max = int(match.group(2))
                elif len(match.groups()) == 1:
                    exp = int(match.group(1))
                    self.features.required_experience_min = max(0, exp - 2)
                    self.features.required_experience_max = exp + 3
                break
        
        # Look for experience notes (usually in a dedicated section)
        exp_section = re.search(
            r'(?:what we mean by|experience range|about experience).*?(?=\n\n|\Z)',
            text_lower,
            re.IGNORECASE | re.DOTALL
        )
        if exp_section:
            self.features.experience_notes = exp_section.group(0)[:500]
    
    def _extract_skills(self, text_lower: str) -> None:
        """Extract must-have, preferred, and explicitly unwanted skills"""
        
        # Must-have skills section
        must_have_section = re.search(
            r'(?:must have|absolutely need|required skills|core skills|essentials?)'
            r'\s*(?::|-)?(.+?)(?:(?:prefer|like|optional|nice to have)|$)',
            text_lower,
            re.IGNORECASE | re.DOTALL
        )
        if must_have_section:
            skills_text = must_have_section.group(1)
            self.features.must_have_skills = self._extract_skills_from_text(skills_text)
        
        # Preferred skills section
        preferred_section = re.search(
            r'(?:prefer|like to have|nice to have|optional|bonus)\s*(?::|-)?'
            r'(.+?)(?:(?:do not|not want|explicitly|anti-pattern)|$)',
            text_lower,
            re.IGNORECASE | re.DOTALL
        )
        if preferred_section:
            skills_text = preferred_section.group(1)
            self.features.preferred_skills = self._extract_skills_from_text(skills_text)
        
        # Explicitly unwanted section
        unwanted_section = re.search(
            r'(?:do not want|explicitly|do NOT want|anti-pattern|avoid)\s*(?::|-)?'
            r'(.+?)(?:\Z)',
            text_lower,
            re.IGNORECASE | re.DOTALL
        )
        if unwanted_section:
            skills_text = unwanted_section.group(1)
            self.features.explicitly_unwanted_skills = self._extract_skills_from_text(skills_text)
    
    def _normalize_text(self, text: str) -> str:
        """
        Normalize text for skill matching.
        
        Args:
            text: Raw text to normalize
            
        Returns:
            Normalized text (lowercase, punctuation cleaned)
        """
        # Convert to lowercase
        text = text.lower()
        
        # Replace common separators with spaces
        text = re.sub(r'[—\-–•]', ' ', text)
        
        # Remove extra punctuation but keep alphanumeric and spaces
        text = re.sub(r'[^\w\s@#\+/]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _extract_atomic_skills(self, text: str) -> List[str]:
        """
        Extract clean, atomic skills from text using canonical vocabulary.
        
        This is the core skill extraction logic that prevents full sentences
        from being stored as skills.
        
        Args:
            text: Text to extract skills from (raw, may contain sentence fragments)
            
        Returns:
            Sorted list of clean, unique skills
        """
        found_skills = set()
        
        # Normalize the input text
        normalized_text = self._normalize_text(text)
        
        # For each skill in canonical vocabulary, check if it appears in text
        for skill in self.CANONICAL_SKILLS:
            # Create a word-boundary pattern to match whole skills
            # This prevents "python" from matching "copython" or similar
            pattern = r'\b' + re.escape(skill) + r'\b'
            
            if re.search(pattern, normalized_text):
                found_skills.add(skill)
        
        # Sort and return
        return sorted(list(found_skills))
    
    def _extract_skills_from_text(self, text: str) -> List[str]:
        """
        Extract individual skills from a text section.
        
        Uses the atomic skill extraction method to ensure only clean,
        recognized skills are returned (not full sentences or phrases).
        
        Args:
            text: Raw text from a skills section
            
        Returns:
            Sorted list of clean, unique skills
        """
        # Use the atomic extraction method with canonical vocabulary
        return self._extract_atomic_skills(text)
    
    def _extract_technical_details(self, text_lower: str) -> None:
        """Extract domains, tools, frameworks"""
        
        # Extract domains (what the role focuses on)
        domain_keywords = {
            "ranking", "retrieval", "search", "recommendation",
            "matching", "embeddings", "llm", "ml/ai", "machine learning"
        }
        self.features.required_domains = [
            d for d in domain_keywords if d in text_lower
        ]
        
        # Extract tools (specific technologies)
        self.features.required_tools = [
            tool for tool in self.VECTOR_DB_TOOLS if tool in text_lower
        ]
        
        # Extract frameworks
        self.features.required_frameworks = [
            fw for fw in self.LLM_FRAMEWORKS if fw in text_lower
        ]
    
    def _extract_soft_skills(self, text: str) -> None:
        """Extract soft skills and responsibilities"""
        
        soft_skills = {
            "communication": ["writing", "communicate", "articulate"],
            "product thinking": ["product", "user-focused", "user feedback"],
            "collaboration": ["cross-functional", "teamwork", "collaborate"],
            "ownership": ["ownership", "own", "responsible"],
            "execution": ["execution", "ship", "delivered", "shipped"],
            "decision making": ["decision", "decide", "decisiveness"]
        }
        
        text_lower = text.lower()
        for skill, keywords in soft_skills.items():
            if any(kw in text_lower for kw in keywords):
                self.features.required_soft_skills.append(skill)
        
        # Extract key responsibilities
        resp_section = re.search(
            r'(?:responsibility|would|you.?d|you will)\s*(?::|-)?(.+?)(?=\n\n|\Z)',
            text_lower,
            re.IGNORECASE | re.DOTALL
        )
        if resp_section:
            resp_text = resp_section.group(1)
            lines = resp_text.split('\n')
            for line in lines:
                line = re.sub(r'^[\s•\-\*\d+\.]+', '', line).strip()
                if len(line) > 10 and len(line) < 200:
                    self.features.required_responsibilities.append(line)
    
    def _extract_keywords(self, text_lower: str) -> None:
        """Extract keywords by category for scoring"""
        
        # Evaluation keywords
        self.features.evaluation_keywords = {
            kw for kw in self.EVALUATION_KEYWORDS if kw in text_lower
        }
        
        # Production keywords
        self.features.production_keywords = {
            kw for kw in self.PRODUCTION_KEYWORDS if kw in text_lower
        }
        
        # Retrieval keywords
        self.features.retrieval_keywords = {
            kw for kw in self.RETRIEVAL_KEYWORDS if kw in text_lower
        }
        
        # Vector database keywords
        self.features.vector_database_keywords = {
            kw for kw in self.VECTOR_DATABASE_KEYWORDS if kw in text_lower
        }
        
        # Ranking keywords
        self.features.ranking_keywords = {
            kw for kw in self.RANKING_KEYWORDS if kw in text_lower
        }
        
        # Startup keywords
        self.features.startup_keywords = {
            kw for kw in self.STARTUP_KEYWORDS if kw in text_lower
        }
        
        # Open source keywords
        self.features.open_source_keywords = {
            kw for kw in self.OPEN_SOURCE_KEYWORDS if kw in text_lower
        }
    
    def _detect_anti_patterns(self, text_lower: str) -> None:
        """Detect anti-patterns (disqualifiers)"""
        
        for pattern_name, pattern_info in self.ANTI_PATTERNS.items():
            keywords = pattern_info["keywords"]
            
            if any(kw in text_lower for kw in keywords):
                self.features.anti_patterns[pattern_name] = pattern_info["description"]
    
    def _calculate_confidence(self) -> float:
        """Calculate parsing confidence score (0-1)"""
        score = 0.0
        max_points = 0
        
        # Check for key fields
        if self.features.role_title:
            score += 0.15
        max_points += 0.15
        
        if self.features.required_experience_min > 0:
            score += 0.15
        max_points += 0.15
        
        if self.features.must_have_skills:
            score += 0.15
        max_points += 0.15
        
        if self.features.required_tools or self.features.required_frameworks:
            score += 0.15
        max_points += 0.15
        
        if self.features.evaluation_keywords or self.features.production_keywords:
            score += 0.15
        max_points += 0.15
        
        if self.features.anti_patterns:
            score += 0.10
        max_points += 0.10
        
        return score / max_points if max_points > 0 else 0.5
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary (excluding raw_text)"""
        d = asdict(self.features)
        d.pop('raw_text', None)  # Remove raw text from output
        
        # Convert sets to sorted lists for JSON serialization
        for key in d:
            if isinstance(d[key], set):
                d[key] = sorted(list(d[key]))
        
        return d
    
    def to_json(self, filepath: Optional[Path] = None) -> str:
        """
        Convert to JSON string and optionally save to file.
        
        Args:
            filepath: Optional path to save JSON
            
        Returns:
            JSON string
        """
        d = self.to_dict()
        json_str = json.dumps(d, indent=2)
        
        if filepath:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(json_str)
            logger.info(f"Saved JD features to {filepath}")
        
        return json_str
    
    def _cleanup_skill_lists(self):
        """
        Clean must-have/preferred/unwanted skill lists.
        """

        must = set(self.features.must_have_skills)
        preferred = set(self.features.preferred_skills)
        unwanted = set(self.features.explicitly_unwanted_skills)

        # --------------------------------
        # Remove duplicates
        # --------------------------------
        preferred -= must
        unwanted -= must
        unwanted -= preferred

        # --------------------------------
        # Move alternative technologies
        # --------------------------------

        move_to_preferred = {
            "bge",
            "e5",
            "openai embeddings",
            "map",
            "mrr",
            "ndcg",
            "milvus",
            "weaviate",
            "opensearch",
            "elasticsearch",
        }

        for skill in list(must):
            if skill in move_to_preferred:
                must.remove(skill)
                preferred.add(skill)

        # --------------------------------
        # Collapse vector databases
        # --------------------------------

        vector_dbs = {
            "faiss",
            "pinecone",
            "qdrant",
            "milvus",
            "weaviate",
            "elasticsearch",
            "opensearch",
        }

        found = must & vector_dbs

        if found:
            must -= vector_dbs
            must.add("vector database")
            preferred |= found

        self.features.must_have_skills = sorted(must)
        self.features.preferred_skills = sorted(preferred)
        self.features.explicitly_unwanted_skills = sorted(unwanted)


def parse_jd_file(jd_path: Path, output_path: Optional[Path] = None) -> JDFeatures:
    """
    Convenience function to parse a JD file and optionally save output.
    
    Args:
        jd_path: Path to job description file (.docx or .txt)
        output_path: Optional path to save JSON output
        
    Returns:
        JDFeatures object
    """
    parser = JDParser()
    
    if jd_path.suffix.lower() == '.docx':
        features = parser.parse_docx(jd_path)
    else:
        text = jd_path.read_text(encoding='utf-8')
        features = parser.parse(text)
    
    if output_path:
        parser.to_json(output_path)
    
    return features


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    jd_path = Path("data/job_description.docx")
    output_path = Path("outputs/jd_features.json")
    
    if jd_path.exists():
        features = parse_jd_file(jd_path, output_path)
        print(f"\n✓ Parsed JD: {features.role_title}")
        print(f"  Experience: {features.required_experience_min}-{features.required_experience_max} years")
        print(f"  Must-have skills: {len(features.must_have_skills)}")
        print(f"  Tools: {', '.join(features.required_tools)}")
        print(f"  Anti-patterns detected: {list(features.anti_patterns.keys())}")
    else:
        print(f"JD file not found: {jd_path}")

    