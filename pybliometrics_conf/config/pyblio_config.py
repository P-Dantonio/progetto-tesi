"""
PYBLIOMETRICS CONFIGURATION MODULE
========================================

This module handles all Pybliometrics configuration for Windows systems.
It automatically initializes the CONFIG variable and creates necessary directories.

USAGE:
    from config.pyblio_config import AuthorRetrieval, ScopusSearch
    
    au = AuthorRetrieval("author_id")
    results = ScopusSearch("TITLE(keywords)")

This module should be imported in ALL your scripts instead of importing
directly from pybliometrics.scopus

IMPORTANT: Windows-specific configuration
Pybliometrics 4.x has specific configuration requirements on Windows.
This module handles all of that automatically.
"""

import os
from pathlib import Path
import configparser

# ============================================================================
# STEP 1: Configuration Setup
# ============================================================================

# Set the configuration file path
config_file = Path.home() / '.pybliometrics' / 'config.ini'
os.environ['PYB_CONFIG_FILE'] = str(config_file)

# ============================================================================
# STEP 2: Initialize CONFIG Variable
# ============================================================================
# This is critical for Pybliometrics 4.x on Windows
# The get_config() function checks this global variable

import pybliometrics.utils.startup as startup

# Read the configuration file
config = configparser.ConfigParser()
config.read(config_file)

# Set the CONFIG variable that Pybliometrics checks
startup.CONFIG = config

# ============================================================================
# STEP 3: Create Directory Structure
# ============================================================================
# Pybliometrics needs specific directory structure for caching results
# These are created automatically the first time, but we ensure they exist

scopus_dir = Path.home() / '.pybliometrics' / 'Scopus'

subdirs = [
    'abstract_retrieval/STANDARD',
    'abstract_retrieval/COMPLETE',
    'abstract_retrieval/FULL',
    'abstract_retrieval/REF',
    'author_retrieval/STANDARD',
    'author_retrieval/COMPLETE', 
    'author_retrieval/ENHANCED',
    'author_search',
    'affiliation_retrieval',
    'affiliation_search',
    'citation_overview',
    'scopus_search',
    'serial_search',
    'serial_title',
    'plumx',
    'subject_classification'
]

for subdir in subdirs:
    (scopus_dir / subdir).mkdir(parents=True, exist_ok=True)

# ============================================================================
# STEP 4: Import Pybliometrics Classes
# ============================================================================
# Now that configuration is set up, we can import and export the main classes

from pybliometrics.scopus import (
    ScopusSearch,           # Search for publications
    AuthorRetrieval,        # Get author information
    AbstractRetrieval,      # Get publication details
    AffiliationRetrieval,   # Get institution information
    AuthorSearch,           # Search for authors
    AffiliationSearch,      # Search for institutions
    SerialSearch,           # Search for journals
    SerialTitle,            # Get journal information
    PlumXMetrics,           # Get PlumX article metrics
    SubjectClassifications  # Get subject area classifications
)

from pybliometrics.scopus.abstract_retrieval import AbstractRetrieval

# ============================================================================
# EXPORT ALL CLASSES
# ============================================================================
# These are all the classes available for import

__all__ = [
    'ScopusSearch',
    'AuthorRetrieval',
    'AbstractRetrieval',
    'AffiliationRetrieval',
    'AuthorSearch',
    'AffiliationSearch',
    'SerialSearch',
    'SerialTitle',
    'PlumXMetrics',
    'SubjectClassifications'
]

# ============================================================================
# USAGE EXAMPLES
# ============================================================================
"""
Example 1: Retrieve Author Profile
    from config.pyblio_config import AuthorRetrieval
    
    au = AuthorRetrieval("7004212771")
    print(f"Name: {au.given_name} {au.surname}")
    print(f"Documents: {au.document_count}")
    print(f"Citations: {au.citation_count}")
    print(f"h-index: {au.h_index}")

Example 2: Search Publications
    from config.pyblio_config import ScopusSearch
    
    query = "TITLE-ABS-KEY(machine learning) AND PUBYEAR > 2020"
    results = ScopusSearch(query, download=False)
    print(f"Found {results.get_results_size()} results")

Example 3: Get Publication Details
    from config.pyblio_config import AbstractRetrieval
    
    pub = AbstractRetrieval("doi_or_eid")
    print(f"Title: {pub.title}")
    print(f"Authors: {pub.author_names}")
    print(f"Citations: {pub.citedby_count}")
"""
