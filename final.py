# working_solution.py
import os
from pathlib import Path
import configparser

# Your config file
config_file = Path.home() / '.pybliometrics' / 'config.ini'
print(f"Config file: {config_file}")
print(f"Exists: {config_file.exists()}\n")

# Set environment variables
os.environ['PYB_CONFIG_FILE'] = str(config_file)

# Import startup module
import pybliometrics.utils.startup as startup

# Read the config
config = configparser.ConfigParser()
config.read(config_file)

# Set the CONFIG global variable
startup.CONFIG = config

print("✓ CONFIG variable initialized\n")

# Create all necessary subdirectories including ENHANCED views
scopus_dir = Path.home() / '.pybliometrics' / 'Scopus'

subdirs = [
    'abstract_retrieval/STANDARD',
    'abstract_retrieval/COMPLETE',
    'abstract_retrieval/FULL',
    'abstract_retrieval/REF',
    'author_retrieval/STANDARD',
    'author_retrieval/COMPLETE', 
    'author_retrieval/ENHANCED',  # This was missing!
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

print("Creating directory structure...")
for subdir in subdirs:
    (scopus_dir / subdir).mkdir(parents=True, exist_ok=True)

print("✓ All directories created\n")

# Now import and test
from pybliometrics.scopus import AuthorRetrieval

print("Testing Pybliometrics...\n")

try:
    # Use refresh=True to fetch fresh data
    au = AuthorRetrieval("7004212771", refresh=True)
    
    print("="*60)
    print("✓✓✓ SUCCESS! Pybliometrics is working! ✓✓✓")
    print("="*60)
    print(f"\nAuthor: {au.given_name} {au.surname}")
    print(f"Affiliation: {au.affiliation_current}")
    print(f"Documents: {au.document_count}")
    print(f"Citations: {au.citation_count}")
    print(f"h-index: {au.h_index}")
    print("\n" + "="*60)
    print("🎉🎉🎉 Pybliometrics is fully configured! 🎉🎉🎉")
    print("="*60)
    
except Exception as e:
    print(f"Error: {e}\n")
    
    error_str = str(e)
    if "401" in error_str or "Unauthorized" in error_str:
        print("→ Authentication error")
        print("\n📋 Checklist:")
        print("  ☐ Connected to university VPN?")
        print("  ☐ API key valid? Check: https://dev.elsevier.com/")
        print("  ☐ Institution has Scopus access?")
    elif "404" in error_str:
        print("→ Author ID not found")
    else:
        print("→ Unexpected error:")
        import traceback
        traceback.print_exc()