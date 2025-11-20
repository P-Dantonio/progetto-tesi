"""
INSTALLATION TEST SCRIPT
========================================

This script tests that Pybliometrics is properly installed and configured.
Run this after running setup_pybliometrics.py

It performs two tests:
1. Author Retrieval - Fetches author profile data
2. Publication Search - Searches for publications

If both tests pass, your installation is complete!
"""
import os, sys
current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.dirname(os.path.dirname(current_dir))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import from our configuration module
from pybliometrics_conf.config.pyblio_config import AuthorRetrieval, ScopusSearch

def test_author_retrieval():
    """
    Test 1: Retrieve author profile
    Uses a real Scopus author ID to test the connection
    """
    print("\n" + "="*70)
    print("TEST 1: AUTHOR RETRIEVAL")
    print("="*70)
    print("Attempting to retrieve author profile...")
    
    try:
        # Retrieve author with ID 7004212771 (John R. Kitchin from CMU)
        au = AuthorRetrieval("7004212771")
        
        print("\n✓ SUCCESS! Author retrieval works!\n")
        print(f"  Name: {au.given_name} {au.surname}")
        print(f"  Affiliation: {au.affiliation_current}")
        print(f"  Documents: {au.document_count}")
        print(f"  Citations: {au.citation_count}")
        print(f"  h-index: {au.h_index}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ FAILED: {e}")
        print("\nTroubleshooting:")
        print("  1. Are you connected to your university VPN?")
        print("  2. Is your API key valid? Check https://dev.elsevier.com/")
        print("  3. Does your institution have Scopus access?")
        return False


def test_publication_search():
    """
    Test 2: Search for publications
    Performs a simple keyword search to test search functionality
    """
    print("\n" + "="*70)
    print("TEST 2: PUBLICATION SEARCH")
    print("="*70)
    print("Searching for publications on 'machine learning'...")
    
    try:
        # Search for publications with title containing "machine learning"
        query = "TITLE(machine learning)"
        results = ScopusSearch(query, download=False)
        
        print(f"\n✓ SUCCESS! Search works!\n")
        print(f"  Found {results.get_results_size()} total results")
        
        # Show first 3 results
        if results.results:
            print(f"\n  First 3 results:")
            for i, doc in enumerate(results.results[:3], 1):
                print(f"\n    {i}. {doc.title}")
                print(f"       Authors: {doc.author_names}")
                print(f"       Year: {doc.coverDate}")
                print(f"       Citations: {doc.citedby_count}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ FAILED: {e}")
        print("\nTroubleshooting:")
        print("  1. Check VPN connection")
        print("  2. Verify API key")
        print("  3. Check internet connection")
        return False


def main():
    """
    Run all tests and report results
    """
    print("\n" + "="*70)
    print("PYBLIOMETRICS INSTALLATION TEST")
    print("="*70)
    print("This script tests your Pybliometrics installation")
    
    # Run tests
    test1_passed = test_author_retrieval()
    test2_passed = test_publication_search()
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    if test1_passed and test2_passed:
        print("\n✓✓✓ ALL TESTS PASSED! ✓✓✓")
        print("\nYour Pybliometrics installation is complete and working!")
        print("You can now use Pybliometrics in your scripts.")
        print("\nNext steps:")
        print("  1. Review other scripts in the 'scripts/' folder")
        print("  2. Modify them for your research")
        print("  3. Start analyzing Scopus data!")
    else:
        print("\n✗ SOME TESTS FAILED")
        print("Please check the troubleshooting information above.")
        print("If problems persist, verify your configuration and VPN access.")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
