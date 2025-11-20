"""
AUTHOR PROFILE ANALYSIS SCRIPT
========================================

This script demonstrates how to:
1. Retrieve author profiles from Scopus
2. Extract key metrics (h-index, citations, etc.)
3. Get co-author information
4. Export author data

Modify this script for your research needs.
"""


import os, sys
current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.dirname(os.path.dirname(current_dir))

if project_root not in sys.path:
    sys.path.insert(0, project_root)


from pybliometrics_conf.config.pyblio_config import AuthorRetrieval
import pandas as pd
from pathlib import Path



def analyze_author(author_id, author_name="Unknown"):
    """
    Analyze a single author's profile
    
    Parameters:
    -----------
    author_id : str
        Scopus author ID
    author_name : str
        Author's name (for reference)
    
    Returns:
    --------
    dict : Dictionary containing author metrics
    """
    
    print(f"\nRetrieving profile for: {author_name} (ID: {author_id})")
    
    try:
        # Retrieve author from Scopus
        au = AuthorRetrieval(author_id)
        
        # Extract key information
        author_data = {
            'Scopus_ID': author_id,
            'First_Name': au.given_name,
            'Last_Name': au.surname,
            'Affiliation': str(au.affiliation_current),
            'Documents': au.document_count,
            'Citations': au.citation_count,
            'h_index': au.h_index,
        }
        
        # Get co-authors
        coauthors = au.get_coauthors()
        author_data['Number_of_Coauthors'] = len(coauthors)
        
        print(f"✓ Profile retrieved successfully")
        print(f"  Name: {au.given_name} {au.surname}")
        print(f"  Documents: {au.document_count}")
        print(f"  Citations: {au.citation_count}")
        print(f"  h-index: {au.h_index}")
        print(f"  Co-authors: {len(coauthors)}")
        
        return author_data
        
    except Exception as e:
        print(f"✗ Error retrieving author: {e}")
        return None


def analyze_multiple_authors(author_list):
    """
    Analyze multiple authors and create comparison table
    
    Parameters:
    -----------
    author_list : list of tuples
        List of (author_id, author_name) tuples
    
    Returns:
    --------
    pd.DataFrame : DataFrame containing all authors' metrics
    """
    
    print("\n" + "="*70)
    print("ANALYZING MULTIPLE AUTHORS")
    print("="*70)
    
    results = []
    
    for author_id, author_name in author_list:
        author_data = analyze_author(author_id, author_name)
        if author_data:
            results.append(author_data)
    
    # Create DataFrame
    df = pd.DataFrame(results)
    
    return df


def main():
    """
    Main execution: Analyze example authors
    """
    
    print("\n" + "="*70)
    print("AUTHOR PROFILE ANALYSIS")
    print("="*70)
    
    # Example authors (modify these for your research)
    # Format: (scopus_id, name)
    authors = [
        ("7004212771", "John R. Kitchin"),
        # Add more authors here
    ]
    
    # Analyze authors
    df = analyze_multiple_authors(authors)
    
    # Save results
    output_dir = Path("data/results")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    csv_file = output_dir / "author_profiles.csv"
    df.to_csv(csv_file, index=False)
    
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    print("\n", df.to_string(index=False))
    print(f"\n✓ Results saved to: {csv_file}")


if __name__ == "__main__":
    main()
