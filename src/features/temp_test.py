import pandas as pd

df = pd.read_parquet("outputs/normalized_candidate_features.parquet")

print(df["skill_match_score"].describe())

print("\nTop 20 Skill Match Scores:")
print(df["skill_match_score"].sort_values(ascending=False).head(20))