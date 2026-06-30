"""FastAPI dependencies placeholder.

Keep this module for dependency injection (e.g., auth, engine clients) later.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

OUTPUT_DIR = BASE_DIR / "outputs"
DATA_DIR = BASE_DIR / "data"