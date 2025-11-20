import sys
import os
from pathlib import Path



SERPAPI_KEY = "236558ca189bbddb6b49fe6a9b5dce0050e1938592e20834725bd777c4f3b3f5"

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)


try:

    from serpapi import GoogleSearch
except ImportError:
    print(" Errore configurazione. Controlla settings.py e librerie.")
    sys.exit(1)

def controlla_id_scholar(scholar_id):
    print(f"\n [SCHOLAR] Analisi ID: '{scholar_id}'...")

    if not SERPAPI_KEY:
        print(" Manca la SERPAPI_KEY in src/config/settings.py")
        return

    params = {
        "api_key": SERPAPI_KEY,
        "engine": "google_scholar_author", # Motore per vedere il profilo
        "author_id": scholar_id,
        "hl": "it"
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        
        # Controllo errori API
        if "error" in results:
            print(f" Errore API: {results['error']}")
            return

        # Estrazione dati autore
        author = results.get("author", {})
        
        if not author:
            print(" Nessun profilo trovato per questo ID. Forse è errato?")
            return

        # --- STAMPA BEL REPORT ---
        print("\n" + "="*50)
        print(f" PROFILO TROVATO: {author.get('name')}")
        print("="*50)
        
        print(f"  Affiliazione: {author.get('affiliations')}")
        print(f" Sito Web:      {author.get('website', 'N/A')}")
        
        # Interessi (Tags)
        interests = [i.get("title") for i in author.get("interests", [])]
        if interests:
            print(f" Interessi:    {', '.join(interests)}")
        
        # Statistiche Citazionali (Tabella 'Cited by')
        cited_by = author.get("cited_by", {})
        table = cited_by.get("table", [])
        if table:
            print("\n📊 Metriche Scholar:")
            # Cerca le metriche principali nella tabella
            for row in table:
                metric = list(row.keys())[0] # es. "citations", "h_index"
                all_val = row[metric].get("all")
                since_val = row[metric].get("since_2018") 
                print(f"   - {metric.capitalize()}: {all_val} (Dal 2019: {since_val})")
        
        print("\n✅ L'ID è valido e funzionante.")
        print("="*50 + "\n")

    except Exception as e:
        print(f"❌ Errore critico durante il controllo: {e}")

if __name__ == "__main__":
    # Se lanciato senza argomenti, chiede l'ID
    user_id = input("Inserisci l'ID Scholar da controllare (es. 8O2YNDUAAAAJ): ").strip()
    if user_id:
        controlla_id_scholar(user_id)
    else:
        print("ID non inserito.")