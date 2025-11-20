import os
from pathlib import Path
import pandas as pd

CACHE_DIR = Path("data/cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def cache_filename(name, surname, scopus_id):
    """
    Genera il nome file univoco della cache per autore.
    Esempio: Giovanni_Stea_7003668816.csv
    """
    safe_name = name.replace(" ", "_").replace(".", "")
    safe_surname = surname.replace(" ", "_").replace(".", "")
    return CACHE_DIR / f"{safe_name}_{safe_surname}_{scopus_id}.csv"


def is_cached(name, surname, scopus_id):
    """Controlla se l'autore è già presente in cache."""
    return cache_filename(name, surname, scopus_id).exists()


def load_from_cache(name, surname, scopus_id):
    """Carica i dati cache dal CSV se esistono."""
    file = cache_filename(name, surname, scopus_id)
    if file.exists():
        print(f"⚡ Cache trovata per {name} {surname} (Scopus {scopus_id})")
        return pd.read_csv(file)
    return None


def save_to_cache(df, name, surname, scopus_id):
    """Salva un nuovo file in cache."""
    file = cache_filename(name, surname, scopus_id)
    df.to_csv(file, index=False)
    print(f"💾 Cache aggiornata: {file}")


def clear_temp_data(name):
    """
    Rimuove i file temporanei (Scopus e Scholar) dopo il merge.
    Serve per evitare duplicati e alleggerire la memoria.
    """
    base = Path("data/raw")
    for src in ["Scopus", "Scholar"]:
        temp = base / f"{name.replace(' ', '_')}_{src}.csv"
        if temp.exists():
            temp.unlink()
            print(f"🗑️  Rimosso file temporaneo: {temp}")
