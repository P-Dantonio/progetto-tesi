#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
fetcher_scopus.py
=================
Ricerca autore su Scopus (con gestione omonimi) e scarica pubblicazioni.
Ritorna SEMPRE (author_id, selected_name) per il main orchestrator.
Salva i CSV con nome pulito (senza punti).
"""

from pathlib import Path
import os, sys
import pandas as pd
from tqdm import tqdm

current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.dirname(os.path.dirname(current_dir))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from pyblio_config import AuthorSearch, AuthorRetrieval, AbstractRetrieval


# ------------------------------------------------------------
# Utility
# ------------------------------------------------------------
def ensure_pybliometrics_dirs():
    base = Path.home() / ".pybliometrics" / "Scopus"
    subdirs = [
        "author_search",
        "author_retrieval/COMPLETE",
        "author_retrieval/ENHANCED",
        "scopus_search/COMPLETE",
        "abstract_retrieval/COMPLETE",
        "serial_search",
        "serial_title",
    ]
    for sub in subdirs:
        (base / sub).mkdir(parents=True, exist_ok=True)
    print("📁 Pybliometrics directories verified.")


def clean_name_for_filename(name: str) -> str:
    # niente punti, spazi -> underscore, nothing fancy
    return name.replace(".", "").replace("  ", " ").strip().replace(" ", "_")


# ------------------------------------------------------------
# Ricerca autore
# ------------------------------------------------------------
def search_author_by_name(full_name: str):
    """
    Mostra la lista degli autori omonimi e fa scegliere.
    Ritorna (author_id, selected_name) — selected_name è già ripulito per i file.
    """
    print(f"\n Searching Scopus for author: {full_name}")

    try:
        first, last = full_name.strip().split(" ", 1)
    except ValueError:
        print(" Inserisci sia nome che cognome (es. Giovanni Stea).")
        return None, None

    query = f"AUTHLASTNAME({last}) AND AUTHFIRST({first})"
    print(f" Query Scopus: {query}")

    try:
        search = AuthorSearch(query)
    except Exception as e:
        print(f" Errore durante la ricerca Scopus: {e}")
        return None, None

    authors = getattr(search, "authors", []) or []
    if not authors:
        print(" Nessun autore trovato su Scopus.")
        return None, None

    print(f"\n Found {len(authors)} possible matches:\n")
    for i, author in enumerate(authors, start=1):
        aff = getattr(author, "affiliation", "N/A")
        given = getattr(author, "given_name", getattr(author, "givenname", ""))
        surname = getattr(author, "surname", "")
        author_id_raw = getattr(author, "identifier", getattr(author, "author_id", getattr(author, "eid", "N/A")))
        print(f"[{i}] {given} {surname} — {aff} — ID: {author_id_raw}")

    # scelta utente
    while True:
        choice = input("\n Enter the number of the author you want (or 0 to cancel): ").strip()
        if choice.isdigit():
            idx = int(choice)
            if idx == 0:
                print(" Operazione annullata.")
                return None, None
            if 1 <= idx <= len(authors):
                break
        print(" Scelta non valida. Riprova.")

    selected = authors[idx - 1]
    author_id = getattr(selected, "identifier", getattr(selected, "author_id", getattr(selected, "eid", None)))
    # rimuovi prefisso Scopus "9-s2.0-"
    if isinstance(author_id, str) and author_id.startswith("9-s2.0-"):
        author_id = author_id.split("-")[-1]

    given = getattr(selected, "given_name", getattr(selected, "givenname", "")).strip()
    surname = getattr(selected, "surname", "").strip()
    selected_name = f"{given} {surname}"
    selected_name = clean_name_for_filename(selected_name)

    return author_id, selected_name


# ------------------------------------------------------------
# Dettagli + pubblicazioni autore
# ------------------------------------------------------------
def ensure_pybliometrics_dirs():
    base = Path.home() / ".pybliometrics" / "Scopus"
    subdirs = [
        "author_search",
        "author_retrieval/COMPLETE",
        "author_retrieval/ENHANCED",
        "scopus_search/COMPLETE",
        "abstract_retrieval/COMPLETE",
        "serial_search",
        "serial_title",
    ]
    for sub in subdirs:
        (base / sub).mkdir(parents=True, exist_ok=True)
    print("📁 Pybliometrics directories verified.")


def clean_name_for_filename(name: str) -> str:
    return name.replace(".", "").replace("  ", " ").strip().replace(" ", "_")


# ------------------------------------------------------------
# Ricerca autore 
# ------------------------------------------------------------
def search_author_by_name(full_name: str):
    """
    Versione sicura per Web App:
    NON usa input(). Ritorna una lista di dizionari con i candidati.
    """
    print(f"\n Searching Scopus for author: {full_name}")

    try:
        parts = full_name.strip().split()
        if not parts: return []
        last, first = parts[-1], parts[0] if len(parts) > 1 else ""
        
        query = f'AUTHLASTNAME({last}) AND AUTHFIRST({first})' if first else f'AUTHLASTNAME({last})'
        print(f"Query Scopus: {query}")

        s = AuthorSearch(query)
        
        candidates = []
        if s.authors:
            for a in s.authors:
                try:
                    # Estrazione ID
                    raw_id = getattr(a, 'identifier', getattr(a, 'eid', None))
                    if not raw_id: continue
                    
                    clean_id = str(raw_id).split('-')[-1]
                    
                    candidates.append({
                        'id': clean_id,
                        'name': f"{a.surname}, {a.givenname}", # Formato standard
                        'aff': str(a.affiliation) if a.affiliation else "N/A",
                        'documents': getattr(a, 'documents', '0'),
                        'city': str(a.city) if a.city else ""
                    })
                except Exception:
                    continue 
                    
        return candidates

    except Exception as e:
        print(f"❌ Errore critico ricerca Scopus: {e}")
        return []


# ------------------------------------------------------------
# Dettagli + pubblicazioni autore (CON BARRA CARICAMENTO)
# ------------------------------------------------------------
def fetch_author_details(author_id: str):
    """
    Ritorna un dict con metadata autore + lista pubblicazioni.
    Usa TQDM per mostrare il progresso nel terminale.
    """
    print(f"\n Fetching details for author ID: {author_id}\n")

    try:
        au = AuthorRetrieval(author_id, refresh=True)
    except Exception as e:
        print(f" Errore nel recupero autore: {e}")
        return None

    print("✓ Author data retrieved:")
    print(f"✓ Name: {au.given_name} {au.surname}")
    print(f"✓ Total Documents: {au.document_count}")
    print("=" * 60)

    publications = []
    try:
        docs = au.get_documents() or []
        
        # --- BARRA DI CARICAMENTO TQDM ---
        # desc: Testo accanto alla barra
        # unit: Unità di misura (es. "paper")
        for doc in tqdm(docs, desc="⬇ Scaricando Abstract", unit="paper", ncols=100):
            
            eid = getattr(doc, "eid", None)
            if eid:
                try:
            
                    ab = AbstractRetrieval(eid, view='FULL')  
                    doc_type = getattr(ab, "aggregationType", "N/A") 
                    source_type = getattr(ab, "subtype", "N/A")      
                    
                except Exception:
                    doc_type, source_type = "ERROR", "ERROR"
            else:
                doc_type, source_type = "N/A", "N/A"

            title = getattr(doc, "title", "")
            year = getattr(doc, "coverDate", "")[:4]
            cited = getattr(doc, "citedby_count", 0)
            doi = getattr(doc, "doi", "")
            source = getattr(doc, "publicationName", "")
            
            publications.append({
                "title": title,
                "year": year,
                "citations_scopus": cited,
                "venue_scopus": source,
                "doi": doi,
                "document_type": doc_type,
                "source_type": source_type
            })
            
    except Exception as e:
        print(f" Errore nel recupero delle pubblicazioni: {e}")

    aff_str = "N/A"
    if au.affiliation_current:
        aff = au.affiliation_current[0]
        aff_name = getattr(aff, "name", getattr(aff, "organization", "N/A"))
        aff_city = getattr(aff, "city", "N/A")
        aff_country = getattr(aff, "country", "N/A")
        aff_str = f"{aff_name} ({aff_city}, {aff_country})"

    return {
        "author_name": f"{au.given_name} {au.surname}",
        "author_id": author_id,
        "affiliation": aff_str,
        "h_index": au.h_index,
        "document_count": au.document_count,
        "citation_count": au.citation_count,
        "publications": publications
    }


# ------------------------------------------------------------
# Salvataggio CSV
# ------------------------------------------------------------
def save_to_csv(author_data: dict, selected_name: str):
    os.makedirs("data/raw", exist_ok=True)
    filename = f"data/raw/{selected_name}_Scopus.csv"
    df = pd.DataFrame(author_data.get("publications", []))
    df.to_csv(filename, index=False)
    print(f"\n ✓ Dati salvati in: {filename}")