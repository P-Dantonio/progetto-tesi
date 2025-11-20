"""
ONE-TIME SETUP SCRIPT for Pybliometrics Configuration
Run this once at the beginning to configure Pybliometrics
After running, you can delete this file
"""

from pathlib import Path
import os

def setup_pybliometrics():
    """
    Create Pybliometrics configuration directory structure
    """
    print("=" * 70)
    print("PYBLIOMETRICS CONFIGURATION SETUP")
    print("=" * 70)
    print("\nThis script will configure Pybliometrics for your project.\n")
    
    # Get API credentials from user
    api_key = input("Enter your Scopus API Key: ").strip()
    if not api_key:
        print("ERROR: API Key is required!")
        return False
    
    insttoken = input("Enter your InstToken (optional, press Enter to skip): ").strip()
    
    # Create config directory
    config_dir = Path.home() / '.pybliometrics'
    config_dir.mkdir(exist_ok=True)
    
    config_file = config_dir / 'config.ini'
    
    # Create configuration
    config_content = f"""[Authentication]
APIKey = {api_key}
InstToken = {insttoken}

[Directories]
AbstractRetrieval = {config_dir}/Scopus/abstract_retrieval
AuthorRetrieval = {config_dir}/Scopus/author_retrieval
AuthorSearch = {config_dir}/Scopus/author_search
AffiliationRetrieval = {config_dir}/Scopus/affiliation_retrieval
AffiliationSearch = {config_dir}/Scopus/affiliation_search
CitationOverview = {config_dir}/Scopus/citation_overview
ScopusSearch = {config_dir}/Scopus/scopus_search
SerialSearch = {config_dir}/Scopus/serial_search
SerialTitle = {config_dir}/Scopus/serial_title
PlumXMetrics = {config_dir}/Scopus/plumx
SubjectClassifications = {config_dir}/Scopus/subject_classification
"""
    
    # Write config file
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print(f"\n✓ Config file created at: {config_file}")
    
    # Create directory structure with all view types
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
        (config_dir / 'Scopus' / subdir).mkdir(parents=True, exist_ok=True)
    
    print("✓ All directories created")
    print("\n" + "=" * 70)
    print("SETUP COMPLETE!")
    print("=" * 70)
    print("\nNext step: Run 'python scripts/00_install_and_test.py'")
    print("\nYou can now delete this setup script if desired.")
    
    return True

if __name__ == "__main__":
    setup_pybliometrics()
