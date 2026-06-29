from pathlib import Path
import json
import pandas as pd


class DashboardService:

    def __init__(self):
        self.output_dir = Path("outputs")

    def get_dashboard_stats(self):
        stats = {
            "total_candidates": 0,
            "processed_candidates": 0,
            "risk_flagged_candidates": 0,
            "average_match_score": None,
            "top_candidate_score": None,
        }

        try:
            parquet_file = self.output_dir / "candidate_features.parquet"

            if parquet_file.exists():

                df = pd.read_parquet(parquet_file)

                stats["total_candidates"] = len(df)
                stats["processed_candidates"] = len(df)

                if "risk_score" in df.columns:
                    stats["risk_flagged_candidates"] = (
                        df["risk_score"] > 0
                    ).sum()

                if "hybrid_score" in df.columns:
                    stats["average_match_score"] = round(
                        float(df["hybrid_score"].mean()), 2
                    )

                    stats["top_candidate_score"] = round(
                        float(df["hybrid_score"].max()), 2
                    )

        except Exception as e:

            stats["error"] = str(e)

        return stats