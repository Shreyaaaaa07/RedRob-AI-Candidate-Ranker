import pandas as pd
import json

# Load ranked candidates
ranked = pd.read_parquet("outputs/ranked_candidates.parquet")

# Load evidence
with open("outputs/evidence_store.json", "r") as f:
    evidence = json.load(f)

print("=" * 80)

for _, row in ranked.head(5).iterrows():

    cid = row["candidate_id"]

    print(f"\nCandidate: {cid}")
    print(f"Hybrid Score: {row['hybrid_score']:.2f}")

    print("\nEvidence:")

    for e in evidence.get(cid, {}).get("evidence", []):
        print("-", e)

    print("\nRisk Flags:")

    for r in evidence.get(cid, {}).get("risk_flags", []):
        print("-", r)

    print("=" * 80)