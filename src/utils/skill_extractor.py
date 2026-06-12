"""
Skill Extraction Utility - Atomic Skill Detection

Provides reusable functions to extract known technical skills from unstructured text.
Uses a canonical vocabulary of AI/ML technologies to ensure clean, consistent skill detection.

Module: src.utils.skill_extractor
"""

import re
from typing import List, Set

# Canonical skill vocabulary for clean extraction
# This is the single source of truth for recognized technical skills
CANONICAL_SKILLS = {
    # Programming languages
    "python", "java", "c++", "go", "rust", "typescript", "javascript",
    "scala", "kotlin", "c#", "r", "julia", "bash", "shell", "sql",
    
    # Vector databases and search infrastructure
    "faiss", "pinecone", "milvus", "qdrant", "weaviate", "elasticsearch",
    "opensearch", "annoy", "lsh", "hnsw", "pgvector", "pgvecor",
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


def _normalize_text(text: str) -> str:
    """
    Normalize text for skill matching.
    
    Converts to lowercase, removes punctuation, normalizes separators.
    
    Args:
        text: Raw text to normalize
        
    Returns:
        Normalized text
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


def extract_atomic_skills(
    text: str,
    canonical_skills: Set[str] = None,
    return_sorted: bool = True
) -> List[str]:
    """
    Extract clean, atomic skills from unstructured text.
    
    Scans text for known technical skills using a canonical vocabulary.
    Prevents full sentences/phrases from being treated as skills by using
    word-boundary matching.
    
    Args:
        text: Unstructured text (profile summary, job description, headline, etc.)
        canonical_skills: Custom skill vocabulary (defaults to CANONICAL_SKILLS)
        return_sorted: Whether to return sorted list (default: True)
        
    Returns:
        Sorted list of clean, deduplicated skills found in text
        
    Example:
        >>> text = "Strong python and experience with faiss, pinecone for retrieval"
        >>> skills = extract_atomic_skills(text)
        >>> print(skills)
        ['faiss', 'pinecone', 'python', 'retrieval']
    """
    if not text or not isinstance(text, str):
        return []
    
    if canonical_skills is None:
        canonical_skills = CANONICAL_SKILLS
    
    found_skills = set()
    
    # Normalize the input text
    normalized_text = _normalize_text(text)
    
    # For each skill in canonical vocabulary, check if it appears in text
    for skill in canonical_skills:
        # Create a word-boundary pattern to match whole skills
        # This prevents "python" from matching "copython" or similar
        pattern = r'\b' + re.escape(skill) + r'\b'
        
        if re.search(pattern, normalized_text):
            found_skills.add(skill)
    
    # Sort and return
    result = sorted(list(found_skills)) if return_sorted else list(found_skills)
    return result


__all__ = [
    "extract_atomic_skills",
    "CANONICAL_SKILLS",
]
