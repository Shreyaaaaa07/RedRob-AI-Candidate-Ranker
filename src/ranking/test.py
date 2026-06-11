import pandas as pd

df = pd.read_parquet("outputs/ranked_candidates.parquet")

cols = [
    "candidate_id",
    "hybrid_score",
    "skill_match_score",
    "experience_match_score",
    "production_ml_score",
    "retrieval_score",
    "career_stability_score",
    "education_score",
    "behavior_score",
    "risk_score"
]

print(df[cols].head(5))