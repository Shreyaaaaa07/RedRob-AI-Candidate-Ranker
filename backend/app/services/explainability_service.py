from pathlib import Path
import json
import pandas as pd
from app.config import OUTPUT_DIR




class ExplainabilityService:

    def __init__(self):
        self.output_dir = OUTPUT_DIR

    def get_candidate_evidence(self, candidate_id: str):

        parquet_file = self.output_dir / "ranked_candidates.parquet"

       

        print("Current working directory:", Path.cwd())
        print("Looking for:", parquet_file.resolve())
        print("Exists:", parquet_file.exists())

        if not parquet_file.exists():
            return None

        df = pd.read_parquet(parquet_file)

        print("\n========== DEBUG ==========")
        print("Columns:")
        print(df.columns.tolist())

        print("\nFirst 10 Candidate IDs:")
        print(df["candidate_id"].head(10).tolist())

        print("\nSearching For:")
        print(candidate_id)

        print("===========================\n")

        candidate = df[
            df["candidate_id"].astype(str).str.strip() == candidate_id.strip()
        ]

        if candidate.empty:
            return None

        candidate = candidate.iloc[0]

        evidence = candidate.get("evidence", "{}")

        try:
            if isinstance(evidence, str):
                evidence = json.loads(evidence)
        except Exception:
            evidence = {}

        return {
            "candidate_id": candidate_id,
            "hybrid_score": float(candidate["hybrid_score"]),
            "rank": int(candidate["rank"]),
            "risk_score": float(candidate["risk_score"]),
            "evidence": evidence
        }