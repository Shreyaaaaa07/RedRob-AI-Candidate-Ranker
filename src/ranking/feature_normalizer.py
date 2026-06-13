"""
Feature Normalization Layer

Converts all engineered features into a common 0-1 scale
before they are consumed by the Hybrid Ranking Engine.

Input:
    outputs/candidate_features_with_semantic.parquet

Output:
    outputs/normalized_candidate_features.parquet
"""

from pathlib import Path
import logging

import pandas as pd

logger = logging.getLogger(__name__)


class FeatureNormalizer:

    FEATURE_COLUMNS = [
        "experience_match_score",
        "skill_match_score",
        "production_ml_score",
        "retrieval_score",
        "semantic_similarity_score",
        "vector_database_score",
        "ranking_system_score",
        "evaluation_framework_score",
        "startup_fit_score",
        "open_source_score",
        "education_score",
        "career_stability_score",
        "experience_consistency_score",
        "recruiter_interest_score",
        "activity_score",
        "engagement_score",
        "availability_score",
        "behavior_score",
        "risk_score",
    ]

    def __init__(
        self,
        input_path="outputs/candidate_features.parquet",
        output_path="outputs/normalized_candidate_features.parquet",
    ):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)

    def normalize(self):

        logger.info("Loading feature vectors...")

        df = pd.read_parquet(self.input_path)

        logger.info(f"Loaded {len(df)} candidates")

        # Normalize every score column
        for col in self.FEATURE_COLUMNS:

            if col not in df.columns:
                logger.warning(f"{col} not found. Skipping.")
                continue

            df[col] = (
                pd.to_numeric(df[col], errors="coerce")
                .fillna(0)
                .clip(0, 100)
                / 100.0
            )

        # Keep risk_score as-is.
        # 0 = Low Risk
        # 1 = High Risk
        # The HybridRanker will subtract it.

        self.output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        df.to_parquet(
            self.output_path,
            index=False
        )

        logger.info(
            f"Normalized features saved to {self.output_path}"
        )

        return df

    def validate(self, df):

        print("\n========== NORMALIZATION REPORT ==========\n")

        for col in self.FEATURE_COLUMNS:

            if col not in df.columns:
                continue

            print(
                f"{col:35}"
                f"min={df[col].min():.3f}   "
                f"max={df[col].max():.3f}   "
                f"mean={df[col].mean():.3f}"
            )

        print("\n==========================================\n")


def main():

    logging.basicConfig(level=logging.INFO)

    normalizer = FeatureNormalizer()

    df = normalizer.normalize()

    normalizer.validate(df)


if __name__ == "__main__":
    main()