# final_setup.py
from pathlib import Path
import os

# Your credentials
API_KEY = "ea3e460a194a1ad1feacfe085a65c189"
INSTTOKEN = "f4a5b71fc4063e9f0b60575bb01fe426"

print("Creating Pybliometrics configuration...\n")

# Config location
config_dir = Path.home() / '.pybliometrics'
config_dir.mkdir(exist_ok=True)

config_file = config_dir / 'config.ini'

# Create the configuration
config_content = f"""[Authentication]
APIKey = {API_KEY}
InstToken = {INSTTOKEN}

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

# Write the config file
with open(config_file, 'w', encoding='utf-8') as f:
    f.write(config_content)

print(f"✓ Config file created at: {config_file}")

# Create all required directories
subdirs = [
    'abstract_retrieval', 'author_retrieval', 'author_search',
    'affiliation_retrieval', 'affiliation_search', 'citation_overview',
    'scopus_search', 'serial_search', 'serial_title', 'plumx',
    'subject_classification'
]

for subdir in subdirs:
    (config_dir / 'Scopus' / subdir).mkdir(parents=True, exist_ok=True)

print(f"✓ All directories created in: {config_dir / 'Scopus'}")

print("\n" + "="*60)
print("Configuration Complete!")
print("="*60)
print(f"\nConfig file location: {config_file}")
print(f"Contains API Key: {API_KEY[:20]}...")
print(f"Contains InstToken: {INSTTOKEN[:20]}...")

print("\n" + "="*60)
print("IMPORTANT: Close this Python session completely!")
print("="*60)
print("\nThen run this test in a NEW Python session:")
print("-"*60)
print("""
from pybliometrics.scopus import AuthorRetrieval

au = AuthorRetrieval("7004212771")
print(f"Success! {au.given_name} {au.surname}")
print(f"Documents: {au.document_count}")
print(f"Citations: {au.citation_count}")
print(f"h-index: {au.h_index}")
""")
print("-"*60)
