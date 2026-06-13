"""
Diagnostic script to identify the semantic_similarity_score issue
"""

import json
from pathlib import Path
from src.features.jd_parser import parse_jd_file
from src.features.candidate_feature_engine import CandidateFeatureEngine
from src.data.load_data import CandidateDataLoader
import pandas as pd

print("\n" + "="*80)
print("DIAGNOSTIC: TESTING SEMANTIC SIMILARITY COMPUTATION")
print("="*80)

# Test 1: Parse JD
print("\n[TEST 1] Parsing JD...")
jd_path = Path("data") / "job_description.docx"
jd_output_path = Path("outputs") / "jd_features_test.json"

try:
    jd_features = parse_jd_file(jd_path, jd_output_path)
    print(f"[OK] JD parsed successfully")
    print(f"  Role: {jd_features.role_title}")
except Exception as e:
    print(f"[FAIL] JD parsing failed: {e}")
    exit(1)

# Test 2: Initialize engine
print("\n[TEST 2] Initializing feature engine...")
jd_dict = {
    'role_title': jd_features.role_title,
    'required_experience_min': jd_features.required_experience_min,
    'required_experience_max': jd_features.required_experience_max,
    'must_have_skills': jd_features.must_have_skills,
    'preferred_skills': jd_features.preferred_skills,
    'required_tools': jd_features.required_tools,
    'required_domains': jd_features.required_domains,
}

try:
    engine = CandidateFeatureEngine(jd_dict)
    print(f"[OK] Feature engine initialized")
    print(f"  Semantic engine type: {type(engine.semantic_engine)}")
    print(f"  JD text preview: {engine.jd_text[:100]}...")
except Exception as e:
    print(f"[FAIL] Engine initialization failed: {e}")
    exit(1)

# Test 3: Load a few candidates
print("\n[TEST 3] Loading sample candidates...")
loader = CandidateDataLoader()

sample_candidates = []
for candidate_id, candidate_data, error in loader.load_candidates(skip_errors=True, show_progress=False):
    if error is None and candidate_data:
        sample_candidates.append((candidate_id, candidate_data))
    if len(sample_candidates) >= 5:
        break

print(f"[OK] Loaded {len(sample_candidates)} sample candidates")

# Test 4: Process a single candidate
print("\n[TEST 4] Processing single candidate...")
if sample_candidates:
    cand_id, cand_data = sample_candidates[0]
    
    try:
        vector = engine.process_candidate(cand_id, cand_data)
        print(f"✓ Processed candidate {cand_id}")
        print(f"  semantic_similarity_score: {vector.semantic_similarity_score}")
        print(f"  skill_match_score: {vector.skill_match_score}")
        print(f"  experience_match_score: {vector.experience_match_score}")
        print(f"  Semantic evidence: {vector.evidence.get('semantic_similarity', ['N/A'])}")
        print(f"  Evidence keys: {list(vector.evidence.keys())}")
    except Exception as e:
        print(f"✗ Processing failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

# Test 5: Process batch of candidates and check results
print("\n[TEST 5] Processing batch of candidates...")
try:
    # Reload candidates fresh
    loader = CandidateDataLoader()
    
    vectors = []
    for candidate_id, candidate_data, error in loader.load_candidates(skip_errors=True, show_progress=False):
        if error is None and candidate_data:
            try:
                vector = engine.process_candidate(candidate_id, candidate_data)
                vectors.append(vector)
            except Exception as e:
                print(f"  Error processing {candidate_id}: {e}")
        if len(vectors) >= 100:
            break
    
    print(f"✓ Processed {len(vectors)} candidates")
    
    # Analyze semantic similarity
    semantic_scores = [v.semantic_similarity_score for v in vectors]
    print(f"\n  Semantic similarity statistics:")
    print(f"    Mean: {sum(semantic_scores)/len(semantic_scores):.4f}")
    print(f"    Min: {min(semantic_scores):.4f}")
    print(f"    Max: {max(semantic_scores):.4f}")
    print(f"    Non-zero count: {sum(1 for s in semantic_scores if s > 0)}")
    
    # Analyze skill match
    skill_scores = [v.skill_match_score for v in vectors]
    print(f"\n  Skill match statistics:")
    print(f"    Mean: {sum(skill_scores)/len(skill_scores):.4f}")
    print(f"    Min: {min(skill_scores):.4f}")
    print(f"    Max: {max(skill_scores):.4f}")
    
    # Show top candidates
    print(f"\n  Top 5 by semantic similarity:")
    sorted_by_semantic = sorted(vectors, key=lambda v: v.semantic_similarity_score, reverse=True)
    for i, v in enumerate(sorted_by_semantic[:5]):
        print(f"    {i+1}. {v.candidate_id}: {v.semantic_similarity_score:.2f}")
    
except Exception as e:
    print(f"✗ Batch processing failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n" + "="*80)
print("DIAGNOSTIC COMPLETE")
print("="*80 + "\n")
