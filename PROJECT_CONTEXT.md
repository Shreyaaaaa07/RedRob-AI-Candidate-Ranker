# Redrob AI Candidate Ranker - Project Handoff

## Goal

Build a hackathon-winning AI-powered candidate ranking system for Redrob that goes beyond keyword matching.

The architecture should be:

Job Description
→ JD Intelligence Engine
→ Candidate Intelligence Engine
→ Evidence Extraction
→ Feature Normalization
→ Hybrid Ranking Engine
→ Cross Encoder Re-ranking
→ Explainable Top Candidate Output

The focus is on explainability, recruiter-like reasoning, behavioral signals, and evidence-backed ranking.

---

## Current Progress

### ✅ Completed

* Project setup
* GitHub repository
* Data loader
* EDA
* JD Parser
* Candidate Feature Engine
* Feature Pipeline
* Risk Detection
* Behavioral signal mapping fix

Pipeline now completes successfully.

---

## Important Bug Already Fixed

Originally:

Candidates with risk flags = 100000

After fixing behavioral signal source:

Candidates with risk flags ≈ 16588

The issue was that:

profile_completeness_score
open_to_work
notice_period_days
willing_to_relocate

were incorrectly read from `profile` instead of `redrob_signals`.

This has already been fixed.

Do NOT revert it.

---

## Current Known Issue

career_stability_score:

mean = 50

median = 50

range = [50,50]

Likely cause:

Date parsing failure.

score_career_stability() returns default 50 whenever tenure cannot be calculated.

Tomorrow's first task is to inspect career_history date formats and fix tenure parsing.

---

## Experience Match

Current statistics:

mean ≈ 21

median ≈ 1

Needs validation.

May be because:

* strict normalization
* or dataset mostly junior

Should be investigated before ranking.

---

## Things NOT to build yet

* Embeddings
* FAISS
* ChromaDB
* Cross Encoder
* React
* FastAPI
* Final Ranking

First stabilize feature engineering.

---

## Immediate Next Tasks

1. Fix Career Stability
2. Validate Experience Match
3. Audit Evidence Store
4. Verify candidate_features.parquet
5. Review feature distributions
6. Build Feature Normalization Layer
7. Design Hybrid Ranking Engine
8. Add Sentence Transformer embeddings
9. Add Cross Encoder reranking
10. Build React dashboard

---

## Copilot Usage Strategy

Copilot should only:

* implement modules
* optimize code
* refactor
* write tests

Copilot should NOT decide architecture.

Architecture decisions should remain manual.

---

## Development Philosophy

One step at a time.

Never modify multiple subsystems simultaneously.

After every successful step:

git add .
git commit
git push

Keep stable checkpoints.

---

## Current Objective

Build a recruiter-quality AI ranking system that is explainable, evidence-driven, JD-aware, and behavior-aware instead of a simple semantic search engine.
