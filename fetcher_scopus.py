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
import os
import pandas as pd
from tqdm import tqdm
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
    print(" Pybliometrics directories verified.")


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
def fetch_author_details(author_id: str):
    """
    Ritorna un dict con metadata autore + lista pubblicazioni.
    """
    print(f"\n📡 Fetching details for author ID: {author_id}\n")

    try:
        au = AuthorRetrieval(author_id, refresh=True)
    except Exception as e:
        print(f" Errore nel recupero autore: {e}")
        return None

    print(" Author data retrieved:")
    print("=" * 60)
    print(f" Name: {au.given_name} {au.surname}")

    aff_str = "N/A"
    if au.affiliation_current:
        aff = au.affiliation_current[0]
        aff_name = getattr(aff, "name", getattr(aff, "organization", "N/A"))
        aff_city = getattr(aff, "city", "N/A")
        aff_country = getattr(aff, "country", "N/A")
        aff_str = f"{aff_name} ({aff_city}, {aff_country})"
        print(f"🏛️  Affiliation: {aff_str}")

    print(f"📈 h-index: {au.h_index}")
    print(f"📚 Total Documents: {au.document_count}")
    print(f"🔢 Citations: {au.citation_count}") 
    print(f"🆔 Scopus ID: {author_id}")
    print("=" * 60)

    publications = []
    try:
        docs = au.get_documents() or []

        # Usiamo tqdm per avvolgere 'docs'. 
        # desc="..." è il testo che appare a sinistra della barra.
        for doc in tqdm(docs, desc="Scaricando dettagli pubblicazioni", unit="doc"):
            
            eid = getattr(doc, "eid", None)
            if eid:
                try:
                    ab = AbstractRetrieval(eid, view='FULL')
                    doc_type = getattr(ab, "aggregationType", "N/A") 
                    source_type = getattr(ab, "subtype", "N/A")      
                except Exception as e:
                    # Rimuovi il print dell'errore per non "rompere" la barra grafica, 
                    # oppure stampalo solo se strettamente necessario.
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

    return {
        # ... (resto del return uguale) ...
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
    """
    Salva le pubblicazioni Scopus in data/raw/<selected_name>_Scopus.csv
    """
    os.makedirs("data/raw", exist_ok=True)
    filename = f"data/raw/{selected_name}_Scopus.csv"
    df = pd.DataFrame(author_data.get("publications", []))
    df.to_csv(filename, index=False)
    print(f"\n Dati salvati in: {filename}")
