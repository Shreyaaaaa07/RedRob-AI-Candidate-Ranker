import json

from src.features.semantic_similarity import SemanticSimilarityEngine


# Initialize the model
engine = SemanticSimilarityEngine()

# ----------------------------
# Load JD
# ----------------------------
with open("outputs/jd_features.json", "r", encoding="utf-8") as f:
    jd = json.load(f)

jd_text = engine.build_jd_text(jd)

print("=" * 80)
print("JD TEXT")
print("=" * 80)
print(jd_text[:1000])   # print first 1000 chars


# ----------------------------
# Load first candidate
# ----------------------------
with open("data/candidates.jsonl", "r", encoding="utf-8") as f:

    first_line = f.readline()

candidate = json.loads(first_line)

candidate_text = engine.build_candidate_text(candidate)

print("\n")
print("=" * 80)
print("CANDIDATE TEXT")
print("=" * 80)
print(candidate_text[:1000])


# ----------------------------
# Compute similarity
# ----------------------------
score = engine.compute_similarity(
    jd_text,
    candidate_text
)

print("\n")
print("=" * 80)
print("SEMANTIC SIMILARITY")
print("=" * 80)
print(score)