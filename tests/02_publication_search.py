"""
SCRIPT DI RICERCA E ANALISI PUBBLICAZIONI
========================================

Questo script dimostra come:
1. Cercare pubblicazioni tramite parole chiave
2. Filtrare per anno, area tematica, ecc.
3. Analizzare i trend delle pubblicazioni
4. Esportare i risultati in CSV

"""

import os, sys
from pathlib import Path
from datetime import datetime
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import dal tuo file di configurazione
from src.pybliometrics_conf.config.pyblio_config import ScopusSearch


def search_publications(query, max_results=1000):
    """
    Cerca pubblicazioni su Scopus
    
    Parametri:
    -----------
    query : str
        Query di ricerca Scopus (es. "TITLE-ABS-KEY(machine learning)")
    max_results : int
        Numero massimo di risultati da recuperare
    
    Ritorna:
    --------
    pd.DataFrame : DataFrame con i risultati della ricerca
    """
    
    print(f"\nRicerca pubblicazioni in corso...")
    print(f"Query: {query}")
    print(f"Max risultati: {max_results}")
    
    try:
        # Esegui la ricerca 
        s = ScopusSearch(query, download=True, count=max_results)
        
        total_results = s.get_results_size()
        print(f"\n✓ Trovati {total_results} risultati totali")

        if not s.results:
             print("⚠ Nessun dato scaricato. Forse il download è fallito o la cache è vuota.")
             return pd.DataFrame()
        
        # Estrai i dati dai risultati
        results_list = []
        for doc in s.results:
            results_list.append({
                'Title': doc.title,
                'Authors': doc.author_names,
                'Publication': doc.publicationName,
                'Year': doc.coverDate[:4] if doc.coverDate else 'N/A',
                'Citations': doc.citedby_count,
                'DOI': doc.doi,
                'EID': doc.eid
            })
        
        df = pd.DataFrame(results_list)
        
        print(f"Recuperati: {len(df)} risultati")
        
        return df
        
    except Exception as e:
        print(f"✗ Errore durante la ricerca: {e}")
        return pd.DataFrame()


def analyze_trends(df):
    """
    Analizza i trend delle pubblicazioni
    
    Parametri:
    -----------
    df : pd.DataFrame
        DataFrame con le pubblicazioni
    
    Ritorna:
    --------
    dict : Dizionario con statistiche sui trend
    """
    
    print("\n" + "="*70)
    print("TREND DELLE PUBBLICAZIONI")
    print("="*70)
    
    # Pubblicazioni per anno
    yearly = df['Year'].value_counts().sort_index()
    
    print(f"\nPubblicazioni per anno:")
    for year, count in yearly.items():
        print(f"  {year}: {count} pubblicazioni")
    
    # Top journal (riviste)
    print(f"\nTop 10 riviste:")
    top_journals = df['Publication'].value_counts().head(10)
    for journal, count in top_journals.items():
        print(f"  {journal}: {count} pubblicazioni")
    
    # Statistiche citazioni
    print(f"\nStatistiche citazioni:")
    print(f"  Totale citazioni: {df['Citations'].sum()}")
    print(f"  Media citazioni: {df['Citations'].mean():.1f}")
    print(f"  Più citato: {df['Citations'].max()}")
    
    # Articoli più citati
    print(f"\nTop 5 articoli più citati:")
    top_cited = df.nlargest(5, 'Citations')
    for idx, (i, row) in enumerate(top_cited.iterrows(), 1):
        print(f"  {idx}. {str(row['Title'])[:60]}...")
        print(f"     Citazioni: {row['Citations']}")


def main():
    """
    Esecuzione principale: Cerca e analizza pubblicazioni
    """
    
    print("\n" + "="*70)
    print("RICERCA E ANALISI PUBBLICAZIONI")
    print("="*70)
    
    query = "TITLE-ABS-KEY(machine learning) AND TITLE-ABS-KEY(bibliometrics) AND PUBYEAR > 2022"
    

    print(f"Tentativo di scaricare max 20 risultati...")
    df = search_publications(query, max_results=20)
    
    if df.empty:
        print("Nessun risultato trovato o errore nel download!")
        return
    
    # Analizza i trend
    analyze_trends(df)
    
    # Salva i risultati
    output_dir = Path("data/results")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = output_dir / f"pubblicazioni_{timestamp}.csv"
    df.to_csv(csv_file, index=False)
    
    print(f"\n✓ Risultati salvati in: {csv_file}")
    print(f"\n✓ Record totali: {len(df)}")

if __name__ == "__main__":
    main()