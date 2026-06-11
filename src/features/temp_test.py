import pandas as pd

df = pd.read_parquet("outputs/candidate_features.parquet")

print(df["experience_match_score"].describe())

print(df.nlargest(10, "experience_match_score")[
    ["experience_match_score"]
])

print(df["experience_consistency_score"].describe())