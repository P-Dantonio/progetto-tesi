# pybliometrics_fix.py
from pathlib import Path
import os

def setup_config():
    """Setup Pybliometrics configuration for Windows"""
    
    # Your credentials
    api_key = "ea3e460a194a1ad1feacfe085a65c189"
    insttoken = "f4a5b71fc4063e9f0b60575bb01fe426"
    
    # Config directory
    config_dir = Path.home() / '.pybliometrics'
    config_dir.mkdir(exist_ok=True)
    
    config_file = config_dir / 'config.ini'
    
    # Create config with forward slashes (works better on Windows)
    config_content = f"""[Directories]
AbstractRetrieval = {config_dir}/Scopus/abstract_retrieval
AffiliationRetrieval = {config_dir}/Scopus/affiliation_retrieval
AffiliationSearch = {config_dir}/Scopus/affiliation_search
AuthorRetrieval = {config_dir}/Scopus/author_retrieval
AuthorSearch = {config_dir}/Scopus/author_search
CitationOverview = {config_dir}/Scopus/citation_overview
ScopusSearch = {config_dir}/Scopus/scopus_search
SerialSearch = {config_dir}/Scopus/serial_search
SerialTitle = {config_dir}/Scopus/serial_title
PlumXMetrics = {config_dir}/Scopus/plumx
SubjectClassifications = {config_dir}/Scopus/subject_classification

[Authentication]
APIKey = {api_key}
InstToken = {insttoken}
"""
    
    # Write config
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    # Create all subdirectories
    subdirs = ['abstract_retrieval', 'affiliation_retrieval', 'affiliation_search', 
               'author_retrieval', 'author_search', 'citation_overview', 
               'scopus_search', 'serial_search', 'serial_title', 'plumx', 
               'subject_classification']
    
    for subdir in subdirs:
        (config_dir / 'Scopus' / subdir).mkdir(parents=True, exist_ok=True)
    
    print(f"✓ Config created at: {config_file}")
    print(f"✓ All directories created")
    
    return config_file

# Setup configuration
print("Setting up Pybliometrics...\n")
config_file = setup_config()

# Set environment variable BEFORE importing
os.environ['PYB_CONFIG_FILE'] = str(config_file)
print(f"✓ Environment variable set: {os.environ['PYB_CONFIG_FILE']}\n")

# Verify config file
print("Config file contents:")
print("="*60)
with open(config_file, 'r') as f:
    print(f.read())
print("="*60 + "\n")

# Now import and test (no trying to import config module)
print("Importing pybliometrics...")
from pybliometrics.scopus import AuthorRetrieval

print("Testing with author ID 7004212771...\n")

try:
    au = AuthorRetrieval("7004212771")
    
    print("="*60)
    print("✓✓✓ SUCCESS! ✓✓✓")
    print("="*60)
    print(f"\nAuthor: {au.given_name} {au.surname}")
    print(f"Affiliation: {au.affiliation_current}")
    print(f"Documents: {au.document_count}")
    print(f"Citations: {au.citation_count}")
    print(f"h-index: {au.h_index}")
    print("\n" + "="*60)
    
except Exception as e:
    print("="*60)
    print("✗ Error occurred:")
    print("="*60)
    print(f"{e}\n")
    
    import traceback
    traceback.print_exc()
    
    print("\n" + "="*60)
    print("NEXT STEP: Close Python and run this in a NEW session:")
    print("="*60)
    print("""
import os
from pathlib import Path

config_file = Path.home() / '.pybliometrics' / 'config.ini'
os.environ['PYB_CONFIG_FILE'] = str(config_file)

from pybliometrics.scopus import AuthorRetrieval
au = AuthorRetrieval("7004212771")
print(f"Success! {au.given_name} {au.surname}")
    """)
