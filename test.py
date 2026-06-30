import pandas as pd

print("Candidate Features:",
      len(pd.read_parquet("outputs/candidate_features.parquet")))

print("Normalized Features:",
      len(pd.read_parquet("outputs/normalized_candidate_features.parquet")))

print("Ranked Candidates:",
      len(pd.read_parquet("outputs/ranked_candidates.parquet")))