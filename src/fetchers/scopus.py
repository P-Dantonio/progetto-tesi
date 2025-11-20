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
from src.pybliometrics_conf.config.pyblio_config import AuthorSearch, AuthorRetrieval


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
        print(" Inserisci sia nome che cognome.")
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


def fetch_author_details(author_id):
    """
    Scarica i dettagli dell'autore e i suoi documenti.
    Include messaggi di stato semplici (senza tqdm) per mostrare il progresso.
    """
    print(f"\n[SCOPUS] Connessione al database per ID: {author_id}...")
    
    try:
        # 1. Scaricamento Profilo
        print(" Scaricamento profilo autore in corso...", end=" ", flush=True)
        
        # refresh=False usa la cache se c'è, True scarica sempre da zero
        au = AuthorRetrieval(author_id, refresh=False) 
        print("Fatto!")
        
        # 2. Recupero Documenti (Questo è il punto dove di solito si "blocca")
        print("recuperando la lista delle pubblicazioni (attendere)...", end=" ", flush=True)
        docs = au.get_documents()
        print(f"Fatto! Trovati {len(docs)} documenti.")

        if not docs:
            return []

        data_list = []
        total_docs = len(docs)
        
        print(f"[SCOPUS] Inizio elaborazione dati:")

        # 3. Ciclo di elaborazione con contatore manuale
        for i, doc in enumerate(docs, 1):
            
            # Stampa un aggiornamento ogni 10 documenti (per non intasare il terminale)
            # oppure se è l'ultimo.
            if i % 10 == 0 or i == total_docs:
                print(f"   > Elaborazione documento n.{i} su {total_docs}...", flush=True)

            data_list.append({
                "title": doc.title,
                "year": doc.coverDate[:4] if doc.coverDate else "",
                "citations_scopus": int(doc.citedby_count) if doc.citedby_count else 0,
                "type": doc.aggregationType,
                "doi": doc.doi,
                "eid": doc.eid,
                "journal": doc.publicationName
            })
            
        # Convertiamo in DataFrame
        df = pd.DataFrame(data_list)
        print(f"[SCOPUS] Finito. Creato dataset con {len(df)} righe.\n")
        
        return df

    except Exception as e:
        print(f"\n[ERRORE SCOPUS]: {e}")
        return None


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
    return filename
