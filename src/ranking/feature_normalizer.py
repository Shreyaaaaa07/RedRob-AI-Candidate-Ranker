"""
Feature Normalization Layer

Converts engineered features into a common 0-1 scale.

Input:
    outputs/candidate_features.parquet

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

        for col in self.FEATURE_COLUMNS:

            if col not in df.columns:
                logger.warning(f"{col} missing. Skipping.")
                continue

            vals = pd.to_numeric(
                df[col],
                errors="coerce"
            ).fillna(0)

            raw_max = vals.max()

            # Already normalized
            if raw_max <= 1.0:

                normalized = vals

            # Raw score out of 100
            else:

                normalized = vals / 100.0

            df[col] = normalized.clip(
                lower=0.0,
                upper=1.0,
            )

            logger.info(
                f"{col:35}"
                f" raw_max={raw_max:.4f}"
                f" normalized_max={df[col].max():.4f}"
            )

        self.output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        df.to_parquet(
            self.output_path,
            index=False,
        )

        logger.info(
            f"Saved normalized features -> {self.output_path}"
        )

        return df

    def validate(self, df):

        logger.info("Validation Report")

        for col in self.FEATURE_COLUMNS:

            if col not in df.columns:
                continue

            logger.info(
                f"{col:35}"
                f" min={df[col].min():.4f}"
                f" max={df[col].max():.4f}"
                f" mean={df[col].mean():.4f}"
            )


def main():

    logging.basicConfig(level=logging.INFO)

    normalizer = FeatureNormalizer()

    df = normalizer.normalize()

    normalizer.validate(df)


if __name__ == "__main__":
    main()