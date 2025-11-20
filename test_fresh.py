# test_fresh.py - Run in a COMPLETELY FRESH Python session
import os
from pathlib import Path

# MUST set this BEFORE any pybliometrics imports
config_file = Path.home() / '.pybliometrics' / 'config.ini'
os.environ['PYB_CONFIG_FILE'] = str(config_file)

print(f"Config file: {config_file}")
print(f"Exists: {config_file.exists()}\n")

# Verify config content
if config_file.exists():
    with open(config_file, 'r') as f:
        content = f.read()
        print("Config contains API key:", "ea3e460a194a1ad1feacfe085a65c189" in content)
        print("Config contains InstToken:", "f4a5b71fc4063e9f0b60575bb01fe426" in content)
        print()

# Now import
print("Importing pybliometrics...")
from pybliometrics.scopus import AuthorRetrieval

# Test
print("Testing AuthorRetrieval...\n")
try:
    au = AuthorRetrieval("7004212771")
    print("="*60)
    print("✓✓✓ SUCCESS! ✓✓✓")
    print("="*60)
    print(f"Name: {au.given_name} {au.surname}")
    print(f"Documents: {au.document_count}")
    print(f"Citations: {au.citation_count}")
    print(f"h-index: {au.h_index}")
except Exception as e:
    print("="*60)
    print("✗ Error:")
    print("="*60)
    print(f"{e}\n")
    
    # Provide specific troubleshooting
    error_str = str(e).lower()
    if "401" in error_str or "unauthorized" in error_str:
        print("→ Authentication issue. Check:")
        print("  1. Connected to university VPN?")
        print("  2. API key is valid at https://dev.elsevier.com/")
    elif "404" in error_str:
        print("→ Author not found. Try author ID: 7004212771")
    elif "config" in error_str:
        print("→ Config still not found. Try running:")
        print("     import pybliometrics")
        print("     pybliometrics.scopus.utils.create_config()")
    else:
        print("→ Unexpected error")
        import traceback
        traceback.print_exc()
