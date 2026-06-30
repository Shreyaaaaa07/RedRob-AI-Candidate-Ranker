from app.config import OUTPUT_DIR
import pandas as pd


class DashboardService:

    def __init__(self):
        self.output_dir = OUTPUT_DIR

    def get_dashboard_stats(self):

        stats = {
            "total_candidates": 0,
            "processed_candidates": 0,
            "risk_flagged_candidates": 0,
            "average_match_score": None,
            "top_candidate_score": None,
        }

        try:

            parquet_file = self.output_dir / "ranked_candidates.parquet"

            if parquet_file.exists():

                df = pd.read_parquet(parquet_file)

                stats["total_candidates"] = len(df)
                stats["processed_candidates"] = len(df)

                if "risk_score" in df.columns:
                    stats["risk_flagged_candidates"] = int(
                        (df["risk_score"] > 0).sum()
                    )

                if "hybrid_score" in df.columns:

                    stats["average_match_score"] = round(
                        float(df["hybrid_score"].mean()),
                        2,
                    )

                    stats["top_candidate_score"] = round(
                        float(df["hybrid_score"].max()),
                        2,
                    )

        except Exception as e:

            stats["error"] = str(e)

        return stats