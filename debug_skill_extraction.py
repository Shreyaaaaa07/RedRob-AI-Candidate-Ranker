"""
Debug Script - Analyze Candidate CAND_0000024 Skill Extraction
"""
import json
import logging
from pathlib import Path
from typing import List, Dict

from src.utils import extract_atomic_skills

logging.basicConfig(level=logging.DEBUG)

# Load candidate data
candidates_path = Path("data/candidates.jsonl")
jd_path = Path("outputs/jd_features.json")

# Load JD features
with open(jd_path, 'r') as f:
    jd_features = json.load(f)

jd_must_have = jd_features.get('must_have_skills', [])
jd_preferred = jd_features.get('preferred_skills', [])

# Find candidate CAND_0000024
target_candidate = None
with open(candidates_path, 'r') as f:
    for i, line in enumerate(f):
        candidate = json.loads(line)
        if candidate.get('candidate_id') == 'CAND_0000024':
            target_candidate = candidate
            print(f"Found target candidate at line {i}")
            break

if not target_candidate:
    print("ERROR: Could not find CAND_0000024")
    exit(1)

print("\n" + "="*80)
print("COMPREHENSIVE DEBUG - SKILL MATCHING FOR CAND_0000024")
print("="*80)

# Extract all data
profile = target_candidate.get('profile', {})
career_history = target_candidate.get('career_history', []) or []
skills = target_candidate.get('skills', []) or []

print("\n1. CANDIDATE SKILLS EXTRACTION")
print("-" * 80)

# Explicit skills
explicit_skills = [s.get('name', '') for s in skills]
print(f"Explicit skills from 'skills' field ({len(explicit_skills)}):")
for skill in explicit_skills:
    print(f"   - {skill}")

# Summary skills
summary_text = profile.get('summary', '') or ""
summary_skills = extract_atomic_skills(summary_text)
print(f"\nFrom summary ({len(summary_skills)}):")
print(f"   Summary text (first 100 chars): {summary_text[:100]}...")
for skill in summary_skills:
    print(f"   - {skill}")

# Headline skills
headline_text = profile.get('headline', '') or ""
headline_skills = extract_atomic_skills(headline_text)
print(f"\nFrom headline ({len(headline_skills)}):")
print(f"   Headline: {headline_text}")
for skill in headline_skills:
    print(f"   - {skill}")

# Career description skills
print(f"\nFrom career descriptions ({len(career_history)} jobs):")
career_skills_all = []
for i, job in enumerate(career_history[:5]):  # Show first 5
    desc_skills = extract_atomic_skills(job.get('description', ''))
    career_skills_all.extend(desc_skills)
    print(f"   Job {i} ({job.get('title', 'Unknown')[:30]}): {len(desc_skills)} skills")
    for skill in desc_skills:
        print(f"      - {skill}")

# Combine all skills
all_candidate_skills = explicit_skills + summary_skills + headline_skills + career_skills_all
candidate_skills = sorted(list(set([s.strip() for s in all_candidate_skills if s and s.strip()])))

print(f"\n2. FINAL CANDIDATE SKILLS ({len(candidate_skills)} total, deduplicated):")
print("-" * 80)
for skill in candidate_skills:
    print(f"   - {skill}")

print(f"\n3. JD REQUIREMENTS")
print("-" * 80)
print(f"Must-have skills ({len(jd_must_have)}):")
for skill in jd_must_have:
    print(f"   - {skill}")

print(f"\nPreferred skills ({len(jd_preferred)}):")
for skill in jd_preferred:
    print(f"   - {skill}")

print(f"\n4. SKILL MATCHING ANALYSIS")
print("-" * 80)

# Normalize for matching
candidate_skills_lower = set(s.lower() for s in candidate_skills)
must_have_lower = set(s.lower() for s in jd_must_have)
preferred_lower = set(s.lower() for s in jd_preferred) if jd_preferred else set()

# Count matches using the exact logic from score_skill_match
must_have_matches = sum(1 for skill in must_have_lower if any(
    skill in cs or cs in skill for cs in candidate_skills_lower
))

preferred_matches = sum(1 for skill in preferred_lower if any(
    skill in cs or cs in skill for cs in candidate_skills_lower
))

print(f"Must-have matches: {must_have_matches}/{len(jd_must_have)}")
print(f"Preferred matches: {preferred_matches}/{len(jd_preferred)}")

# Calculate expected score using the exact logic
if must_have_lower:
    must_have_score = (must_have_matches / len(must_have_lower)) * 60
else:
    must_have_score = 60

preferred_bonus = min(40, (preferred_matches / max(1, len(preferred_lower))) * 40) if preferred_lower else 0
expected_score = must_have_score + preferred_bonus

print(f"\n5. SCORE CALCULATION")
print("-" * 80)
print(f"must_have_score = ({must_have_matches}/{len(jd_must_have)}) * 60 = {must_have_score:.4f}")
print(f"preferred_bonus = ({preferred_matches}/{max(1, len(jd_preferred))}) * 40 = {preferred_bonus:.4f}")
print(f"EXPECTED FINAL SCORE = {expected_score:.4f}")
print(f"(min 0, max 100) = {min(100.0, max(0.0, expected_score)):.4f}")

print(f"\n6. EXACT INTERSECTIONS")
print("-" * 80)

# Find what's matching
must_have_intersection = set()
for skill in must_have_lower:
    for cs in candidate_skills_lower:
        if skill in cs or cs in skill:
            must_have_intersection.add(skill)

print(f"Must-have skills that matched ({len(must_have_intersection)}):")
if must_have_intersection:
    for skill in sorted(must_have_intersection):
        print(f"   - {skill}")
else:
    print("   (none)")

preferred_intersection = set()
for skill in preferred_lower:
    for cs in candidate_skills_lower:
        if skill in cs or cs in skill:
            preferred_intersection.add(skill)

print(f"\nPreferred skills that matched ({len(preferred_intersection)}):")
if preferred_intersection:
    for skill in sorted(preferred_intersection):
        print(f"   - {skill}")
else:
    print("   (none)")

print("\n" + "="*80)
print("END DEBUG")
print("="*80)
