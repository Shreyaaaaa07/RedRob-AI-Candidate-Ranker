import pandas as pd

df = pd.read_parquet("outputs/candidate_features.parquet")

print(df["skill_match_score"].describe())

print(
    df.sort_values(
        "skill_match_score",
        ascending=False
    )[
        ["candidate_id", "skill_match_score"]
    ].head(20)
)