import pandas as pd

df = pd.read_parquet("outputs/ranked_candidates.parquet")

print(df.isna().sum().sum())
print(df["candidate_id"].duplicated().sum())

print(df["hybrid_score"].is_monotonic_decreasing)