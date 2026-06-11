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

    WEIGHTS = {

        "skill_match_score": 0.20,

        "production_ml_score": 0.20,

        "experience_match_score": 0.15,

        "career_stability_score": 0.10,

        "retrieval_score": 0.10,

        "vector_database_score": 0.05,

        "ranking_system_score": 0.05,

        "evaluation_framework_score": 0.05,

        "startup_fit_score": 0.03,

        "open_source_score": 0.02,

        "education_score": 0.02,

        "recruiter_interest_score": 0.01,

        "activity_score": 0.01,

        "engagement_score": 0.01,

        "availability_score": 0.03,

        "behavior_score": 0.02,

        "experience_consistency_score": 0.02,
    }

    RISK_WEIGHT = 0.10

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

        score = 0.0

        for feature, weight in self.WEIGHTS.items():

            if feature not in df.columns:
                logger.warning(f"{feature} missing.")
                continue

            score += df[feature] * weight

        # Penalize risk

        if "risk_score" in df.columns:

            score += df["risk_score"] * self.RISK_WEIGHT

        df["hybrid_score"] = score

        # Scale to 0-100

        df["hybrid_score"] = df["hybrid_score"] * 100

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

        print()

        print("=" * 80)

        print("TOP CANDIDATES")

        print("=" * 80)

        cols = [
            "rank",
            "candidate_id",
            "hybrid_score",
        ]

        print(df[cols].head(k))

        print()

        print("=" * 80)


def main():

    logging.basicConfig(level=logging.INFO)

    ranker = HybridRanker()

    df = ranker.rank()

    ranker.show_top(df)


if __name__ == "__main__":
    main()