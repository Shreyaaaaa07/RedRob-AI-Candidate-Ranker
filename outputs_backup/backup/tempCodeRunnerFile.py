print(df["skill_match_score"].describe())

print("\nTop 10 Skill Match Scores:")
print(df["skill_match_score"].sort_values(ascending=False).head(10))