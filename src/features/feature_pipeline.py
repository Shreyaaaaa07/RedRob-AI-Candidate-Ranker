"""
Main Feature Engineering Pipeline Orchestrator

Orchestrates the complete feature engineering process:
1. Parse job description
2. Load candidate data
3. Process all candidates through feature engine
4. Generate outputs

Usage:
    python src/features/feature_pipeline.py
"""

import json
import logging
from pathlib import Path
from datetime import datetime

from src.features.jd_parser import parse_jd_file
from src.features.candidate_feature_engine import CandidateFeatureEngine
from src.data.load_data import CandidateDataLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FeatureEngineeringPipeline:
    """
    Complete feature engineering pipeline for intelligent candidate ranking.
    """
    
    def __init__(
        self,
        data_dir: Path = Path("data"),
        output_dir: Path = Path("outputs"),
        jd_filename: str = "job_description.docx",
        candidates_filename: str = "candidates.jsonl"
    ):
        """
        Initialize pipeline.
        
        Args:
            data_dir: Directory with input data
            output_dir: Directory for output files
            jd_filename: Job description filename
            candidates_filename: Candidates JSONL filename
        """
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.jd_path = self.data_dir / jd_filename
        self.candidates_path = self.data_dir / candidates_filename
        
        self.jd_features = None
        self.feature_engine = None
    
    def run(self) -> None:
        """Execute complete pipeline"""
        logger.info("=" * 80)
        logger.info("FEATURE ENGINEERING PIPELINE STARTED")
        logger.info("=" * 80)
        
        try:
            # Step 1: Parse JD
            logger.info("\nStep 1: Parsing Job Description")
            self._parse_jd()
            
            # Step 2: Initialize feature engine
            logger.info("\nStep 2: Initializing Feature Engine")
            self._init_feature_engine()
            
            # Step 3: Process candidates
            logger.info("\nStep 3: Processing Candidates")
            vectors = self._process_candidates()
            
            # Step 4: Generate outputs
            logger.info("\nStep 4: Generating Outputs")
            self._generate_outputs(vectors)
            
            logger.info("\n" + "=" * 80)
            logger.info("PIPELINE COMPLETED SUCCESSFULLY")
            logger.info("=" * 80)
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}", exc_info=True)
            raise
    
    def _parse_jd(self) -> None:
        """Parse job description into structured features"""
        if not self.jd_path.exists():
            raise FileNotFoundError(f"JD file not found: {self.jd_path}")
        
        logger.info(f"Parsing JD from: {self.jd_path}")
        
        jd_output_path = self.output_dir / "jd_features.json"
        self.jd_features = parse_jd_file(self.jd_path, jd_output_path)
        
        logger.info(f"✓ Parsed JD: {self.jd_features.role_title}")
        logger.info(f"  Experience: {self.jd_features.required_experience_min}-{self.jd_features.required_experience_max} years")
        logger.info(f"  Must-have skills: {len(self.jd_features.must_have_skills)}")
        logger.info(f"  Preferred skills: {len(self.jd_features.preferred_skills)}")
        logger.info(f"  Tools: {', '.join(self.jd_features.required_tools)}")
        logger.info(f"  Anti-patterns: {len(self.jd_features.anti_patterns)}")
    
    def _init_feature_engine(self) -> None:
        """Initialize feature engine with JD features"""
        # Convert JD features to dict
        jd_dict = {
            'role_title': self.jd_features.role_title,
            'required_experience_min': self.jd_features.required_experience_min,
            'required_experience_max': self.jd_features.required_experience_max,
            'must_have_skills': self.jd_features.must_have_skills,
            'preferred_skills': self.jd_features.preferred_skills,
            'required_tools': self.jd_features.required_tools,
            'required_domains': self.jd_features.required_domains,
        }
        
        self.feature_engine = CandidateFeatureEngine(jd_dict)
        logger.info("✓ Feature engine initialized")
    
    def _process_candidates(self) -> list:
        """Load and process all candidates"""
        if not self.candidates_path.exists():
            raise FileNotFoundError(f"Candidates file not found: {self.candidates_path}")
        
        logger.info(f"Loading candidates from: {self.candidates_path}")
        
        # Initialize data loader
        loader = CandidateDataLoader()
        
        # Get total count
        total = loader.get_candidate_count()
        logger.info(f"Total candidates: {total}")
        
        # Process candidates
        vectors = self.feature_engine.process_candidates_batch(
            loader.load_candidates(skip_errors=True, show_progress=True),
            batch_size=1000
        )
        
        logger.info(f"✓ Processed {len(vectors)} candidates")
        
        return vectors
    
    def _generate_outputs(self, vectors: list) -> None:
        """Generate output files"""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. Save to Parquet (efficient storage)
        parquet_path = self.output_dir / "candidate_features.parquet"
        logger.info(f"Saving to Parquet: {parquet_path}")
        self.feature_engine.save_to_parquet(vectors, parquet_path)
        logger.info(f"✓ Saved {len(vectors)} vectors to Parquet")
        
        # 2. Save evidence store
        evidence_path = self.output_dir / "evidence_store.json"
        logger.info(f"Saving evidence store: {evidence_path}")
        self.feature_engine.save_evidence_store(vectors, evidence_path)
        logger.info(f"✓ Saved evidence store")
        
        # 3. Generate summary statistics
        self._generate_summary(vectors)
    
    def _generate_summary(self, vectors: list) -> None:
        """Generate summary statistics"""
        import numpy as np
        
        summary = {
            'processing_timestamp': datetime.now().isoformat(),
            'jd': {
                'title': self.jd_features.role_title,
                'experience_range': f"{self.jd_features.required_experience_min}-{self.jd_features.required_experience_max}y",
                'must_have_skills_count': len(self.jd_features.must_have_skills),
                'preferred_skills_count': len(self.jd_features.preferred_skills),
            },
            'candidates_processed': len(vectors),
            'score_statistics': {}
        }
        
        # Calculate statistics for each score
        score_fields = [
            'experience_match_score', 'skill_match_score', 'production_ml_score',
            'retrieval_score', 'vector_database_score', 'ranking_system_score',
            'evaluation_framework_score', 'startup_fit_score', 'open_source_score',
            'education_score', 'career_stability_score', 'experience_consistency_score',
            'recruiter_interest_score', 'activity_score', 'engagement_score',
            'availability_score', 'behavior_score', 'risk_score'
        ]
        
        for field in score_fields:
            scores = [getattr(v, field) for v in vectors]
            if len(scores) == 0:
                continue
                        
            summary['score_statistics'][field] = {
                'mean': float(np.mean(scores)),
                'median': float(np.median(scores)),
                'min': float(np.min(scores)),
                'max': float(np.max(scores)),
                'std': float(np.std(scores)),
            }
        
        # Risk statistics
        risk_flags_count = {}
        for v in vectors:
            for flag in v.risk_flags:
                # Extract flag type (first part before colon)
                flag_type = flag.split(':')[0].strip()
                risk_flags_count[flag_type] = risk_flags_count.get(flag_type, 0) + 1
        
        summary['risk_analysis'] = {
            'total_flags': sum(len(v.risk_flags) for v in vectors),
            'candidates_with_risk': sum(1 for v in vectors if v.risk_flags),
            'flag_breakdown': risk_flags_count,
        }
        
        # Save summary
        summary_path = self.output_dir / "feature_engineering_summary.json"
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"✓ Generated summary: {summary_path}")
        
        # Print summary to console
        logger.info("\n" + "=" * 60)
        logger.info("FEATURE ENGINEERING SUMMARY")
        logger.info("=" * 60)
        logger.info(f"JD: {self.jd_features.role_title}")
        logger.info(f"Candidates processed: {len(vectors)}")
        logger.info(f"Candidates with risk flags: {summary['risk_analysis']['candidates_with_risk']}")
        logger.info(f"Total risk flags: {summary['risk_analysis']['total_flags']}")
        logger.info("\nTop score statistics:")
        
        for field in ['experience_match_score', 'production_ml_score', 'retrieval_score',
                      'recruiter_interest_score', 'career_stability_score']:
            if field in summary['score_statistics']:
                stats = summary['score_statistics'][field]
                logger.info(f"  {field}: mean={stats['mean']:.1f}, median={stats['median']:.1f}, "
                          f"range=[{stats['min']:.1f}, {stats['max']:.1f}]")


def main():
    """Main entry point"""
    import sys
    
    try:
        pipeline = FeatureEngineeringPipeline()
        pipeline.run()
        
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
