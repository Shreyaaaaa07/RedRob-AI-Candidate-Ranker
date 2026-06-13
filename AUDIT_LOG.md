# AUDIT LOG

---

## Entry 1: 2026-06-13

**Issue:** Missing context preservation files  
**Root cause:** PROJECT_STATUS.md, NEXT_TASK.md, AUDIT_LOG.md did not exist  
**Fix:** Created all three files with initial state  
**Validation:** Files exist and are readable  
**Status:** COMPLETE

---

## Entry 2: 2026-06-13

**Issue:** SemanticSimilarityEngine re-computes JD embedding for every candidate  
**Root cause:** `compute_similarity()` encodes both JD and candidate text each call  
**Fix:** Add `encode_jd()`/`compute_similarity_with_jd_embedding()` methods for pre-computation  
**Files modified:**
   - `src/features/semantic_similarity.py`
   - `src/features/candidate_feature_engine.py`  
**Validation:** TBD (after regeneration)  
**Status:** PENDING

---

## Entry 3: 2026-06-13

**Issue:** Debug code in process_candidate() for CAND_0000024  
**Root cause:** Leftover debug logging during development  
**Fix:** Remove debug code block (lines 882-944)  
**Files modified:** `src/features/candidate_feature_engine.py`  
**Status:** PENDING

---

## Entry 4: 2026-06-13

**Issue:** Duplicate pipeline (semantic_feature_pipeline.py + merge_semantic_features.py)  
**Root cause:** Workaround created when semantic was not integrated into main pipeline  
**Fix:** Delete both files after confirming main pipeline works  
**Files removed:**
   - `src/features/semantic_feature_pipeline.py`
   - `src/features/merge_semantic_features.py`  
**Status:** PENDING
