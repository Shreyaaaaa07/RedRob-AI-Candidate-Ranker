"""
Comprehensive Project Audit Analysis Script

Traces semantic_similarity_score and skill_match_score through the entire pipeline
"""

import pandas as pd
import json
from pathlib import Path
import sys

print("\n" + "="*80)
print("REDROB AI CANDIDATE RANKER - COMPREHENSIVE AUDIT ANALYSIS")
print("="*80)

outputs_dir = Path("outputs")

# ============================================================================
# STEP 1: CHECK OUTPUT FILES EXISTENCE
# ============================================================================
print("\n[STEP 1] Checking output files...")
files_to_check = {
    "candidate_features.parquet": outputs_dir / "candidate_features.parquet",
    "semantic_scores.parquet": outputs_dir / "semantic_scores.parquet",
    "candidate_features_with_semantic.parquet": outputs_dir / "candidate_features_with_semantic.parquet",
    "normalized_candidate_features.parquet": outputs_dir / "normalized_candidate_features.parquet",
    "ranked_candidates.parquet": outputs_dir / "ranked_candidates.parquet",
    "ranked_candidates.csv": outputs_dir / "ranked_candidates.csv",
}

file_status = {}
for name, path in files_to_check.items():
    exists = path.exists()
    size_mb = path.stat().st_size / (1024*1024) if exists else 0
    file_status[name] = exists
    status_str = f"✓ EXISTS ({size_mb:.2f}MB)" if exists else "✗ MISSING"
    print(f"   {name:45} {status_str}")

# ============================================================================
# STEP 2: ANALYZE CANDIDATE_FEATURES.PARQUET
# ============================================================================
print("\n[STEP 2] Analyzing candidate_features.parquet...")
try:
    cf = pd.read_parquet(outputs_dir / "candidate_features.parquet")
    print(f"   Rows: {len(cf)}")
    print(f"   Columns: {len(cf.columns)}")
    print(f"   Columns list:")
    for col in sorted(cf.columns):
        print(f"      - {col}")
    
    # Check semantic_similarity_score
    if 'semantic_similarity_score' in cf.columns:
        print(f"\n   ✓ semantic_similarity_score EXISTS")
        print(f"      Mean: {cf['semantic_similarity_score'].mean():.4f}")
        print(f"      Min: {cf['semantic_similarity_score'].min():.4f}")
        print(f"      Max: {cf['semantic_similarity_score'].max():.4f}")
        print(f"      Non-zero count: {(cf['semantic_similarity_score'] > 0).sum()}")
    else:
        print(f"\n   ✗ semantic_similarity_score MISSING")
    
    # Check skill_match_score
    if 'skill_match_score' in cf.columns:
        print(f"\n   ✓ skill_match_score EXISTS")
        print(f"      Mean: {cf['skill_match_score'].mean():.4f}")
        print(f"      Min: {cf['skill_match_score'].min():.4f}")
        print(f"      Max: {cf['skill_match_score'].max():.4f}")
    else:
        print(f"\n   ✗ skill_match_score MISSING")
        
except Exception as e:
    print(f"   ✗ ERROR: {e}")

# ============================================================================
# STEP 3: ANALYZE SEMANTIC_SCORES.PARQUET
# ============================================================================
print("\n[STEP 3] Analyzing semantic_scores.parquet...")
if file_status.get("semantic_scores.parquet"):
    try:
        ss = pd.read_parquet(outputs_dir / "semantic_scores.parquet")
        print(f"   Rows: {len(ss)}")
        print(f"   Columns: {ss.columns.tolist()}")
        if 'semantic_similarity_score' in ss.columns:
            print(f"   ✓ semantic_similarity_score EXISTS")
            print(f"      Mean: {ss['semantic_similarity_score'].mean():.4f}")
            print(f"      Min: {ss['semantic_similarity_score'].min():.4f}")
            print(f"      Max: {ss['semantic_similarity_score'].max():.4f}")
            print(f"      Non-zero count: {(ss['semantic_similarity_score'] > 0).sum()}")
        print(f"\n   First 5 rows:")
        print(f"   {ss.head()}")
    except Exception as e:
        print(f"   ✗ ERROR: {e}")
