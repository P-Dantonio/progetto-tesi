"""
SCRIPT DI ANALISI PROFILO AUTORE
========================================

Questo script dimostra come:
1. Recuperare profili autore da Scopus
2. Estrarre metriche chiave (h-index, citazioni, ecc.)
3. Ottenere informazioni sui co-autori
4. Esportare i dati dell'autore

"""

import os, sys
from pathlib import Path
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

if project_root not in sys.path:
    sys.path.insert(0, project_root)


from src.pybliometrics_conf.config.pyblio_config import AuthorRetrieval


def analyze_author(author_id, author_name="Sconosciuto"):
    """
    Analizza il profilo di un singolo autore
    
    Parametri:
    -----------
    author_id : str
        ID autore Scopus
    author_name : str
        Nome dell'autore (per riferimento)
    
    Ritorna:
    --------
    dict : Dizionario contenente le metriche dell'autore
    """
    
    print(f"\nRecupero profilo per: {author_name} (ID: {author_id})")
    
    try:
        # Recupera l'autore da Scopus
        au = AuthorRetrieval(author_id)
        
        # Estrae informazioni chiave
        author_data = {
            'Scopus_ID': author_id,
            'Nome': au.given_name,
            'Cognome': au.surname,
            'Affiliazione': str(au.affiliation_current),
            'Documenti': au.document_count,
            'Citazioni': au.citation_count,
            'h_index': au.h_index,
        }
        
        # Ottiene i co-autori
        coauthors = au.get_coauthors()
        author_data['Numero_Coautori'] = len(coauthors)
        
        print(f"✓ Profilo recuperato con successo")
        print(f"  Nome: {au.given_name} {au.surname}")
        print(f"  Documenti: {au.document_count}")
        print(f"  Citazioni: {au.citation_count}")
        print(f"  h-index: {au.h_index}")
        print(f"  Co-autori: {len(coauthors)}")
        
        return author_data
        
    except Exception as e:
        print(f"✗ Errore nel recupero dell'autore: {e}")
        return None


def analyze_multiple_authors(author_list):
    """
    Analizza più autori e crea una tabella di confronto
    
    Parametri:
    -----------
    author_list : list of tuples
        Lista di tuple (author_id, author_name)
    
    Ritorna:
    --------
    pd.DataFrame : DataFrame contenente le metriche di tutti gli autori
    """
    
    print("\n" + "="*70)
    print("ANALISI DI PIÙ AUTORI")
    print("="*70)
    
    results = []
    
    for author_id, author_name in author_list:
        author_data = analyze_author(author_id, author_name)
        if author_data:
            results.append(author_data)
    
    # Crea il DataFrame
    df = pd.DataFrame(results)
    
    return df


def main():
    """
    Esecuzione principale: Analizza autori di esempio
    """
    
    print("\n" + "="*70)
    print("ANALISI PROFILO AUTORE")
    print("="*70)
    
    # Autori di esempio (modifica questi per la tua ricerca)
    # Formato: (scopus_id, nome)
    authors = [
        ("7004212771", "John R. Kitchin"),
        # Aggiungi altri autori qui
    ]
    
    # Analizza gli autori
    df = analyze_multiple_authors(authors)
    
    # Salva i risultati
    output_dir = Path("data/results")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    csv_file = output_dir / "profili_autori.csv"
    df.to_csv(csv_file, index=False)
    
    print("\n" + "="*70)
    print("RISULTATI")
    print("="*70)
    print("\n", df.to_string(index=False))
    print(f"\n✓ Risultati salvati in: {csv_file}")


if __name__ == "__main__":
    main()