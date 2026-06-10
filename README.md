# Redrob AI Candidate Ranker

A production-ready Python application for ranking and analyzing candidates at scale. Designed to process 100,000+ candidates efficiently using machine learning and data-driven insights.

## Overview

This project provides a robust foundation for candidate ranking with support for large-scale data processing, feature engineering, and ranking algorithms. Built with scalability, maintainability, and performance in mind.

## Project Structure

```
redrob-ai-ranker/
├── data/                    # Raw and processed candidate data
│   ├── raw/                # Original data files
│   └── processed/          # Cleaned and processed data
├── notebooks/              # Jupyter notebooks for exploration
├── docs/                   # Documentation
├── outputs/                # Generated outputs and results
├── src/                    # Production source code
│   ├── data/              # Data loading and preprocessing
│   ├── features/          # Feature engineering modules
│   ├── ranking/           # Ranking algorithms
│   └── utils/             # Utility functions
├── tests/                 # Unit and integration tests
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── .gitignore            # Git ignore rules
```

## Features

- **Scalable Data Processing**: Handle 100,000+ candidates efficiently
- **Modular Architecture**: Clean separation of concerns for data, features, and ranking
- **Type Hints**: Full type annotations for better code quality
- **Testing**: Comprehensive test suite with pytest
- **Code Quality**: Black, Flake8, isort, and mypy for linting and formatting

## Installation

### Prerequisites
- Python 3.9+
- pip or conda

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd redrob-ai-ranker
   ```

2. **Create a virtual environment**
   ```bash
   # Using venv
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   source venv/bin/activate      # On macOS/Linux
   
   # Or using conda
   conda create -n redrob-ranker python=3.11
   conda activate redrob-ranker
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env  # Create your own .env file
   ```

## Quick Start

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_data.py -v
```

### Code Quality Checks
```bash
# Format code with Black
black src/ tests/

# Sort imports
isort src/ tests/

# Lint with Flake8
flake8 src/ tests/

# Type checking with mypy
mypy src/
```

## Development Workflow

### 1. Data Loading (`src/data/`)
- Data ingestion and validation
- Schema management
- Handling large datasets

### 2. Feature Engineering (`src/features/`)
- Feature extraction
- Feature transformations
- Feature scaling and normalization

### 3. Ranking (`src/ranking/`)
- Ranking algorithms
- Score calculation
- Result aggregation

### 4. Utilities (`src/utils/`)
- Helper functions
- Logging utilities
- Configuration management

## Configuration

Create a `.env` file in the project root:
```env
# Data paths
DATA_RAW_PATH=data/raw
DATA_PROCESSED_PATH=data/processed
OUTPUT_PATH=outputs

# Processing
BATCH_SIZE=1000
NUM_WORKERS=4

# Logging
LOG_LEVEL=INFO
```

## Dependencies

### Core Libraries
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **scikit-learn**: Machine learning utilities
- **scipy**: Scientific computing

### Data Validation
- **pydantic**: Data validation using Python type hints

### Testing & Quality
- **pytest**: Testing framework
- **pytest-cov**: Coverage measurement
- **black**: Code formatting
- **flake8**: Linting
- **mypy**: Static type checking
- **isort**: Import sorting

### Utilities
- **tqdm**: Progress bars for long operations
- **loguru**: Enhanced logging
- **python-dotenv**: Environment variable management
- **pyarrow**: Efficient data serialization

## Documentation

See the [docs/](docs/) directory for detailed documentation on:
- Data format specifications
- API documentation
- Architecture decisions
- Performance optimization

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Follow PEP 8 style guide
3. Add tests for new features
4. Run code quality checks before committing
5. Submit a pull request

## Performance Considerations

When processing 100,000+ candidates:
- Use batch processing for memory efficiency
- Leverage multiprocessing for CPU-bound tasks
- Monitor memory usage with large datasets
- Consider using Parquet format for faster I/O
- Profile code with profiling tools before optimization

## License

[Add your license information here]

## Contact

For questions or issues, please create an issue in the repository.

## Roadmap

- [ ] Ranking algorithm implementation
- [ ] Embedding generation pipeline
- [ ] REST API for serving rankings
- [ ] Web dashboard for results visualization
- [ ] Performance optimization and benchmarking
- [ ] Docker containerization
- [ ] CI/CD pipeline setup

## Status

🚀 **Project Foundation** - Ready for feature development
