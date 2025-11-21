"""
TEST INSTALLAZIONE SERPAPI (GOOGLE SCHOLAR)
===========================================
Verifica la connessione a SerpApi e il recupero dati.
"""

import os, sys
from serpapi import GoogleSearch
import pandas as pd
from pathlib import Path  

# --- CONFIGURAZIONE ---
SERPAPI_KEY = "236558ca189bbddb6b49fe6a9b5dce0050e1938592e20834725bd777c4f3b3f5"

def test_author_profile():
    """
    Test 1: Recupero Profilo Autore e restituzione DataFrame pubblicazioni
    """
    print("\n" + "="*70)
    print("TEST 1: RECUPERO PROFILO AUTORE (SerpApi)")
    print("="*70)
    
    # ID di Ian Goodfellow su Scholar
    test_id = "iYzcrHkAAAAJ" 
    print(f"Tentativo di recupero ID: {test_id}...")

    params = {
        "engine": "google_scholar_author",
        "author_id": test_id,
        "api_key": SERPAPI_KEY,
        "num": 100,        # Aggiunto: Scarica fino a 100 articoli
        "sort": "pubdate"  # Opzionale: ordina per data
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        
        if "error" in results:
            print(f"\n✗ ERRORE API: {results['error']}")
            return None

        author = results.get("author", {})
        
        print("\n✓ SUCCESSO! Autore trovato!\n")
        print(f"  Nome: {author.get('name')}")
        print(f"  Affiliazione: {author.get('affiliations')}")
        print(f"  Interessi: {author.get('interests')}")
        print(f"  Citazioni Totali: {results.get('cited_by', {}).get('table', [{}])[0].get('citations', {}).get('all')}")
        
        # Verifica se ci sono articoli e crea il DataFrame
        articles = results.get("articles", [])
        print(f"  Articoli recuperati: {len(articles)}")
        
        if articles:
            print(f"  Primo articolo: {articles[0].get('title')}")
            
            # Creiamo una lista pulita di dizionari per il CSV
            clean_data = []
            for art in articles:
                clean_data.append({
                    "title": art.get("title"),
                    "link": art.get("link"),
                    "authors": art.get("authors"),
                    "publication": art.get("publication"),
                    "year": art.get("year"),
                    "cited_by": art.get("cited_by", {}).get("value") if isinstance(art.get("cited_by"), dict) else art.get("cited_by"),
                    "citation_id": art.get("citation_id")
                })
            
            # Restituisce il DataFrame invece di True
            return pd.DataFrame(clean_data)
        
        return pd.DataFrame() # Restituisce DF vuoto se non ci sono articoli

    except Exception as e:
        print(f"\n✗ FALLITO: {e}")
        return None

def test_general_search():
    """
    Test 2: Ricerca generica (per verificare che l'engine funzioni)
    """
    print("\n" + "="*70)
    print("TEST 2: RICERCA GENERICA")
    print("="*70)
    
    params = {
        "engine": "google_scholar",
        "q": "Deep Learning",
        "api_key": SERPAPI_KEY,
        "num": 1
    }
    
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        organic = results.get("organic_results", [])
        
        if organic:
            print(f"\n✓ SUCCESSO! Ricerca funzionante.")
            print(f"  Titolo trovato: {organic[0].get('title')}")
            return True
        else:
            print("\n✗ NESSUN RISULTATO.")
            return False
            
    except Exception as e:
        print(f"\n✗ FALLITO: {e}")
        return False

if __name__ == "__main__":
    if SERPAPI_KEY == "INSERISCI_LA_TUA_API_KEY_QUI":
        print("ATTENZIONE: Devi inserire la tua SERPAPI_KEY nello script prima di eseguire.")
    else:
        # Esegue il test 1 e cattura il DataFrame
        df_author_pubs = test_author_profile()
        
        # Esegue il test 2 (solo verifica booleana)
        t2_passed = test_general_search()

        # Salvataggio CSV se il DataFrame esiste e non è vuoto
        if df_author_pubs is not None and not df_author_pubs.empty:
            output_dir = Path("tests/data")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            csv_file = output_dir / "author_search_scholarcsv"
            df_author_pubs.to_csv(csv_file, index=False)
            print(f"\n CSV Salvato in: {csv_file} ({len(df_author_pubs)} righe)")

        if df_author_pubs is not None and t2_passed:
            print("\n✓✓✓ TUTTI I TEST SERPAPI SUPERATI! ✓✓✓")