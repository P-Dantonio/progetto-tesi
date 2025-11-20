"""
DATA ANALYSIS AND VISUALIZATION SCRIPT
========================================

This script demonstrates how to:
1. Load saved publication data
2. Perform statistical analysis
3. Create visualizations
4. Generate reports

This script works with data exported from other scripts.
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def load_results(filename):
    """
    Load previously saved search results
    
    Parameters:
    -----------
    filename : str
        CSV filename in data/results/
    
    Returns:
    --------
    pd.DataFrame : Loaded data
    """
    
    filepath = Path("data/results") / filename
    
    if not filepath.exists():
        print(f"File not found: {filepath}")
        return pd.DataFrame()
    
    df = pd.read_csv(filepath)
    print(f"✓ Loaded {len(df)} records from {filename}")
    
    return df


def analyze_citation_distribution(df):
    """
    Analyze how citations are distributed across papers
    """
    
    print("\n" + "="*70)
    print("CITATION DISTRIBUTION ANALYSIS")
    print("="*70)
    
    citations = df['Citations'].astype(int)
    
    print(f"\nStatistics:")
    print(f"  Mean: {citations.mean():.1f}")
    print(f"  Median: {citations.median():.1f}")
    print(f"  Std Dev: {citations.std():.1f}")
    print(f"  Min: {citations.min()}")
    print(f"  Max: {citations.max()}")
    
    # Create histogram
    plt.figure(figsize=(10, 6))
    plt.hist(citations, bins=30, edgecolor='black', color='skyblue')
    plt.xlabel('Number of Citations')
    plt.ylabel('Number of Papers')
    plt.title('Citation Distribution')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    output_path = Path("data/results") / "citation_distribution.png"
    plt.savefig(output_path, dpi=300)
    print(f"\n✓ Visualization saved to: {output_path}")
    plt.close()


def yearly_trend_analysis(df):
    """
    Analyze publications trends over years
    """
    
    print("\n" + "="*70)
    print("YEARLY TREND ANALYSIS")
    print("="*70)
    
    # Convert Year to int
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    
    # Group by year
    yearly = df.groupby('Year').agg({
        'Title': 'count',
        'Citations': 'sum'
    }).rename(columns={'Title': 'Publications', 'Citations': 'Total_Citations'})
    
    print("\n", yearly)
    
    # Plot trends
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Publications per year
    yearly['Publications'].plot(ax=ax1, marker='o', color='green', linewidth=2)
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Number of Publications')
    ax1.set_title('Publications per Year')
    ax1.grid(True, alpha=0.3)
    
    # Citations per year
    yearly['Total_Citations'].plot(ax=ax2, marker='o', color='red', linewidth=2)
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Total Citations')
    ax2.set_title('Total Citations per Year')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    output_path = Path("data/results") / "yearly_trends.png"
    plt.savefig(output_path, dpi=300)
    print(f"\n✓ Visualization saved to: {output_path}")
    plt.close()


def journal_analysis(df):
    """
    Analyze which journals publish most papers
    """
    
    print("\n" + "="*70)
    print("JOURNAL ANALYSIS")
    print("="*70)
    
    journal_counts = df['Publication'].value_counts().head(15)
    
    print(f"\nTop 15 journals publishing on this topic:")
    print(journal_counts)
    
    # Create bar chart
    plt.figure(figsize=(12, 6))
    journal_counts.plot(kind='barh', color='orange')
    plt.xlabel('Number of Publications')
    plt.ylabel('Journal')
    plt.title('Top Journals')
    plt.tight_layout()
    
    output_path = Path("data/results") / "top_journals.png"
    plt.savefig(output_path, dpi=300)
    print(f"\n✓ Visualization saved to: {output_path}")
    plt.close()


def main():
    """
    Main execution: Analyze previously saved data
    """
    
    print("\n" + "="*70)
    print("DATA ANALYSIS AND VISUALIZATION")
    print("="*70)
    
    # List available CSV files
    results_dir = Path("data/results")
    csv_files = list(results_dir.glob("*.csv"))
    
    if not csv_files:
        print("\nNo CSV files found in data/results/")
        print("Run 02_publication_search.py first to generate data.")
        return
    
    print(f"\nAvailable files:")
    for i, f in enumerate(csv_files, 1):
        print(f"  {i}. {f.name}")
    
    # Load the most recent file
    latest_file = max(csv_files, key=lambda p: p.stat().st_mtime)
    print(f"\nLoading: {latest_file.name}")
    
    df = load_results(latest_file.name)
    
    if df.empty:
        return
    
    # Perform analyses
    analyze_citation_distribution(df)
    yearly_trend_analysis(df)
    journal_analysis(df)
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE!")
    print("="*70)
    print("Visualizations saved to data/results/")


if __name__ == "__main__":
    main()
