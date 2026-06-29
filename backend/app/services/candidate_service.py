from pathlib import Path
import json
import pandas as pd


class CandidateService:

    def __init__(self):
        BASE_DIR = Path(__file__).resolve().parents[3]
        self.output_dir = BASE_DIR / "outputs"

    def get_candidate(self, candidate_id: str):

        parquet_file = self.output_dir / "ranked_candidates.parquet"

        if not parquet_file.exists():
            return None

        df = pd.read_parquet(parquet_file)

        candidate = df[df["candidate_id"] == candidate_id]

        if candidate.empty:
            return None

        candidate = candidate.iloc[0].to_dict()

        # Convert evidence string into JSON
        if "evidence" in candidate:
            try:
                candidate["evidence"] = json.loads(candidate["evidence"])
            except:
                pass

        # Convert risk flags string into list
        if "risk_flags" in candidate:
            try:
                candidate["risk_flags"] = json.loads(candidate["risk_flags"])
            except:
                candidate["risk_flags"] = []

        return candidate