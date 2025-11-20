# Bibliometric Analysis Research Project

## Project Overview
This project uses **Pybliometrics** to conduct bibliometric analysis of publications from the Scopus database.

## What is Pybliometrics?
Pybliometrics is a Python wrapper for the Scopus API that allows you to:
- Search for publications by keywords, authors, or institutions
- Retrieve author profiles and citation metrics
- Analyze publication trends and co-author networks
- Export bibliometric data for further analysis

## Quick Start

### Prerequisites
- Python 3.7+
- Scopus API Key (get at https://dev.elsevier.com/)
- University VPN access (for Scopus API)

### Installation (Windows)

1. **Create virtual environment**
```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
```

2. **Install dependencies**
```bash
   pip install -r requirements.txt --break-system-packages
```

3. **Run initial setup**
```bash
   python setup_pybliometrics.py
```
   Enter your Scopus API Key and InstToken (optional)

4. **Test installation**
```bash
   python scripts/00_install_and_test.py
```

## How to Use

All scripts import from `config/pyblio_config.py`:
```python
from config.pyblio_config import AuthorRetrieval, ScopusSearch

# Your code here
```

## Scripts Available

- `01_author_profile.py` - Analyze author profiles
- `02_publication_search.py` - Search and analyze publications
- `03_data_analysis.py` - Statistical analysis and visualization
