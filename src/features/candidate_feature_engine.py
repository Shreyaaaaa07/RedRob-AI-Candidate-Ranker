"""
Candidate Feature Engineering Engine - Intelligent Feature Vector Generation

Processes 100,000+ candidates and generates comprehensive feature vectors based on:
- JD requirements matching
- Production experience signals
- Behavioral metrics
- Risk factors

Module: src.features.candidate_feature_engine
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional, Set
from dataclasses import dataclass, asdict, field
from collections import defaultdict
import re
from datetime import datetime, timedelta

import numpy as np
from tqdm import tqdm

logger = logging.getLogger(__name__)


@dataclass
class CandidateFeatureVector:
    """Structured feature vector for a candidate"""
    
    # Identifiers
    candidate_id: str = ""
    
    # JD-Specific Matching Scores (0-100)
    experience_match_score: float = 0.0
    skill_match_score: float = 0.0
    production_ml_score: float = 0.0
    retrieval_score: float = 0.0
    vector_database_score: float = 0.0
    ranking_system_score: float = 0.0
    evaluation_framework_score: float = 0.0
    startup_fit_score: float = 0.0
    open_source_score: float = 0.0
    
    # Behavioral Scores (0-100)
    education_score: float = 0.0
    career_stability_score: float = 0.0
    experience_consistency_score: float = 0.0
    recruiter_interest_score: float = 0.0
    activity_score: float = 0.0
    engagement_score: float = 0.0
    availability_score: float = 0.0
    behavior_score: float = 0.0
    
    # Risk Assessment (0-100, higher = more risk)
    risk_score: float = 0.0
    
    # Evidence and context
    evidence: Dict[str, List[str]] = field(default_factory=dict)
    risk_flags: List[str] = field(default_factory=list)
    
    # Metadata
    processing_timestamp: str = ""


class ScoringEngine:
    """Centralized scoring logic for all features"""
    
    # Keyword categories for detection
    PRODUCTION_KEYWORDS = {
        "deployed", "production", "serving", "scalable", "inference",
        "live", "real users", "at scale", "pipeline", "real-time",
        "shipped", "released", "launch", "serving models"
    }
    
    RETRIEVAL_KEYWORDS = {
        "retrieval", "semantic search", "hybrid search", "ranking",
        "recommendation", "search system", "search ranking", "retrieval system",
        "candidate matching", "document ranking", "query"
    }
    
    VECTOR_DB_KEYWORDS = {
        "faiss", "pinecone", "milvus", "qdrant", "weaviate",
        "elasticsearch", "opensearch", "vector", "embedding index"
    }
    
    RANKING_KEYWORDS = {
        "ranking", "learning to rank", "ltr", "l2r", "ranker",
        "xgboost", "lightgbm", "rank", "scoring system"
    }
    
    EVALUATION_KEYWORDS = {
        "ndcg", "mrr", "map", "precision@k", "recall@k",
        "offline evaluation", "online evaluation", "a/b test", "evaluation"
    }
    
    STARTUP_KEYWORDS = {
        "founding", "startup", "early stage", "zero to one",
        "shipped", "mvp", "growth stage", "early"
    }
    
    OPEN_SOURCE_KEYWORDS = {
        "github", "open source", "oss", "contributor", "maintainer",
        "pull request", "repository", "open-source"
    }
    
    def __init__(self, jd_features: Optional[Dict[str, Any]] = None):
        """
        Initialize scoring engine with optional JD features.
        
        Args:
            jd_features: JD features from parser
        """
        self.jd_features = jd_features or {}
        self.jd_experience_min = jd_features.get('required_experience_min', 5) if jd_features else 5
        self.jd_experience_max = jd_features.get('required_experience_max', 9) if jd_features else 9
    
    # ========== EXPERIENCE MATCHING ==========
    
    def score_experience_match(
        self, candidate_years: float, career_history: List[Dict], 
        evidence_list: List[str]
    ) -> float:
        """
        Score experience match using smooth normalization.
        
        Not just comparing to JD years directly.
        Consider career progression and stability.
        """
        if candidate_years <= 0:
            return 0.0
        
        # Ideal range: JD min to JD max
        jd_min = self.jd_experience_min
        jd_max = self.jd_experience_max
        mid_point = (jd_min + jd_max) / 2
        range_width = (jd_max - jd_min) / 2
        
        # Smooth bell curve (Gaussian-like)
        distance_from_ideal = abs(candidate_years - mid_point)
        sigma = range_width / 2  # Standard deviation
        
        if distance_from_ideal == 0:
            score = 100.0
        else:
            # Gaussian: exp(-distance^2 / (2 * sigma^2))
            score = 100.0 * np.exp(-(distance_from_ideal ** 2) / (2 * sigma ** 2))
        
        if score > 90:
            evidence_list.append(f"Experience {candidate_years:.1f}y matches JD range {jd_min}-{jd_max}y")
        
        return min(100.0, max(0.0, score))
    
    # ========== SKILL MATCHING ==========
    
    def score_skill_match(
        self, candidate_skills: List[str], jd_must_have: List[str],
        jd_preferred: List[str], evidence_list: List[str]
    ) -> float:
        """Score how many JD required skills candidate has"""
        
        if not jd_must_have:
            return 50.0  # Neutral if no requirements
        
        candidate_skills_lower = set(s.lower() for s in candidate_skills)
        must_have_lower = set(s.lower() for s in jd_must_have)
        preferred_lower = set(s.lower() for s in jd_preferred) if jd_preferred else set()
        
        # Check for exact matches (simple keyword matching)
        must_have_matches = sum(1 for skill in must_have_lower if any(
            skill in cs or cs in skill for cs in candidate_skills_lower
        ))
        
        preferred_matches = sum(1 for skill in preferred_lower if any(
            skill in cs or cs in skill for cs in candidate_skills_lower
        ))
        
        # Score: 40% must-have, 60% for going beyond
        if must_have_lower:
            must_have_score = (must_have_matches / len(must_have_lower)) * 60
        else:
            must_have_score = 60
        
        # Bonus for preferred
        preferred_bonus = min(40, (preferred_matches / max(1, len(preferred_lower))) * 40) if preferred_lower else 0
        
        score = must_have_score + preferred_bonus
        
        if must_have_matches > 0:
            evidence_list.append(f"Has {must_have_matches}/{len(must_have_lower)} must-have skills")
        
        return min(100.0, max(0.0, score))
    
    # ========== DOMAIN-SPECIFIC SCORING ==========
    
    def score_production_ml(
        self, profile_text: str, career_history: List[Dict],
        evidence_list: List[str], risk_flags: List[str]
    ) -> float:
        """Score production ML/AI experience"""
        
        score = 0.0
        all_text = profile_text.lower()
        
        # Add career history to search
        for entry in career_history:
            all_text += " " + (entry.get('title', '') or '').lower()
            all_text += " " + (entry.get('description', '') or '').lower()
        
        # Check for production keywords
        prod_keywords_found = [kw for kw in self.PRODUCTION_KEYWORDS if kw in all_text]
        if prod_keywords_found:
            score += 40
            evidence_list.append(f"Production experience: {', '.join(set(prod_keywords_found[:3]))}")
        
        # Check for ML-specific keywords
        ml_keywords = {"machine learning", "deep learning", "neural", "model", "ml", "ai"}
        ml_keywords_found = [kw for kw in ml_keywords if kw in all_text]
        if ml_keywords_found:
            score += 30
            evidence_list.append(f"ML expertise: {', '.join(set(ml_keywords_found[:2]))}")
        
        # Check for scale
        if any(kw in all_text for kw in ["100k", "million", "billion", "scale", "distributed"]):
            score += 20
            evidence_list.append("Evidence of building at scale")
        
        # Anti-pattern: Recent LangChain-only
        if "langchain" in all_text and "pytorch" not in all_text and "tensorflow" not in all_text:
            risk_flags.append("LangChain-only experience detected")
            score = max(0, score - 30)
        
        return min(100.0, max(0.0, score))
    
    def score_retrieval(
        self, profile_text: str, career_history: List[Dict],
        evidence_list: List[str]
    ) -> float:
        """Score retrieval/search systems experience"""
        
        score = 0.0
        all_text = profile_text.lower()
        
        for entry in career_history:
            all_text += " " + (entry.get('title', '') or '').lower()
            all_text += " " + (entry.get('description', '') or '').lower()
        
        retrieval_found = [kw for kw in self.RETRIEVAL_KEYWORDS if kw in all_text]
        if retrieval_found:
            score += 50
            evidence_list.append(f"Retrieval expertise: {', '.join(set(retrieval_found[:3]))}")
        
        # Search systems
        if "search" in all_text:
            score += 30
            evidence_list.append("Search systems experience")
        
        # Ranking
        if "rank" in all_text:
            score += 20
            evidence_list.append("Ranking systems experience")
        
        return min(100.0, max(0.0, score))
    
    def score_vector_database(
        self, profile_text: str, career_history: List[Dict],
        evidence_list: List[str]
    ) -> float:
        """Score vector database and similarity search experience"""
        
        score = 0.0
        all_text = profile_text.lower()
        
        for entry in career_history:
            all_text += " " + (entry.get('title', '') or '').lower()
            all_text += " " + (entry.get('description', '') or '').lower()
        
        vdb_found = [kw for kw in self.VECTOR_DB_KEYWORDS if kw in all_text]
        if vdb_found:
            score += 70
            evidence_list.append(f"Vector DB tools: {', '.join(set(vdb_found[:3]))}")
        
        # Embeddings
        if "embedding" in all_text or "embeddings" in all_text:
            score += 30
            evidence_list.append("Embeddings experience")
        
        return min(100.0, max(0.0, score))
    
    def score_ranking_system(
        self, profile_text: str, career_history: List[Dict],
        evidence_list: List[str]
    ) -> float:
        """Score learning-to-rank and ranking systems experience"""
        
        score = 0.0
        all_text = profile_text.lower()
        
        for entry in career_history:
            all_text += " " + (entry.get('title', '') or '').lower()
            all_text += " " + (entry.get('description', '') or '').lower()
        
        ranking_found = [kw for kw in self.RANKING_KEYWORDS if kw in all_text]
        if ranking_found:
            score += 60
            evidence_list.append(f"Ranking expertise: {', '.join(set(ranking_found[:3]))}")
        
        # ML models
        if any(kw in all_text for kw in ["xgboost", "lightgbm", "gradient"]):
            score += 25
            evidence_list.append("ML ranking models")
        
        return min(100.0, max(0.0, score))
    
    def score_evaluation_framework(
        self, profile_text: str, career_history: List[Dict],
        evidence_list: List[str]
    ) -> float:
        """Score experience with evaluation frameworks (NDCG, MRR, etc.)"""
        
        score = 0.0
        all_text = profile_text.lower()
        
        for entry in career_history:
            all_text += " " + (entry.get('title', '') or '').lower()
            all_text += " " + (entry.get('description', '') or '').lower()
        
        eval_found = [kw for kw in self.EVALUATION_KEYWORDS if kw in all_text]
        if eval_found:
            score += 70
            evidence_list.append(f"Evaluation frameworks: {', '.join(set(eval_found[:3]))}")
        
        # A/B testing
        if "a/b test" in all_text or "ab test" in all_text:
            score += 20
            evidence_list.append("A/B testing experience")
        
        return min(100.0, max(0.0, score))
    
    def score_startup_fit(
        self, profile_text: str, career_history: List[Dict],
        current_role: str, evidence_list: List[str]
    ) -> float:
        """Score founding engineer and early-stage experience"""
        
        score = 0.0
        all_text = profile_text.lower()
        
        for entry in career_history:
            all_text += " " + (entry.get('title', '') or '').lower()
            all_text += " " + (entry.get('description', '') or '').lower()
        
        # Direct startup keywords
        startup_found = [kw for kw in self.STARTUP_KEYWORDS if kw in all_text]
        if startup_found:
            score += 50
            evidence_list.append(f"Startup experience: {', '.join(set(startup_found[:2]))}")
        
        # Currently at startup (proxy: if current company is in tech sector)
        if current_role and any(word in current_role.lower() for word in ["startup", "founding", "early"]):
            score += 30
            evidence_list.append(f"Current role: {current_role}")
        
        return min(100.0, max(0.0, score))
    
    def score_open_source(
        self, profile_text: str, github_activity: Optional[float],
        evidence_list: List[str]
    ) -> float:
        """Score open source and GitHub contributions"""
        
        score = 0.0
        all_text = profile_text.lower()
        
        # GitHub activity
        if github_activity and github_activity > 50:
            score += 60
            evidence_list.append(f"GitHub activity score: {github_activity:.0f}")
        
        # OSS keywords
        oss_found = [kw for kw in self.OPEN_SOURCE_KEYWORDS if kw in all_text]
        if oss_found:
            score += 40
            evidence_list.append(f"Open source: {', '.join(set(oss_found[:2]))}")
        
        return min(100.0, max(0.0, score))
    
    # ========== CAREER ANALYSIS ==========
    
    def score_career_stability(
        self, career_history: List[Dict],
        evidence_list: List[str], risk_flags: List[str]
    ) -> float:
        """
        Score career stability based on tenure and job switching patterns.
        
        Don't penalize reasonable growth - penalize excessive hopping.
        """
        if not career_history or len(career_history) < 2:
            return 50.0  # Neutral
        
        # Calculate average tenure
        tenures = []
        for job in career_history:
            start = job.get('start_date')
            end = job.get('end_date')
            if start and end:
                # Parse dates (assume YYYY-MM format)
                try:
                    start_date = datetime.strptime(start, '%Y-%m')
                    end_date = datetime.strptime(end, '%Y-%m')
                    tenure_months = (end_date - start_date).days / 30.44
                    if tenure_months > 0:
                        tenures.append(tenure_months)
                except:
                    pass
        
        if not tenures:
            return 50.0
        
        avg_tenure = np.mean(tenures)
        num_jobs = len(career_history)
        job_switch_rate = num_jobs / (np.sum(tenures) / 12) if np.sum(tenures) > 0 else 0
        
        # Scoring logic
        score = 0.0
        
        # Average tenure: 3+ years is good
        if avg_tenure >= 36:
            score += 50
            evidence_list.append(f"Good stability: avg {avg_tenure/12:.1f}y tenure")
        elif avg_tenure >= 24:
            score += 35
            evidence_list.append(f"Decent stability: avg {avg_tenure/12:.1f}y tenure")
        else:
            score += 20
        
        # Job switching: < 1 switch per year is good
        if job_switch_rate <= 1:
            score += 30
            evidence_list.append(f"Good retention: {num_jobs} jobs in {np.sum(tenures)/12:.0f}y")
        elif job_switch_rate <= 2:
            score += 15
        else:
            score = max(0, score - 20)
            risk_flags.append(f"High job switching: {job_switch_rate:.1f} jobs/year")
        
        # Recent progression
        if len(career_history) > 0:
            latest_role = career_history[0].get('title', '').lower()
            if any(word in latest_role for word in ["senior", "lead", "staff", "principal"]):
                score += 20
                evidence_list.append("Career progression: senior role")
        
        return min(100.0, max(0.0, score))
    
    def score_experience_consistency(
        self, claimed_years: float, career_history: List[Dict],
        evidence_list: List[str], risk_flags: List[str]
    ) -> float:
        """
        Check if claimed years matches actual career history duration.
        
        Detect inconsistencies and inflations.
        """
        if not career_history or claimed_years <= 0:
            return 50.0
        
        # Calculate actual years from career history
        start_dates = []
        for job in career_history:
            start = job.get('start_date')
            if start:
                try:
                    start_date = datetime.strptime(start, '%Y-%m')
                    start_dates.append(start_date)
                except:
                    pass
        
        if not start_dates:
            return 50.0  # Can't verify
        
        earliest_start = min(start_dates)
        actual_years = (datetime.now() - earliest_start).days / 365.25
        
        # Compare claimed vs actual
        difference = abs(claimed_years - actual_years)
        discrepancy_percent = (difference / max(claimed_years, actual_years)) * 100
        
        if discrepancy_percent < 10:
            score = 90
            evidence_list.append(f"Consistent: claimed {claimed_years}y, actual {actual_years:.1f}y")
        elif discrepancy_percent < 25:
            score = 60
            evidence_list.append(f"Slight inconsistency: claimed {claimed_years}y, actual {actual_years:.1f}y")
            risk_flags.append(f"Experience inflation: {discrepancy_percent:.0f}% difference")
        else:
            score = 30
            risk_flags.append(f"Major inconsistency: claimed {claimed_years}y, actual {actual_years:.1f}y")
        
        return min(100.0, max(0.0, score))
    
    # ========== BEHAVIORAL METRICS ==========
    
    def score_recruiter_interest(
        self, response_rate: float, saved_by_recruiters: int,
        interview_rate: float, evidence_list: List[str]
    ) -> float:
        """Score recruiter validation signals"""
        
        score = 0.0
        
        # Response rate (0-100%)
        if response_rate > 60:
            score += 40
            evidence_list.append(f"Good response rate: {response_rate:.0f}%")
        elif response_rate > 30:
            score += 20
        
        # Saved by recruiters (absolute count)
        if saved_by_recruiters >= 20:
            score += 40
            evidence_list.append(f"Highly saved: {saved_by_recruiters} recruiters")
        elif saved_by_recruiters >= 5:
            score += 20
        
        # Interview rate
        if interview_rate > 30:
            score += 20
            evidence_list.append(f"Interview rate: {interview_rate:.0f}%")
        
        return min(100.0, max(0.0, score))
    
    def score_activity(
        self, github_score: float, profile_views_30d: int,
        search_appearances_30d: int, applications_30d: int,
        evidence_list: List[str]
    ) -> float:
        """Score recent activity and engagement"""
        
        score = 0.0
        
        if github_score and github_score > 30:
            score += 30
            evidence_list.append(f"Active on GitHub: {github_score:.0f}")
        
        if profile_views_30d > 50:
            score += 25
            evidence_list.append(f"Profile views (30d): {profile_views_30d}")
        
        if search_appearances_30d > 20:
            score += 25
            evidence_list.append(f"Search appearances (30d): {search_appearances_30d}")
        
        if applications_30d > 5:
            score += 20
            evidence_list.append(f"Active applications (30d): {applications_30d}")
        
        return min(100.0, max(0.0, score))
    
    def score_engagement(
        self, profile_completeness: float, response_time_hours: float,
        response_rate: float, evidence_list: List[str]
    ) -> float:
        """Score profile engagement and responsiveness"""
        
        score = 0.0
        
        if profile_completeness > 80:
            score += 40
            evidence_list.append(f"Complete profile: {profile_completeness:.0f}%")
        elif profile_completeness > 50:
            score += 20
        else:
            score += 5
        
        if response_time_hours and response_time_hours < 24:
            score += 35
            evidence_list.append(f"Quick responses: {response_time_hours:.1f}h avg")
        elif response_time_hours and response_time_hours < 72:
            score += 20
        
        if response_rate > 40:
            score += 25
            evidence_list.append(f"Good response rate: {response_rate:.0f}%")
        
        return min(100.0, max(0.0, score))
    
    def score_availability(
        self, open_to_work: bool, notice_period_days: int,
        willing_to_relocate: bool, evidence_list: List[str]
    ) -> float:
        """Score hiring availability"""
        
        score = 0.0
        
        if open_to_work:
            score += 50
            evidence_list.append("Actively open to work")
        else:
            score += 20
        
        if notice_period_days <= 30:
            score += 30
            evidence_list.append(f"Quick available: {notice_period_days}d notice")
        elif notice_period_days <= 60:
            score += 15
        else:
            score += 5
        
        if willing_to_relocate:
            score += 20
            evidence_list.append("Willing to relocate")
        
        return min(100.0, max(0.0, score))
    
    def score_education(
        self, education_list: List[Dict], evidence_list: List[str]
    ) -> float:
        """Score education tier and relevance"""
        
        score = 0.0
        
        if not education_list:
            return 40.0  # No education info
        
        for edu in education_list:
            school = (edu.get('school_name', '') or '').lower()
            degree = (edu.get('degree_type', '') or '').lower()
            field = (edu.get('field_of_study', '') or '').lower()
            
            # Tier 1 schools
            tier1 = {
                "iit", "bits", "delhi", "mumbai", "stanford",
                "mit", "berkeley", "carnegie", "oxford", "cambridge"
            }
            if any(t in school for t in tier1):
                score += 40
                evidence_list.append(f"Tier-1 education: {school}")
            else:
                score += 20
            
            # Relevant degree
            if any(field_kw in field for field_kw in ["computer", "ai", "ml", "data", "engineering"]):
                score += 30
                evidence_list.append(f"Relevant degree: {degree} in {field}")
            else:
                score += 10
        
        return min(100.0, max(0.0, score))
    
    # ========== RISK DETECTION ==========
    
    def detect_risks(
        self, candidate_data: Dict[str, Any],
        risk_flags: List[str]
    ) -> float:
        """
        Detect red flags and risk factors.
        
        Returns risk score (0-100, higher = more risk)
        """
        risk_score = 0.0
        
        profile = candidate_data.get('profile', {})
        career_history = candidate_data.get('career_history', [])
        skills = candidate_data.get('skills', [])
        signals = candidate_data.get('redrob_signals', {})
        
        # Normalize skills to string list (skills may be dicts or strings)
        skill_names = []
        for s in skills:
            if isinstance(s, dict):
                skill_names.append((s.get('name', '') or '').lower())
            else:
                skill_names.append((s or '').lower())
        
        # Risk 1: Skill stuffing
        num_skills = len(skills)
        if num_skills > 100:
            risk_score += 20
            risk_flags.append(f"Skill stuffing: {num_skills} skills listed")
        
        # Risk 2: Unrealistic claims
        years = profile.get('years_of_experience', 0)
        ai_skills = [s for s in skill_names if any(kw in s for kw in ["ai", "ml", "llm", "gpt"])]
        if len(ai_skills) > 30 and years < 3:
            risk_score += 25
            risk_flags.append(f"Unrealistic AI expertise: {len(ai_skills)} AI skills but only {years}y exp")
        
        # Risk 3: Career contradiction
        if career_history:
            titles = [j.get('title', '').lower() for j in career_history]
            if any('ml' in t or 'ai' in t or 'data' in t for t in titles):
                pass  # Expected AI background
            elif len(ai_skills) > 20:
                risk_score += 15
                risk_flags.append("AI expertise but no AI role in history")
        
        # Risk 4: Experience inconsistency (handled separately)
        
        # Risk 5: Low profile completeness
        completeness = profile.get('profile_completeness_score', 0)
        if completeness < 30:
            risk_score += 15
            risk_flags.append(f"Very incomplete profile: {completeness}%")
        
        # Risk 6: Poor recruiter engagement
        resp_rate = signals.get('recruiter_response_rate', 0)
        saved_recruiters = signals.get('saved_by_recruiters_30d', 0)
        if resp_rate < 5 and saved_recruiters < 1:
            risk_score += 20
            risk_flags.append("No recruiter engagement signal")
        
        # Risk 7: Excessive job hopping (handled in career stability)
        
        return min(100.0, max(0.0, risk_score))


class CandidateFeatureEngine:
    """Main engine for processing candidates and generating features"""
    
    def __init__(self, jd_features: Optional[Dict[str, Any]] = None):
        """Initialize with optional JD features"""
        self.scorer = ScoringEngine(jd_features)
        self.jd_features = jd_features or {}
    
    def process_candidate(
        self, candidate_id: str, candidate_data: Dict[str, Any]
    ) -> CandidateFeatureVector:
        """
        Process a single candidate and generate feature vector.
        
        Args:
            candidate_id: Unique candidate identifier
            candidate_data: Candidate profile data
            
        Returns:
            CandidateFeatureVector with all scores and evidence
        """
        vector = CandidateFeatureVector()
        vector.candidate_id = candidate_id
        vector.processing_timestamp = datetime.now().isoformat()
        
        # Extract key fields
        profile = candidate_data.get('profile', {})
        career_history = candidate_data.get('career_history', []) or []
        skills = candidate_data.get('skills', []) or []
        education = candidate_data.get('education', []) or []
        signals = candidate_data.get('redrob_signals', {})
        
        years_exp = profile.get('years_of_experience', 0) or 0
        profile_text = (profile.get('summary', '') or '') + " " + (profile.get('headline', '') or '')
        
        # Initialize evidence storage
        vector.evidence = defaultdict(list)
        
        # ========== JD MATCHING SCORES ==========
        
        # Experience match
        vector.experience_match_score = self.scorer.score_experience_match(
            years_exp, career_history, vector.evidence['experience_match']
        )
        
        # Skill match
        jd_must_have = self.jd_features.get('must_have_skills', [])
        jd_preferred = self.jd_features.get('preferred_skills', [])
        vector.skill_match_score = self.scorer.score_skill_match(
            [s.get('name', '') for s in skills],
            jd_must_have, jd_preferred, vector.evidence['skill_match']
        )
        
        # Production ML
        vector.production_ml_score = self.scorer.score_production_ml(
            profile_text, career_history, vector.evidence['production_ml'], vector.risk_flags
        )
        
        # Retrieval
        vector.retrieval_score = self.scorer.score_retrieval(
            profile_text, career_history, vector.evidence['retrieval']
        )
        
        # Vector databases
        vector.vector_database_score = self.scorer.score_vector_database(
            profile_text, career_history, vector.evidence['vector_database']
        )
        
        # Ranking systems
        vector.ranking_system_score = self.scorer.score_ranking_system(
            profile_text, career_history, vector.evidence['ranking_system']
        )
        
        # Evaluation frameworks
        vector.evaluation_framework_score = self.scorer.score_evaluation_framework(
            profile_text, career_history, vector.evidence['evaluation_framework']
        )
        
        # Startup fit
        current_role = profile.get('headline', '')
        vector.startup_fit_score = self.scorer.score_startup_fit(
            profile_text, career_history, current_role, vector.evidence['startup_fit']
        )
        
        # Open source
        github_score = signals.get('github_activity_score')
        vector.open_source_score = self.scorer.score_open_source(
            profile_text, github_score, vector.evidence['open_source']
        )
        
        # ========== BEHAVIORAL SCORES ==========
        
        # Education
        vector.education_score = self.scorer.score_education(
            education, vector.evidence['education']
        )
        
        # Career stability
        vector.career_stability_score = self.scorer.score_career_stability(
            career_history, vector.evidence['career_stability'], vector.risk_flags
        )
        
        # Experience consistency
        vector.experience_consistency_score = self.scorer.score_experience_consistency(
            years_exp, career_history, vector.evidence['experience_consistency'], vector.risk_flags
        )
        
        # Recruiter interest
        resp_rate = signals.get('recruiter_response_rate', 0) or 0
        saved = signals.get('saved_by_recruiters_30d', 0) or 0
        interview_rate = signals.get('interview_completion_rate', 0) or 0
        vector.recruiter_interest_score = self.scorer.score_recruiter_interest(
            resp_rate, saved, interview_rate, vector.evidence['recruiter_interest']
        )
        
        # Activity
        github_score = signals.get('github_activity_score') or 0
        profile_views = signals.get('profile_views_received_30d', 0) or 0
        search_apps = signals.get('search_appearance_30d', 0) or 0
        apps_30d = signals.get('applications_submitted_30d', 0) or 0
        vector.activity_score = self.scorer.score_activity(
            github_score, profile_views, search_apps, apps_30d,
            vector.evidence['activity']
        )
        
        # Engagement
        completeness = profile.get('profile_completeness_score', 0) or 0
        response_time = signals.get('avg_response_time_hours', 0) or 24
        vector.engagement_score = self.scorer.score_engagement(
            completeness, response_time, resp_rate, vector.evidence['engagement']
        )
        
        # Availability
        open_to_work = profile.get('open_to_work', False) or False
        notice_days = profile.get('notice_period_days', 60) or 60
        relocate = profile.get('willing_to_relocate', False) or False
        vector.availability_score = self.scorer.score_availability(
            open_to_work, notice_days, relocate, vector.evidence['availability']
        )
        
        # Behavior (composite of engagement + activity + responsiveness)
        vector.behavior_score = (vector.engagement_score + vector.activity_score + resp_rate) / 3
        
        # ========== RISK ASSESSMENT ==========
        
        vector.risk_score = self.scorer.detect_risks(candidate_data, vector.risk_flags)
        
        # Convert defaultdict to dict
        vector.evidence = dict(vector.evidence)
        
        return vector
    
    def process_candidates_batch(
        self, candidates_iterator, batch_size: int = 1000
    ) -> List[CandidateFeatureVector]:
        """
        Process candidates in batches with progress tracking.
        
        Args:
            candidates_iterator: Iterator yielding (id, data) tuples
            batch_size: Number of candidates per batch
            
        Returns:
            List of feature vectors
        """
        vectors = []
        batch = []
        
        for candidate_id, candidate_data, error in tqdm(
            candidates_iterator,
            desc="Processing candidates",
            unit="candidate"
        ):
            if error is None and candidate_data is not None:
                try:
                    vector = self.process_candidate(candidate_id, candidate_data)
                    batch.append(vector)
                    
                    if len(batch) >= batch_size:
                        vectors.extend(batch)
                        batch = []
                except Exception as e:
                    logger.warning(f"Error processing candidate {candidate_id}: {e}")
        
        # Add remaining batch
        if batch:
            vectors.extend(batch)
        
        logger.info(f"Processed {len(vectors)} candidates successfully")
        return vectors
    
    def save_to_parquet(self, vectors: List[CandidateFeatureVector], output_path: Path) -> None:
        """
        Save feature vectors to Parquet format.
        
        Args:
            vectors: List of feature vectors
            output_path: Path to save parquet file
        """
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("pandas required. Install with: pip install pandas")
        
        # Convert vectors to list of dicts
        data = []
        for v in vectors:
            d = asdict(v)
            # Convert evidence dict to JSON string for Parquet
            d['evidence'] = json.dumps(d['evidence']) if d['evidence'] else ""
            # Convert risk_flags list to JSON string
            d['risk_flags'] = json.dumps(d['risk_flags']) if d['risk_flags'] else ""
            data.append(d)
        
        df = pd.DataFrame(data)
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(output_path, index=False, engine='pyarrow')
        logger.info(f"Saved {len(vectors)} feature vectors to {output_path}")
    
    def save_evidence_store(
        self, vectors: List[CandidateFeatureVector], output_path: Path
    ) -> None:
        """
        Save evidence store as JSON.
        
        Args:
            vectors: List of feature vectors
            output_path: Path to save JSON file
        """
        evidence_store = {}
        
        for vector in vectors:
            evidence_store[vector.candidate_id] = {
                'evidence': vector.evidence,
                'risk_flags': vector.risk_flags,
                'timestamp': vector.processing_timestamp
            }
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(evidence_store, f, indent=2)
        
        logger.info(f"Saved evidence store for {len(vectors)} candidates to {output_path}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Candidate Feature Engine module loaded")
