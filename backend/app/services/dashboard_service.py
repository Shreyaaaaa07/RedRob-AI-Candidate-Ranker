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
            "top_candidates": [],
            "ai_insights": [],
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

                    high_score = 60

                    stats["ai_insights"] = [
                        f"{stats['total_candidates'] - stats['risk_flagged_candidates']} candidates are low risk.",
                        f"Average hybrid score is {stats['average_match_score']}.",
                        f"{len(df[df['hybrid_score'] >= high_score])} candidates scored above {high_score}.",
                        f"{stats['risk_flagged_candidates']} candidates require recruiter review."
                    ]

                    top_df = (
                        df.sort_values("hybrid_score", ascending=False)
                        .head(5)
                    )

                    stats["ai_insights"].append(
                        f"Top candidate is {top_df.iloc[0]['candidate_id']} with score {top_df.iloc[0]['hybrid_score']:.2f}."
                    )

                    stats["top_candidates"] = []

                    for _, row in top_df.iterrows():

                        stats["top_candidates"].append(
                            {
                                "rank": int(row["rank"]),
                                "candidate_id": row["candidate_id"],
                                "hybrid_score": round(float(row["hybrid_score"]), 2),
                            }
                        )

        except Exception as e:

            stats["error"] = str(e)

        return stats