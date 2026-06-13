# NEXT TASK: Optimize Semantic Similarity + Regenerate Outputs

## Current Issue

`SemanticSimilarityEngine.compute_similarity()` re-computes the JD embedding for every candidate. The JD text is constant across all candidates, so the embedding should be pre-computed once in `CandidateFeatureEngine.__init__()` and reused.

## Files to Modify

1. `src/features/semantic_similarity.py` - Add pre-computation support
2. `src/features/candidate_feature_engine.py` - Pre-compute JD embedding, remove debug code

## Expected Fix

1. Add `precompute_jd_embedding(jd_text)` method to `SemanticSimilarityEngine`
2. Store `self.jd_embedding` in `CandidateFeatureEngine.__init__()`
3. Add `compute_similarity_with_jd_embedding(jd_embedding, candidate_text)` method
4. Call pre-computed method in `process_candidate()`
5. Remove debug code block (CAND_0000024 logging, lines 882-944)

## Exact Commands to Run After Fix

```powershell
# 1. Regenerate candidate features
python -m src.features.feature_pipeline

# 2. Verify semantic scores exist
python -c "import pandas as pd; df = pd.read_parquet('outputs/candidate_features.parquet'); print(f'semantic mean: {df[\"semantic_similarity_score\"].mean():.4f}')"

# 3. Run normalizer
python -m src.ranking.feature_normalizer

# 4. Run ranker
python -m src.ranking.hybrid_ranker

# 5. Final validation
python -c "
import pandas as pd
df = pd.read_parquet('outputs/ranked_candidates.parquet')
print(f'Top 10:')
print(df[['rank','candidate_id','semantic_similarity_score','skill_match_score','hybrid_score']].head(10))
print(f'semantic mean: {df[\"semantic_similarity_score\"].mean():.4f}')
print(f'skill mean: {df[\"skill_match_score\"].mean():.4f}')
print(f'hybrid mean: {df[\"hybrid_score\"].mean():.2f}')
"
```

## Expected Outputs

- `candidate_features.parquet`: semantic_similarity_score mean > 20 (not zero)
- `normalized_candidate_features.parquet`: semantic_similarity_score mean ~0.20-0.40
- `ranked_candidates.parquet`: semantic_similarity_score propagated correctly, hybrid_score computed

## Validation

- All features non-null
- Semantic scores non-zero
- Hybrid score properly weighted
- No missing columns
- No duplicate code paths
