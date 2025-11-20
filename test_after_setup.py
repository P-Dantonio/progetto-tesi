# test_after_setup.py - Run in NEW session after final_setup.py
from pybliometrics.scopus import AuthorRetrieval

print("Testing Pybliometrics...\n")

try:
    # Test 1: Retrieve author
    print("Test 1: Retrieving author 7004212771...")
    au = AuthorRetrieval("7004212771")
    
    print("\n" + "="*60)
    print("✓✓✓ SUCCESS! Pybliometrics is working! ✓✓✓")
    print("="*60)
    print(f"\nAuthor: {au.given_name} {au.surname}")
    print(f"Affiliation: {au.affiliation_current}")
    print(f"Documents: {au.document_count}")
    print(f"Citations: {au.citation_count}")
    print(f"h-index: {au.h_index}")
    
    # Test 2: Basic search
    print("\n" + "="*60)
    print("Test 2: Searching for publications...")
    print("="*60)
    
    from pybliometrics.scopus import ScopusSearch
    
    query = "TITLE(machine learning) AND PUBYEAR = 2024"
    s = ScopusSearch(query, download=False)
    print(f"\nFound {s.get_results_size()} results for: {query}")
    
    print("\n" + "="*60)
    print("All tests passed! You can now use Pybliometrics!")
    print("="*60)
    
except Exception as e:
    print("\n" + "="*60)
    print("✗ Error occurred:")
    print("="*60)
    print(f"{e}\n")
    
    error_str = str(e).lower()
    
    if "401" in error_str or "unauthorized" in error_str:
        print("→ Authentication Error")
        print("\nPossible solutions:")
        print("1. Make sure you're connected to your university VPN")
        print("2. Verify your API key at: https://dev.elsevier.com/")
        print("3. Check that your institution has Scopus access")
        print("4. Try generating a new API key")
        
    elif "config" in error_str:
        print("→ Configuration Error")
        print("\nThe config file still isn't being found.")
        print("Try this workaround:")
        print("""
import os
from pathlib import Path

config_file = Path.home() / '.pybliometrics' / 'config.ini'
os.environ['PYB_CONFIG_FILE'] = str(config_file)

from pybliometrics.scopus import AuthorRetrieval
au = AuthorRetrieval("7004212771")
        """)
        
    else:
        print("→ Unexpected Error")
        print("\nFull traceback:")
        import traceback
        traceback.print_exc()
