
"""
Hybrid Ranking Engine

Combines normalized features into a single recruiter score.

Input:
    outputs/normalized_candidate_features.parquet

Output:
    outputs/ranked_candidates.parquet
"""

from pathlib import Path
import logging

import pandas as pd

logger = logging.getLogger(__name__)


class HybridRanker:

    # ==========================================================
    # Production Weight Configuration
    # Total Weight = 1.00
    # ==========================================================
    WEIGHTS = {

        # ------------------------------------------------------
        # Core Matching (62%)
        # ------------------------------------------------------
        "skill_match_score": 0.22,
        "semantic_similarity_score": 0.10,
        "production_ml_score": 0.18,
        "experience_match_score": 0.12,

        # ------------------------------------------------------
        # Retrieval / Search Expertise (23%)
        # ------------------------------------------------------
        "retrieval_score": 0.08,
        "vector_database_score": 0.05,
        "ranking_system_score": 0.05,
        "evaluation_framework_score": 0.05,

        # ------------------------------------------------------
        # Career Quality (8%)
        # ------------------------------------------------------
        "career_stability_score": 0.05,
        "experience_consistency_score": 0.03,

        # ------------------------------------------------------
        # Startup / OSS (4%)
        # ------------------------------------------------------
        "startup_fit_score": 0.02,
        "open_source_score": 0.02,

        # ------------------------------------------------------
        # Education / Recruiter Signals (3%)
        # ------------------------------------------------------
        "education_score": 0.02,
        "recruiter_interest_score": 0.01,

        # ------------------------------------------------------
        # Activity Signals (3%)
        # ------------------------------------------------------
        "activity_score": 0.01,
        "engagement_score": 0.01,
        "availability_score": 0.01,

        # ------------------------------------------------------
        # Behaviour (1%)
        # ------------------------------------------------------
        "behavior_score": 0.01,
    }

    # Risk penalty
    RISK_WEIGHT = 0.05

    # Skill gate thresholds
    SOFT_SKILL_THRESHOLD = 0.15
    HARD_SKILL_THRESHOLD = 0.10

    def __init__(
        self,
        input_path="outputs/normalized_candidate_features.parquet",
        output_path="outputs/ranked_candidates.parquet",
    ):

        self.input_path = Path(input_path)
        self.output_path = Path(output_path)

    def rank(self):

        logger.info("Loading normalized features...")

        df = pd.read_parquet(self.input_path)

        score = pd.Series(0.0, index=df.index)

        # ======================================================
        # Weighted Feature Aggregation
        # ======================================================
        for feature, weight in self.WEIGHTS.items():

            if feature not in df.columns:
                logger.warning(f"{feature} missing.")
                continue

            score += df[feature] * weight

        # ======================================================
        # Skill Gate
        #
        # Prevent candidates with extremely poor skill overlap
        # from reaching the top purely due to semantic similarity.
        # ======================================================

        if "skill_match_score" in df.columns:

            # Hard penalty (<10%)
            hard_mask = df["skill_match_score"] < self.HARD_SKILL_THRESHOLD
            score.loc[hard_mask] *= 0.70

            # Soft penalty (10%-15%)
            soft_mask = (
                (df["skill_match_score"] >= self.HARD_SKILL_THRESHOLD)
                &
                (df["skill_match_score"] < self.SOFT_SKILL_THRESHOLD)
            )

            score.loc[soft_mask] *= 0.85

        # ======================================================
        # Risk Penalty
        # ======================================================

        if "risk_score" in df.columns:
            score -= df["risk_score"] * self.RISK_WEIGHT

        # Prevent negative scores
        score = score.clip(lower=0)

        df["hybrid_score"] = score * 100

        # ======================================================
        # Ranking
        # ======================================================

        df.sort_values(
            by="hybrid_score",
            ascending=False,
            inplace=True,
        )

        df.reset_index(drop=True, inplace=True)

        df["rank"] = df.index + 1

        self.output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        df.to_parquet(
            self.output_path,
            index=False,
        )

        logger.info(
            f"Saved ranked candidates to {self.output_path}"
        )

        return df

    def show_top(self, df, k=10):
        # Debug/inspection helper. Prefer logging over prints for production safety.
        cols = [
            "rank",
            "candidate_id",
            "hybrid_score",
            "skill_match_score",
            "semantic_similarity_score",
            "production_ml_score",
        ]
        logger.info("=" * 80)
        logger.info("TOP CANDIDATES")
        logger.info("=" * 80)
        logger.info(df[cols].head(k).to_string(index=False))
        logger.info("=" * 80)


def main():

    logging.basicConfig(level=logging.INFO)

    ranker = HybridRanker()

    df = ranker.rank()

    ranker.show_top(df)


if __name__ == "__main__":
    main()

