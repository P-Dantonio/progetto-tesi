#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from serpapi import GoogleSearch
import pandas as pd
import os

# La tua API Key
SERPAPI_KEY = "236558ca189bbddb6b49fe6a9b5dce0050e1938592e20834725bd777c4f3b3f5"

def fetch_scholar_by_id(author_id: str, output_name: str | None = None, max_retries: int = 3):
   
    print(f"\n Ricerca Author ID: {author_id}")
    
    all_articles = []
    start = 0
    page_size = 100 # SerpApi permette fino a 100 risultati per pagina
    author_name = "Unknown_Author"
    
    while True:
        print(f" Scarico pagina risultati {start} - {start + page_size}...")
        
        params = {
            "api_key": SERPAPI_KEY,
            "engine": "google_scholar_author",
            "author_id": author_id,
            "start": start,
            "num": page_size,
            "sort": "pubdate" # Ordina per data (opzionale)
        }

        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            
            # Gestione errori API
            if "error" in results:
                print(f"❌ Errore SerpApi: {results['error']}")
                break

            # Recupera il nome autore (solo al primo giro)
            if start == 0 and "author" in results:
                author_name = results["author"].get("name", "Unknown_Author")
                print(f"✅ Autore Trovato: {author_name}")

            # Estrazione articoli
            if "articles" in results:
                articles = results["articles"]
                if not articles:
                    print("   🏁 Nessun altro articolo trovato.")
                    break 
                
                for art in articles:
                    # Mappatura dei dati nel formato che il tuo merge si aspetta
                    row = {
                        "title": art.get("title", ""),
                        "year": art.get("year", ""),
                        # SerpApi restituisce le citazioni dentro 'cited_by' -> 'value'
                        "citations_scholar": art.get("cited_by", {}).get("value", 0),
                        "venue": art.get("publication", ""), # Journal/Conference
                        "link": art.get("link", ""),
                        "source": "Scholar"
                    }
                    all_articles.append(row)
            else:
                # Se non c'è la chiave 'articles', abbiamo finito
                break 

            # Gestione Paginazione 
            if "serpapi_pagination" in results and "next" in results["serpapi_pagination"]:
                start += page_size 
            else:
                print("🏁 Fine delle pagine disponibili.")
                break
            
        except Exception as e:
            print(f"❌ Eccezione durante la richiesta SerpApi: {e}")
            break

    # --- SALVATAGGIO ---
    if not all_articles:
        print("⚠️ Nessun articolo trovato o errore nel download.")
        return None

    print(f"📚 Totale scaricati: {len(all_articles)} articoli.")
    
    df = pd.DataFrame(all_articles)
    
    # Assicurati che la cartella esista
    os.makedirs("data/raw", exist_ok=True)

    # Determina il nome del file
    if output_name:
        base = output_name
    else:
        base = author_name.replace(" ", "_")

    filename = f"data/raw/{base}_Scholar.csv"
    df.to_csv(filename, index=False)
    print(f"\n💾 File salvato: {filename}")
    return filename