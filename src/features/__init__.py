"""
Feature Engineering Module

Provides intelligent candidate feature engineering based on JD requirements.

Modules:
    jd_parser: Job description parsing and feature extraction
    candidate_feature_engine: Candidate feature vector generation
    feature_pipeline: Main orchestration pipeline
"""

from .jd_parser import JDParser, parse_jd_file, JDFeatures
from .candidate_feature_engine import (
    CandidateFeatureEngine,
    ScoringEngine,
    CandidateFeatureVector
)

__all__ = [
    'JDParser',
    'parse_jd_file',
    'JDFeatures',
    'CandidateFeatureEngine',
    'ScoringEngine',
    'CandidateFeatureVector',
]
