import json

from src.features.semantic_similarity import SemanticSimilarityEngine

engine = SemanticSimilarityEngine()

# Load JD
with open("outputs/jd_features.json", "r", encoding="utf-8") as f:
    jd = json.load(f)

jd_text = engine.build_jd_text(jd)

results = []
candidate_infos = []
candidate_texts = []

with open("data/candidates.jsonl", "r", encoding="utf-8") as f:

    for line in f:

        candidate = json.loads(line)

        candidate_infos.append({
            "candidate_id": candidate["candidate_id"],
            "headline": candidate["profile"].get("headline", "")
        })

        candidate_texts.append(
            engine.build_candidate_text(candidate)
        )

        if len(candidate_texts) >= 2000:
            break

print(f"Loaded {len(candidate_texts)} candidates...")

scores = engine.batch_compute(
    jd_text,
    candidate_texts
)

for info, score in zip(candidate_infos, scores):

    results.append({
        "candidate_id": info["candidate_id"],
        "headline": info["headline"],
        "score": score
    })

# Sort by similarity
results = sorted(
    results,
    key=lambda x: x["score"],
    reverse=True
)

print("\n===== TOP 20 SEMANTIC SCORES =====\n")

for r in results[:20]:

    print(
        f"{r['candidate_id']:15} "
        f"{r['score']:.2f}    "
        f"{r['headline']}"
    )