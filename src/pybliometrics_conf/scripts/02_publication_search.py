"""
PUBLICATION SEARCH AND ANALYSIS SCRIPT
========================================

This script demonstrates how to:
1. Search for publications by keywords
2. Filter by year, subject area, etc.
3. Analyze publication trends
4. Export results to CSV

Modify this script for your research queries.
"""

from config.pyblio_config import ScopusSearch
import pandas as pd
from pathlib import Path
from datetime import datetime

def search_publications(query, max_results=1000):
    """
    Search for publications in Scopus
    
    Parameters:
    -----------
    query : str
        Scopus search query (e.g., "TITLE-ABS-KEY(machine learning)")
    max_results : int
        Maximum results to retrieve
    
    Returns:
    --------
    pd.DataFrame : DataFrame with search results
    """
    
    print(f"\nSearching for publications...")
    print(f"Query: {query}")
    print(f"Max results: {max_results}")
    
    try:
        # Perform search
        s = ScopusSearch(query, download=False)
        
        total_results = s.get_results_size()
        print(f"\n✓ Found {total_results} total results")
        
        # Extract data from results
        results_list = []
        for doc in s.results:
            results_list.append({
                'Title': doc.title,
                'Authors': doc.author_names,
                'Publication': doc.publicationName,
                'Year': doc.coverDate[:4] if doc.coverDate else 'N/A',
                'Citations': doc.citedby_count,
                'DOI': doc.doi,
                'URL': doc.url
            })
        
        df = pd.DataFrame(results_list)
        
        print(f"Retrieved: {len(df)} results")
        
        return df
        
    except Exception as e:
        print(f"✗ Error during search: {e}")
        return pd.DataFrame()


def analyze_trends(df):
    """
    Analyze publication trends
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with publications
    
    Returns:
    --------
    dict : Dictionary with trend statistics
    """
    
    print("\n" + "="*70)
    print("PUBLICATION TRENDS")
    print("="*70)
    
    # Publications by year
    yearly = df['Year'].value_counts().sort_index()
    
    print(f"\nPublications by year:")
    for year, count in yearly.items():
        print(f"  {year}: {count} publications")
    
    # Top journals
    print(f"\nTop 10 journals:")
    top_journals = df['Publication'].value_counts().head(10)
    for journal, count in top_journals.items():
        print(f"  {journal}: {count} publications")
    
    # Citation statistics
    print(f"\nCitation statistics:")
    print(f"  Total citations: {df['Citations'].sum()}")
    print(f"  Average citations: {df['Citations'].mean():.1f}")
    print(f"  Most cited: {df['Citations'].max()}")
    
    # Most cited papers
    print(f"\nTop 5 most cited papers:")
    top_cited = df.nlargest(5, 'Citations')
    for idx, (i, row) in enumerate(top_cited.iterrows(), 1):
        print(f"  {idx}. {row['Title'][:60]}...")
        print(f"     Citations: {row['Citations']}")


def main():
    """
    Main execution: Search and analyze publications
    """
    
    print("\n" + "="*70)
    print("PUBLICATION SEARCH AND ANALYSIS")
    print("="*70)
    
    # Define search query (modify for your research)
    query = "TITLE-ABS-KEY(machine learning) AND PUBYEAR > 2020"
    
    # Search publications
    df = search_publications(query)
    
    if df.empty:
        print("No results found!")
        return
    
    # Analyze trends
    analyze_trends(df)
    
    # Save results
    output_dir = Path("data/results")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = output_dir / f"publications_{timestamp}.csv"
    df.to_csv(csv_file, index=False)
    
    print(f"\n✓ Results saved to: {csv_file}")
    print(f"\n✓ Total records: {len(df)}")


if __name__ == "__main__":
    main()
