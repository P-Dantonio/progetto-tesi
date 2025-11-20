# pyblio_config.py - FINAL WORKING VERSION
"""
Pybliometrics 4.3 configuration helper for Windows
Auto-initializes CONFIG and creates directory structure

Usage:
    from pyblio_config import AuthorRetrieval, ScopusSearch
"""

import os
from pathlib import Path
import configparser

# Config file path
config_file = Path.home() / '.pybliometrics' / 'config.ini'
os.environ['PYB_CONFIG_FILE'] = str(config_file)

# Initialize CONFIG variable
import pybliometrics.utils.startup as startup
config = configparser.ConfigParser()
config.read(config_file)
startup.CONFIG = config

# Create all necessary subdirectories
scopus_dir = Path.home() / '.pybliometrics' / 'Scopus'
subdirs = [
    'abstract_retrieval/STANDARD', 'abstract_retrieval/COMPLETE',
    'abstract_retrieval/FULL', 'abstract_retrieval/REF',
    'author_retrieval/STANDARD', 'author_retrieval/COMPLETE', 
    'author_retrieval/ENHANCED', 'author_search',
    'affiliation_retrieval', 'affiliation_search',
    'citation_overview', 'scopus_search', 'serial_search',
    'serial_title', 'plumx', 'subject_classification'
]
for subdir in subdirs:
    (scopus_dir / subdir).mkdir(parents=True, exist_ok=True)

# Import classes
from pybliometrics.scopus import (
    ScopusSearch, AuthorRetrieval, AbstractRetrieval,
    AffiliationRetrieval, AuthorSearch, AffiliationSearch,
    SerialSearch, SerialTitle, PlumXMetrics, SubjectClassifications
)


__all__ = [
    'ScopusSearch', 'AuthorRetrieval', 'AbstractRetrieval',
    'AffiliationRetrieval', 'AuthorSearch',
    'AffiliationSearch', 'SerialSearch', 'SerialTitle',
    'PlumXMetrics', 'SubjectClassifications'
]