import sys
from pathlib import Path
import logging

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(PROJECT_ROOT))




logger = logging.getLogger(__name__)


class RankService:

    def run_pipeline(self):

        from src.features.feature_pipeline import FeatureEngineeringPipeline
        from src.features.semantic_similarity import SemanticSimilarityEngine
        from src.ranking.feature_normalizer import FeatureNormalizer
        from src.ranking.hybrid_ranker import HybridRanker

        logger.info("Step 1: Feature Engineering...")
        FeatureEngineeringPipeline().run()

        logger.info("Step 2: Semantic Similarity...")
        SemanticSimilarityEngine().run()

        logger.info("Step 3: Feature Normalization...")
        FeatureNormalizer().normalize()

        logger.info("Step 4: Hybrid Ranking...")
        HybridRanker().rank()

        return {
            "status": "success",
            "message": "Ranking pipeline completed successfully."
        }