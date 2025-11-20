from pathlib import Path
import os

def setup_pybliometrics_windows(api_key):
    """
    Setup Pybliometrics configuration for Windows
    """
    # Create config directory
    config_dir = Path.home() / '.pybliometrics'
    config_dir.mkdir(exist_ok=True)
    
    # Create config file
    config_file = config_dir / 'config.ini'
    
    config_content = f"""[Directories]
AbstractRetrieval = {config_dir}\\Scopus\\abstract_retrieval
AffiliationRetrieval = {config_dir}\\Scopus\\affiliation_retrieval
AffiliationSearch = {config_dir}\\Scopus\\affiliation_search
AuthorRetrieval = {config_dir}\\Scopus\\author_retrieval
AuthorSearch = {config_dir}\\Scopus\\author_search
CitationOverview = {config_dir}\\Scopus\\citation_overview
ScopusSearch = {config_dir}\\Scopus\\scopus_search
SerialSearch = {config_dir}\\Scopus\\serial_search
SerialTitle = {config_dir}\\Scopus\\serial_title
PlumXMetrics = {config_dir}\\Scopus\\plumx
SubjectClassifications = {config_dir}\\Scopus\\subject_classification

[Authentication]
APIKey = {api_key}
"""
    
    with open(config_file, 'w') as f:
        f.write(config_content)
    
    # Create all subdirectories
    scopus_dir = config_dir / 'Scopus'
    subdirs = ['abstract_retrieval', 'affiliation_retrieval', 'affiliation_search', 
               'author_retrieval', 'author_search', 'citation_overview', 
               'scopus_search', 'serial_search', 'serial_title', 'plumx', 
               'subject_classification']
    
    for subdir in subdirs:
        (scopus_dir / subdir).mkdir(parents=True, exist_ok=True)
    
    print(f"✓ Configuration created at: {config_file}")
    print(f"✓ All directories created in: {scopus_dir}")
    return config_file

# Run setup
if __name__ == "__main__":
    API_KEY = input("Enter your Scopus API key: ")
    config_file = setup_pybliometrics_windows(API_KEY)
    
    # Test the configuration
    print("\nTesting configuration...")
    try:
        from pybliometrics.scopus import AuthorRetrieval
        au = AuthorRetrieval("7004212771")
        print(f"\n✓ SUCCESS! Retrieved: {au.given_name} {au.surname}")
        print(f"  Documents: {au.document_count}")
        print(f"  Citations: {au.citation_count}")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print(f"\nConfig file location: {config_file}")
        print("Please check if the API key is correct and you have VPN access.")
