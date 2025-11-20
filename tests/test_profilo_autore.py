"""
SCRIPT DI ANALISI PROFILO AUTORE
========================================

Questo script dimostra come:
1. Recuperare i profili autore da Scopus
2. Estrarre metriche chiave (h-index, citazioni, ecc.)
3. Ottenere informazioni sui co-autori
4. Esportare i dati dell'autore

Modifica questo script secondo le tue esigenze di ricerca.
"""

import os, sys
current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.dirname(os.path.dirname(current_dir))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Nota: Assicurati che questo percorso di importazione corrisponda alla tua struttura file
from pyblio_config_test import AuthorRetrieval
import pandas as pd
from pathlib import Path


def analyze_author(author_id, author_name="Unknown"):
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
        
        # Estrai informazioni chiave
        # Nota: Mantengo le chiavi in inglese per le intestazioni del CSV
        author_data = {
            'Scopus_ID': author_id,
            'First_Name': au.given_name,
            'Last_Name': au.surname,
            'Affiliation': str(au.affiliation_current),
            'Documents': au.document_count,
            'Citations': au.citation_count,
            'h_index': au.h_index,
        }
        
        # Ottieni i co-autori
        coauthors = au.get_coauthors()
        author_data['Number_of_Coauthors'] = len(coauthors)
        
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
    
    # Crea DataFrame
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
    # Formato: (id_scopus, nome)
    authors = [
        ("7004212771", "John R. Kitchin"),
        # Aggiungi altri autori qui
    ]
    
    # Analizza autori
    df = analyze_multiple_authors(authors)
    
    # Salva i risultati
    output_dir = Path("tests/data")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    csv_file = output_dir / "author_profiles.csv"
    df.to_csv(csv_file, index=False)
    
    print("\n" + "="*70)
    print("RISULTATI")
    print("="*70)
    print("\n", df.to_string(index=False))
    print(f"\n✓ Risultati salvati in: {csv_file}")


if __name__ == "__main__":
    main()