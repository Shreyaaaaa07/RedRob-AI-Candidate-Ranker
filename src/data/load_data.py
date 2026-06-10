"""
Production-ready data loading pipeline for Redrob AI Candidate Ranker.

This module provides efficient streaming data loading for large-scale candidate datasets.
Handles 100,000+ candidates without excessive memory usage through generators and streaming.

Key Features:
    - Streaming JSONL loading with generators
    - Graceful error handling for malformed JSON
    - Progress tracking with tqdm
    - Schema validation with jsonschema
    - Structured logging
    - Memory-efficient batch processing
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Set, Tuple

import jsonschema
from tqdm import tqdm

# Configure logging
logger = logging.getLogger(__name__)


class CandidateDataLoader:
    """Production-ready data loader for candidate profiles."""

    def __init__(self, data_dir: str = "data", schema_path: Optional[str] = None):
        """
        Initialize the data loader.

        Args:
            data_dir: Path to the data directory containing JSONL and schema files
            schema_path: Path to the JSON schema file for validation
        """
        self.data_dir = Path(data_dir)
        self.schema_path = schema_path or self.data_dir / "candidate_schema.json"
        self._schema: Optional[Dict[str, Any]] = None

    @property
    def schema(self) -> Dict[str, Any]:
        """Lazy-load and cache the JSON schema."""
        if self._schema is None:
            if self.schema_path.exists():
                with open(self.schema_path, "r", encoding="utf-8") as f:
                    self._schema = json.load(f)
                logger.info(f"Loaded schema from {self.schema_path}")
            else:
                logger.warning(
                    f"Schema file not found at {self.schema_path}. "
                    "Validation will be skipped."
                )
                self._schema = {}
        return self._schema

    def load_candidates(
        self,
        filename: str = "candidates.jsonl",
        show_progress: bool = True,
        validate: bool = False,
        skip_errors: bool = True,
    ) -> Generator[Tuple[str, Dict[str, Any], Optional[str]], None, None]:
        """
        Stream candidates from JSONL file efficiently using a generator.

        This function yields candidates one at a time, minimizing memory usage
        for large datasets. Perfect for processing 100,000+ records.

        Args:
            filename: Name of the JSONL file in data_dir
            show_progress: Whether to show progress bar
            validate: Whether to validate against schema
            skip_errors: If True, skip malformed records and log warnings.
                        If False, raise exceptions on bad records.

        Yields:
            Tuple of (candidate_id, candidate_dict, error_message or None)
            If error_message is not None, the candidate_dict will be None.

        Example:
            >>> loader = CandidateDataLoader()
            >>> for cand_id, cand_data, error in loader.load_candidates():
            ...     if error:
            ...         print(f"Skipped {cand_id}: {error}")
            ...     else:
            ...         process_candidate(cand_data)
        """
        filepath = self.data_dir / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Candidate file not found: {filepath}")

        logger.info(f"Loading candidates from {filepath}")

        # Count total lines for progress bar
        total_lines = self._count_lines(filepath) if show_progress else None

        success_count = 0
        error_count = 0

        with open(filepath, "r", encoding="utf-8") as f:
            iterator = (
                tqdm(f, total=total_lines, desc="Loading candidates")
                if show_progress
                else f
            )

            for line_num, line in enumerate(iterator, 1):
                line = line.strip()
                if not line:  # Skip empty lines
                    continue

                try:
                    # Parse JSON
                    candidate = json.loads(line)

                    # Validate against schema if requested
                    if validate and self.schema:
                        try:
                            jsonschema.validate(candidate, self.schema)
                        except jsonschema.ValidationError as e:
                            error_msg = f"Schema validation failed: {e.message}"
                            if skip_errors:
                                logger.warning(
                                    f"Line {line_num}: {error_msg}. Skipping record."
                                )
                                error_count += 1
                                yield None, None, error_msg
                                continue
                            else:
                                raise

                    # Extract candidate_id
                    candidate_id = candidate.get("candidate_id")
                    success_count += 1
                    yield candidate_id, candidate, None

                except json.JSONDecodeError as e:
                    error_msg = f"JSON decode error on line {line_num}: {str(e)}"
                    logger.warning(error_msg)
                    error_count += 1

                    if not skip_errors:
                        raise ValueError(error_msg) from e

                    yield None, None, error_msg

                except Exception as e:
                    error_msg = f"Unexpected error on line {line_num}: {str(e)}"
                    logger.error(error_msg)
                    error_count += 1

                    if not skip_errors:
                        raise

                    yield None, None, error_msg

        logger.info(
            f"Loading complete. Success: {success_count}, Errors: {error_count}"
        )

    def load_candidates_batch(
        self,
        filename: str = "candidates.jsonl",
        batch_size: int = 1000,
        show_progress: bool = True,
        validate: bool = False,
        skip_errors: bool = True,
    ) -> Generator[List[Dict[str, Any]], None, None]:
        """
        Load candidates in batches for efficient bulk processing.

        Args:
            filename: Name of the JSONL file
            batch_size: Number of candidates per batch
            show_progress: Whether to show progress bar
            validate: Whether to validate against schema
            skip_errors: Whether to skip malformed records

        Yields:
            Lists of candidate dictionaries

        Example:
            >>> loader = CandidateDataLoader()
            >>> for batch in loader.load_candidates_batch(batch_size=5000):
            ...     process_batch(batch)
        """
        batch = []

        for _, candidate, error in self.load_candidates(
            filename=filename,
            show_progress=show_progress,
            validate=validate,
            skip_errors=skip_errors,
        ):
            if error is None and candidate is not None:
                batch.append(candidate)

                if len(batch) >= batch_size:
                    yield batch
                    batch = []

        # Yield remaining candidates
        if batch:
            yield batch

    def load_sample_candidates(
        self, filename: str = "sample_candidates.json"
    ) -> List[Dict[str, Any]]:
        """
        Load sample candidates from a JSON file for quick testing.

        Args:
            filename: Name of the JSON file in data_dir

        Returns:
            List of candidate dictionaries

        Example:
            >>> loader = CandidateDataLoader()
            >>> samples = loader.load_sample_candidates()
        """
        filepath = self.data_dir / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Sample file not found: {filepath}")

        logger.info(f"Loading sample candidates from {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            candidates = json.load(f)

        logger.info(f"Loaded {len(candidates)} sample candidates")
        return candidates

    def get_candidate_count(self, filename: str = "candidates.jsonl") -> int:
        """
        Get the total number of candidates in the JSONL file.

        Note: This requires reading the file once. For large files,
        consider caching the result.

        Args:
            filename: Name of the JSONL file

        Returns:
            Total number of valid candidate records

        Example:
            >>> loader = CandidateDataLoader()
            >>> count = loader.get_candidate_count()
            >>> print(f"Total candidates: {count}")
        """
        filepath = self.data_dir / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Candidate file not found: {filepath}")

        count = 0
        error_count = 0

        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    json.loads(line)
                    count += 1
                except json.JSONDecodeError:
                    error_count += 1

        logger.info(
            f"Candidate file contains {count} valid records "
            f"({error_count} malformed records)"
        )
        return count

    def validate_candidate_schema(
        self, candidate: Dict[str, Any], raise_exception: bool = False
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate a single candidate record against the schema.

        Args:
            candidate: Candidate dictionary to validate
            raise_exception: If True, raise ValidationError on invalid records

        Returns:
            Tuple of (is_valid, error_message)
            If is_valid is True, error_message is None.

        Example:
            >>> loader = CandidateDataLoader()
            >>> is_valid, error = loader.validate_candidate_schema(cand)
            >>> if not is_valid:
            ...     print(f"Invalid: {error}")
        """
        if not self.schema:
            return True, None

        try:
            jsonschema.validate(candidate, self.schema)
            return True, None
        except jsonschema.ValidationError as e:
            error_msg = f"Validation error at {'.'.join(str(p) for p in e.path)}: {e.message}"
            if raise_exception:
                raise
            logger.warning(error_msg)
            return False, error_msg

    def extract_required_fields(
        self, candidate: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract a flattened dictionary of key candidate fields.

        Useful for quick profiling and analysis without full nested structure.

        Args:
            candidate: Full candidate dictionary

        Returns:
            Dictionary with commonly-used fields

        Example:
            >>> loader = CandidateDataLoader()
            >>> fields = loader.extract_required_fields(candidate)
        """
        profile = candidate.get("profile", {})
        signals = candidate.get("redrob_signals", {})
        skills = candidate.get("skills", [])
        education = candidate.get("education", [])
        career = candidate.get("career_history", [])

        return {
            "candidate_id": candidate.get("candidate_id"),
            # Profile fields
            "years_of_experience": profile.get("years_of_experience", 0),
            "current_title": profile.get("current_title"),
            "current_company": profile.get("current_company"),
            "current_industry": profile.get("current_industry"),
            "country": profile.get("country"),
            # Skills
            "num_skills": len(skills),
            "top_skills": [s.get("name") for s in skills[:5]],
            "total_endorsements": sum(s.get("endorsements", 0) for s in skills),
            # Education
            "num_degrees": len(education),
            "highest_degree_tier": (
                education[0].get("tier") if education else "unknown"
            ),
            # Career history
            "num_previous_jobs": max(0, len(career) - 1),
            # Signals
            "profile_completeness": signals.get("profile_completeness_score", 0),
            "recruiter_response_rate": signals.get("recruiter_response_rate", 0),
            "github_activity_score": signals.get("github_activity_score", -1),
            "open_to_work": signals.get("open_to_work_flag", False),
            "saved_by_recruiters_30d": signals.get("saved_by_recruiters_30d", 0),
        }

    @staticmethod
    def _count_lines(filepath: Path) -> int:
        """Count total lines in a file efficiently."""
        count = 0
        with open(filepath, "rb") as f:
            for _ in f:
                count += 1
        return count


# Convenience functions for quick access
def load_candidates(
    data_dir: str = "data",
    batch_size: Optional[int] = None,
    show_progress: bool = True,
    validate: bool = False,
) -> Generator[Any, None, None]:
    """
    Load candidates with sensible defaults.

    Args:
        data_dir: Path to data directory
        batch_size: If specified, yields batches instead of individual records
        show_progress: Whether to show progress bar
        validate: Whether to validate against schema

    Yields:
        Individual candidates or batches of candidates
    """
    loader = CandidateDataLoader(data_dir=data_dir)

    if batch_size:
        yield from loader.load_candidates_batch(
            batch_size=batch_size,
            show_progress=show_progress,
            validate=validate,
        )
    else:
        for _, candidate, error in loader.load_candidates(
            show_progress=show_progress,
            validate=validate,
        ):
            if error is None:
                yield candidate


def get_candidate_count(data_dir: str = "data") -> int:
    """Get total candidate count."""
    loader = CandidateDataLoader(data_dir=data_dir)
    return loader.get_candidate_count()


if __name__ == "__main__":
    # Quick test
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    loader = CandidateDataLoader()

    # Test 1: Count candidates
    count = loader.get_candidate_count()
    print(f"✓ Total candidates: {count}")

    # Test 2: Load samples
    try:
        samples = loader.load_sample_candidates()
        print(f"✓ Loaded {len(samples)} sample candidates")
    except FileNotFoundError:
        print("⚠ Sample file not found (expected in new setup)")

    # Test 3: Stream a few candidates
    print("\n✓ Streaming first 3 candidates:")
    for i, (cand_id, cand_data, error) in enumerate(loader.load_candidates()):
        if error is None:
            print(f"  - {cand_id}: {cand_data.get('profile', {}).get('current_title')}")
        if i >= 2:
            break