else:
    print(f"   ✗ FILE DOES NOT EXIST")

# ============================================================================
# STEP 4: ANALYZE CANDIDATE_FEATURES_WITH_SEMANTIC.PARQUET
# ============================================================================
print("\n[STEP 4] Analyzing candidate_features_with_semantic.parquet...")
if file_status.get("candidate_features_with_semantic.parquet"):
    try:
        cfs = pd.read_parquet(outputs_dir / "candidate_features_with_semantic.parquet")
        print(f"   Rows: {len(cfs)}")
        print(f"   Columns: {len(cfs.columns)}")
        if 'semantic_similarity_score' in cfs.columns:
            print(f"   ✓ semantic_similarity_score EXISTS")
            print(f"      Mean: {cfs['semantic_similarity_score'].mean():.4f}")
            print(f"      Min: {cfs['semantic_similarity_score'].min():.4f}")
            print(f"      Max: {cfs['semantic_similarity_score'].max():.4f}")
            print(f"      Non-zero count: {(cfs['semantic_similarity_score'] > 0).sum()}")
        else:
            print(f"   ✗ semantic_similarity_score MISSING")
    except Exception as e:
        print(f"   ✗ ERROR: {e}")
else:
    print(f"   ✗ FILE DOES NOT EXIST")

# ============================================================================
# STEP 5: ANALYZE NORMALIZED_CANDIDATE_FEATURES.PARQUET
# ============================================================================
print("\n[STEP 5] Analyzing normalized_candidate_features.parquet...")
if file_status.get("normalized_candidate_features.parquet"):
    try:
        ncf = pd.read_parquet(outputs_dir / "normalized_candidate_features.parquet")
        print(f"   Rows: {len(ncf)}")
        print(f"   Columns: {len(ncf.columns)}")
        if 'semantic_similarity_score' in ncf.columns:
            print(f"   ✓ semantic_similarity_score EXISTS")
            print(f"      Mean: {ncf['semantic_similarity_score'].mean():.4f}")
            print(f"      Min: {ncf['semantic_similarity_score'].min():.4f}")
            print(f"      Max: {ncf['semantic_similarity_score'].max():.4f}")
        else:
            print(f"   ✗ semantic_similarity_score MISSING")
    except Exception as e:
        print(f"   ✗ ERROR: {e}")
else:
    print(f"   ✗ FILE DOES NOT EXIST")

# ============================================================================
# STEP 6: ANALYZE RANKED_CANDIDATES.PARQUET
# ============================================================================
print("\n[STEP 6] Analyzing ranked_candidates.parquet...")
if file_status.get("ranked_candidates.parquet"):
    try:
        rc = pd.read_parquet(outputs_dir / "ranked_candidates.parquet")
        print(f"   Rows: {len(rc)}")
        print(f"   Columns: {len(rc.columns)}")
        print(f"   Columns list:")
        for col in sorted(rc.columns):
            print(f"      - {col}")
        
        if 'semantic_similarity_score' in rc.columns:
            print(f"\n   ✓ semantic_similarity_score EXISTS in ranked output")
            print(f"      Mean: {rc['semantic_similarity_score'].mean():.4f}")
            print(f"      Min: {rc['semantic_similarity_score'].min():.4f}")
            print(f"      Max: {rc['semantic_similarity_score'].max():.4f}")
        else:
            print(f"\n   ✗ semantic_similarity_score MISSING in ranked output")
        
        if 'skill_match_score' in rc.columns:
            print(f"\n   ✓ skill_match_score EXISTS in ranked output")
            print(f"      Mean: {rc['skill_match_score'].mean():.4f}")
        else:
            print(f"\n   ✗ skill_match_score MISSING in ranked output")
        
        if 'hybrid_score' in rc.columns:
            print(f"\n   ✓ hybrid_score EXISTS")
            print(f"      Mean: {rc['hybrid_score'].mean():.4f}")
            print(f"      Top 5 scores:")
            for idx, row in rc.head(5).iterrows():
                print(f"         Rank {row['rank']}: {row['candidate_id']} = {row['hybrid_score']:.4f}")
    except Exception as e:
        print(f"   ✗ ERROR: {e}")
