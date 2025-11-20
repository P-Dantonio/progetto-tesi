# truly_working_test.py
import os
from pathlib import Path
import sys

# Your config
config_file = Path.home() / '.pybliometrics' / 'config.ini'
print(f"Config file: {config_file}")
print(f"Exists: {config_file.exists()}\n")

# Set environment variables
os.environ['PYB_CONFIG_FILE'] = str(config_file)
os.environ['HOME'] = str(Path.home())

# Import startup module where get_config is actually defined
import pybliometrics.utils.startup as startup
import configparser

# Patch at the source
def patched_get_config():
    """Force config to use our file"""
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def patched_get_keys():
    """Return API keys directly"""
    return ['ea3e460a194a1ad1feacfe085a65c189'], ['f4a5b71fc4063e9f0b60575bb01fe426']

# Apply patches to startup module
startup.get_config = patched_get_config
startup.get_keys = patched_get_keys

# Also patch in the main utils module
import pybliometrics.utils as utils
utils.get_config = patched_get_config
utils.get_keys = patched_get_keys

print("✓ Config functions patched in all locations\n")

# Now import Retrieval classes (they will use our patched functions)
from pybliometrics.scopus import AuthorRetrieval

print("Testing Pybliometrics...\n")

try:
    au = AuthorRetrieval("7004212771", refresh=False)
    
    print("="*60)
    print("✓✓✓ SUCCESS! Pybliometrics is working! ✓✓✓")
    print("="*60)
    print(f"\nAuthor: {au.given_name} {au.surname}")
    print(f"Affiliation: {au.affiliation_current}")
    print(f"Documents: {au.document_count}")
    print(f"Citations: {au.citation_count}")
    print(f"h-index: {au.h_index}")
    print("\n" + "="*60)
    print("Configuration is working perfectly!")
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