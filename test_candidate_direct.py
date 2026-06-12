"""
Direct test of candidate processing with comprehensive debug logging
"""
import json
from pathlib import Path
from src.features.candidate_feature_engine import CandidateFeatureEngine
from src.features.jd_parser import parse_jd_file

# Step 1: Parse JD
jd_path = Path("data/job_description.docx")
jd_output = Path("outputs/jd_features.json")
jd_features_obj = parse_jd_file(jd_path, jd_output)

# Convert to dict for engine
jd_dict = {
    'role_title': jd_features_obj.role_title,
    'required_experience_min': jd_features_obj.required_experience_min,
    'required_experience_max': jd_features_obj.required_experience_max,
    'must_have_skills': jd_features_obj.must_have_skills,
    'preferred_skills': jd_features_obj.preferred_skills,
    'required_tools': jd_features_obj.required_tools,
    'required_domains': jd_features_obj.required_domains,
}

print("JD Features loaded:")
print(f"  Must-have skills ({len(jd_dict['must_have_skills'])}): {jd_dict['must_have_skills']}")
print(f"  Preferred skills ({len(jd_dict['preferred_skills'])}): {jd_dict['preferred_skills']}")

# Step 2: Initialize feature engine
feature_engine = CandidateFeatureEngine(jd_dict)

# Step 3: Load and process candidate CAND_0000024
candidates_path = Path("data/candidates.jsonl")
target_candidate = None

with open(candidates_path, 'r') as f:
    for line in f:
        candidate = json.loads(line)
        if candidate.get('candidate_id') == 'CAND_0000024':
            target_candidate = candidate
            break

if target_candidate:
    print("\n\nProcessing CAND_0000024...")
    vector = feature_engine.process_candidate('CAND_0000024', target_candidate)
    
    print(f"\n\nFinal Result:")
    print(f"  skill_match_score: {vector.skill_match_score}")
    print(f"  Evidence: {vector.evidence.get('skill_match', [])}")
else:
    print("ERROR: Could not find CAND_0000024")
