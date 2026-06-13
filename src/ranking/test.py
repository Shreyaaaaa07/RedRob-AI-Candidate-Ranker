import pandas as pd

raw = pd.read_parquet("outputs/candidate_features.parquet")
norm = pd.read_parquet("outputs/normalized_candidate_features.parquet")

cid = raw.loc[raw["skill_match_score"].idxmax(), "candidate_id"]

print("Candidate:", cid)

print("RAW:",
      raw.loc[raw["candidate_id"] == cid, "skill_match_score"].values[0])

print("NORM:",
      norm.loc[norm["candidate_id"] == cid, "skill_match_score"].values[0])

print("EXPECTED:",
      raw.loc[raw["candidate_id"] == cid, "skill_match_score"].values[0] / 100)