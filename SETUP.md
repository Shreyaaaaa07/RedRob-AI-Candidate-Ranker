# Setup Instructions

## Prerequisites

- **Python**: 3.9 or higher
- **pip**: Latest version (run `pip install --upgrade pip`)
- **Git**: For version control

Check your versions:
```bash
python --version
pip --version
```

## Step 1: Virtual Environment Setup

### Option A: Using venv (Recommended)

```bash
# Navigate to project directory
cd "Redrob AI Candidate Ranker"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Option B: Using conda

```bash
# Create conda environment
conda create -n redrob-ranker python=3.11

# Activate environment
conda activate redrob-ranker
```

## Step 2: Install Dependencies

```bash
# Ensure virtual environment is activated, then:
pip install -r requirements.txt
```

**Installation time**: ~2-5 minutes (depends on internet speed and system specs)

## Step 3: Verify Installation

```bash
# Check Python path
which python  # (macOS/Linux)
where python  # (Windows)

# Check installed packages
pip list

# Run a quick test
python -c "import pandas as pd; import numpy as np; print('✓ Core packages installed')"
```

## Step 4: Development Setup (Optional)

```bash
# Install with development dependencies
pip install -r requirements.txt

# Set up pre-commit hooks (if using git)
pip install pre-commit

# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Run tests
pytest
```

## Step 5: Environment Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings (if needed)
```

## Project Directory Structure

After setup, your project should look like:

```
Redrob AI Candidate Ranker/
├── venv/                          # Virtual environment (created by step 1)
├── data/
│   ├── .gitkeep
├── notebooks/
├── docs/
├── outputs/
│   ├── .gitkeep
├── src/
│   ├── __init__.py
│   ├── data/
│   │   └── __init__.py
│   ├── features/
│   │   └── __init__.py
│   ├── ranking/
│   │   └── __init__.py
│   └── utils/
│       └── __init__.py
├── tests/
│   └── __init__.py
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── pyproject.toml
└── SETUP.md                       # This file
```

## Verification Tests

### Test 1: Import Core Modules

```bash
python -c "from src import data, features, ranking, utils; print('✓ All modules import successfully')"
```

### Test 2: Run Pytest

```bash
pytest --version
pytest tests/
```

### Test 3: Code Quality Check

```bash
black --check src/ tests/
flake8 src/ tests/ --count
mypy src/
```

## Troubleshooting

### Issue: `python: command not found` or `Python not in PATH`
- **Solution**: Ensure Python is installed and added to PATH. Reinstall Python if needed.

### Issue: `No module named 'src'`
- **Solution**: Make sure you're running commands from the project root directory.

### Issue: Permission denied when activating venv
- **Solution** (macOS/Linux): Run `chmod +x venv/bin/activate` then retry

### Issue: Pip install fails with compatibility errors
- **Solution**: Upgrade pip first: `pip install --upgrade pip`
- Then clear pip cache: `pip cache purge`
- Retry installation

### Issue: ModuleNotFoundError after installation
- **Solution**: Verify virtual environment is active
- Reinstall requirements: `pip install --force-reinstall -r requirements.txt`

## Using the Project

### Running Code

```bash
# Activate environment if not already active
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Run Python scripts
python -m src.data.loader

# Run Jupyter notebooks
jupyter notebook notebooks/

# Run tests with coverage
pytest --cov=src tests/
```

### Adding New Dependencies

```bash
# Install new package
pip install package-name

# Add to requirements.txt
pip freeze > requirements.txt
```

### Deactivating Virtual Environment

```bash
deactivate
```

## Next Steps

1. ✅ Verify installation with provided tests
2. 📝 Explore the project structure in [README.md](README.md)
3. 🔧 Start developing in the `src/` directory
4. 📊 Use `notebooks/` for exploratory analysis
5. 🧪 Write tests in `tests/` directory
6. 📦 Document your work in `docs/`

## Getting Help

- Check [README.md](README.md) for project overview
- Review requirements.txt for installed packages
- Run `pip show package-name` for specific package info
- Check official docs: pandas, numpy, scikit-learn, pytest

## Quick Command Reference

```bash
# Activate environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Deactivate environment
deactivate

# Install all dependencies
pip install -r requirements.txt

# Run tests
pytest

# Format code
black src/ tests/

# Check code style
flake8 src/ tests/

# Type checking
mypy src/

# Run Jupyter
jupyter notebook
```

---

**Setup Complete!** 🎉 Your project is ready for development.
