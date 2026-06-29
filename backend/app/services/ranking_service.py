from pathlib import Path
import pandas as pd


class RankingService:

    def __init__(self):
        BASE_DIR = Path(__file__).resolve().parents[3]
        self.output_dir = BASE_DIR / "outputs"

    def get_rankings(self):

        parquet_file = self.output_dir / "ranked_candidates.parquet"

        if not parquet_file.exists():
            return []

        df = pd.read_parquet(parquet_file)

        # Sort if hybrid score exists
        if "hybrid_score" in df.columns:
            df = df.sort_values(
                by="hybrid_score",
                ascending=False
            )

        # Return top 100 for frontend
        return df.head(100).to_dict(orient="records")