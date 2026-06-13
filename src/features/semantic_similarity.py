"""
Semantic Similarity Engine

Generates semantic similarity between a Job Description and
candidate profiles using Sentence Transformers.

This version intentionally embeds ONLY technical information
to avoid generic business language dominating similarity.
"""

from typing import List
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from src.utils.skill_extractor import extract_atomic_skills


class SemanticSimilarityEngine:

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
        self.model = SentenceTransformer(model_name)

    # ---------------------------------------------------
    # JD
    # ---------------------------------------------------

    def build_jd_text(self, jd: dict) -> str:
        """
        Build a clean technical representation of the JD.
        """

        parts = []

        # Role title
        if jd.get("role_title"):
            parts.append(jd["role_title"])

        # Technical skills
        parts.extend(jd.get("must_have_skills", []))
        parts.extend(jd.get("preferred_skills", []))

        # Domains
        parts.extend(jd.get("required_domains", []))

        # Tools
        parts.extend(jd.get("required_tools", []))

        # Frameworks
        parts.extend(jd.get("required_frameworks", []))

        # Remove duplicates
        parts = list(dict.fromkeys(
            str(x).strip().lower()
            for x in parts
            if x
        ))

        return "\n".join(parts)

    # ---------------------------------------------------
    # Candidate
    # ---------------------------------------------------

    def build_candidate_text(self, candidate: dict) -> str:
        """
        Build a clean technical representation of a candidate.

        Intentionally ignores long summaries and descriptions.
        """

        profile = candidate.get("profile", {})
        career = candidate.get("career_history", [])
        skills = candidate.get("skills", [])

        parts = []

        # Headline
        if profile.get("headline"):
            parts.append(profile["headline"])

        # Explicit skills
        explicit_skills = [
            s.get("name", "")
            for s in skills
            if s.get("name")
        ]

        parts.extend(explicit_skills)

        # Career titles only
        for job in career:

            if job.get("title"):
                parts.append(job["title"])

        # --------------------------------------------------
        # Extract atomic skills from ALL technical text
        # --------------------------------------------------

        technical_text = []

        technical_text.append(profile.get("headline", ""))
        technical_text.append(profile.get("summary", ""))

        for job in career:

            technical_text.append(job.get("title", ""))
            technical_text.append(job.get("description", ""))

        technical_blob = "\n".join(technical_text)

        atomic_skills = extract_atomic_skills(technical_blob)

        parts.extend(atomic_skills)

        # Remove duplicates
        parts = list(dict.fromkeys(
            str(x).strip().lower()
            for x in parts
            if x
        ))

        return "\n".join(parts)

    # ---------------------------------------------------
    # Encoding
    # ---------------------------------------------------

    def encode_text(self, text: str):

        return self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

    # ---------------------------------------------------
    # Pre-compute JD embedding (call once, reuse for all candidates)
    # ---------------------------------------------------

    def encode_jd(self, jd_text: str) -> np.ndarray:

        return self.encode_text(jd_text)

    # ---------------------------------------------------
    # Single similarity with pre-computed JD embedding
    # ---------------------------------------------------

    def compute_similarity(
        self,
        jd_text: str,
        candidate_text: str
    ) -> float:

        jd_embedding = self.encode_text(jd_text)

        candidate_embedding = self.encode_text(candidate_text)

        similarity = cosine_similarity(
            [jd_embedding],
            [candidate_embedding]
        )[0][0]

        similarity = float(np.clip(similarity, 0.0, 1.0))

        return similarity * 100

    def compute_similarity_with_jd_embedding(
        self,
        jd_embedding: np.ndarray,
        candidate_text: str
    ) -> float:

        candidate_embedding = self.encode_text(candidate_text)

        similarity = cosine_similarity(
            [jd_embedding],
            [candidate_embedding]
        )[0][0]

        similarity = float(np.clip(similarity, 0.0, 1.0))

        return similarity * 100

    # ---------------------------------------------------
    # Batch similarity
    # ---------------------------------------------------

    def batch_compute(
        self,
        jd_text: str,
        candidate_texts: List[str]
    ) -> List[float]:

        jd_embedding = self.encode_text(jd_text)

        candidate_embeddings = self.model.encode(
            candidate_texts,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        similarities = cosine_similarity(
            [jd_embedding],
            candidate_embeddings
        )[0]

        similarities = np.clip(similarities, 0.0, 1.0)

        return (similarities * 100).tolist()