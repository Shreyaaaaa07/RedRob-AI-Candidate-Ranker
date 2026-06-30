import pandas as pd

from app.config import OUTPUT_DIR


class AnalyticsService:

    def __init__(self):
        self.output_dir = OUTPUT_DIR

    def get_analytics(self):

        parquet_file = self.output_dir / "ranked_candidates.parquet"

        if not parquet_file.exists():
            return {
                "total_candidates": 0,
                "average_score": 0,
                "top_score": 0,
                "risk_candidates": 0,
                "score_distribution": {},
                "top_skills": [],
            }

        df = pd.read_parquet(parquet_file)

        total_candidates = len(df)

        average_score = round(
            float(df["hybrid_score"].mean()), 2
        )

        top_score = round(
            float(df["hybrid_score"].max()), 2
        )

        risk_candidates = int(
            (df["risk_score"] > 0).sum()
        )

        score_distribution = {
            "80-100": int(((df["hybrid_score"] >= 80)).sum()),
            "60-79": int(((df["hybrid_score"] >= 60) &
                          (df["hybrid_score"] < 80)).sum()),
            "40-59": int(((df["hybrid_score"] >= 40) &
                          (df["hybrid_score"] < 60)).sum()),
            "0-39": int((df["hybrid_score"] < 40).sum()),
        }

        top_skills = [
            "Python",
            "Machine Learning",
            "LLMs",
            "Vector Databases",
            "Retrieval",
            "Transformers",
        ]

        return {
            "total_candidates": total_candidates,
            "average_score": average_score,
            "top_score": top_score,
            "risk_candidates": risk_candidates,
            "score_distribution": score_distribution,
            "top_skills": top_skills,
        }