else:
    print(f"   ✗ FILE DOES NOT EXIST")

# ============================================================================
# STEP 7: TRACE semantic_similarity_score DATA FLOW
# ============================================================================
print("\n[STEP 7] TRACING SEMANTIC SIMILARITY SCORE DATA FLOW...")

trace_results = {}

# Compare cf and cfs
if file_status.get("candidate_features.parquet") and file_status.get("candidate_features_with_semantic.parquet"):
    cf = pd.read_parquet(outputs_dir / "candidate_features.parquet")
    cfs = pd.read_parquet(outputs_dir / "candidate_features_with_semantic.parquet")
    
    has_semantic_in_cf = 'semantic_similarity_score' in cf.columns
    has_semantic_in_cfs = 'semantic_similarity_score' in cfs.columns
    
    print(f"\n   candidate_features.parquet has semantic_similarity_score: {has_semantic_in_cf}")
    print(f"   candidate_features_with_semantic.parquet has semantic_similarity_score: {has_semantic_in_cfs}")
    
    if has_semantic_in_cf and has_semantic_in_cfs:
        # Check if they're the same
        cf_semantic = cf[['candidate_id', 'semantic_similarity_score']].set_index('candidate_id')
        cfs_semantic = cfs[['candidate_id', 'semantic_similarity_score']].set_index('candidate_id')
        
        are_equal = cf_semantic['semantic_similarity_score'].equals(cfs_semantic['semantic_similarity_score'])
        print(f"\n   Values identical in both files: {are_equal}")
        
        if not are_equal:
            differences = (cf_semantic['semantic_similarity_score'] != cfs_semantic['semantic_similarity_score']).sum()
            print(f"   Number of differing values: {differences}")

# Compare cfs and ncf
if file_status.get("candidate_features_with_semantic.parquet") and file_status.get("normalized_candidate_features.parquet"):
    cfs = pd.read_parquet(outputs_dir / "candidate_features_with_semantic.parquet")
    ncf = pd.read_parquet(outputs_dir / "normalized_candidate_features.parquet")
    
    has_semantic_in_cfs = 'semantic_similarity_score' in cfs.columns
    has_semantic_in_ncf = 'semantic_similarity_score' in ncf.columns
    
    print(f"\n   candidate_features_with_semantic has semantic_similarity_score: {has_semantic_in_cfs}")
    print(f"   normalized_candidate_features has semantic_similarity_score: {has_semantic_in_ncf}")
    
    if has_semantic_in_cfs and has_semantic_in_ncf:
        # Check if normalized values are in 0-1 range
        print(f"\n   Normalized semantic_similarity_score range: [{ncf['semantic_similarity_score'].min():.4f}, {ncf['semantic_similarity_score'].max():.4f}]")
        
        # Verify normalization formula
        # Original should be divided by 100
        cfs_normalized = cfs['semantic_similarity_score'] / 100
        are_equal = (cfs_normalized - ncf['semantic_similarity_score']).abs().max() < 0.0001
        print(f"   Normalization formula correct (score/100): {are_equal}")

# Compare ncf and rc
if file_status.get("normalized_candidate_features.parquet") and file_status.get("ranked_candidates.parquet"):
    ncf = pd.read_parquet(outputs_dir / "normalized_candidate_features.parquet")
    rc = pd.read_parquet(outputs_dir / "ranked_candidates.parquet")
    
    has_semantic_in_ncf = 'semantic_similarity_score' in ncf.columns
    has_semantic_in_rc = 'semantic_similarity_score' in rc.columns
    
    print(f"\n   normalized_candidate_features has semantic_similarity_score: {has_semantic_in_ncf}")
    print(f"   ranked_candidates has semantic_similarity_score: {has_semantic_in_rc}")

print("\n" + "="*80)
print("END OF AUDIT ANALYSIS")
print("="*80 + "\n")
