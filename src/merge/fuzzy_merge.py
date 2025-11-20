#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
fuzzy_merge.py
==============
Unisce i dati Scopus e Google Scholar.
Interrompe l'esecuzione se il match rate è inferiore al 60%.
"""

import os
import pandas as pd
from rapidfuzz import process, fuzz

CORE_PATH = "data/external/core.csv"
SCIMAGO_DIR = "data/external/scimago_clean.csv"

# ============================================================
#  NORMALIZZAZIONE E MATCHING 
# ============================================================

def normalize_venue(v):
    v = str(v).lower()
    replacements = {
        "&": "and", "trans.": "transactions", "proc.": "proceedings",
        "int.": "international", "conf.": "conference", "symp.": "symposium",
        "journ.": "journal", "rev.": "review", ".": "", "-": " "
    }
    for old, new in replacements.items():
        v = v.replace(old, new)
    return " ".join(v.split()).strip()

def find_best_match(venue, ref_list):
    if not isinstance(venue, str) or not venue.strip(): return None
    match = process.extractOne(venue, ref_list, scorer=fuzz.token_sort_ratio, score_cutoff=70)
    return match[0] if match else None

# ============================================================
#  CARICAMENTO DATI ESTERNI 
# ============================================================

def load_core_data():
    try:
        df = pd.read_csv(CORE_PATH, on_bad_lines="skip", quotechar='"')
        df.columns = [c.strip().lower() for c in df.columns]
        name_col, rank_col = df.columns[0], df.columns[3]
        df["venue_norm"] = df[name_col].fillna("").apply(normalize_venue)
        return df, rank_col
    except: return pd.DataFrame(), None

def load_scimago_data():
    if not os.path.exists(SCIMAGO_DIR): return pd.DataFrame()
    try:
        df = pd.read_csv(SCIMAGO_DIR, on_bad_lines="skip", quotechar='"')
        df.columns = [c.strip().lower() for c in df.columns]
        name_col = next((c for c in df.columns if "title" in c), None)
        if name_col: df["venue_norm"] = df[name_col].fillna("").apply(normalize_venue)
        return df
    except: return pd.DataFrame()

# ============================================================
#  MERGE PRINCIPALE 
# ============================================================

def fuzzy_merge_datasets(scopus_file, scholar_file):
    print(f"\n🔗 Avvio confronto tra: {scopus_file.name} e {scholar_file.name}")

    scopus_df = pd.read_csv(scopus_file)
    scholar_df = pd.read_csv(scholar_file)

    # 1. Normalizzazione Titoli
    scopus_df["title_norm"] = scopus_df["title"].fillna("").astype(str).str.lower().str.strip()
    scholar_df["title_norm"] = scholar_df["title"].fillna("").astype(str).str.lower().str.strip()
    
    scholar_title_list = scholar_df["title_norm"].tolist()
    scholar_titles_map = scholar_df.set_index("title_norm")

    merged_rows = []
    match_count = 0
    matched_scholar_titles = set()

    # 2. Matching Scopus/Scholar 
    for _, s_row in scopus_df.iterrows():
        title_norm = s_row["title_norm"]
        match = process.extractOne(title_norm, scholar_title_list, scorer=fuzz.token_sort_ratio, score_cutoff=70)
        
        base_row = {
            "title": s_row["title"].title(),
            "doi": s_row.get("doi", ""),
            "type": s_row.get("document_type", ""),
            "source_type": s_row.get("source_type", "")
        }

        if match:
            match_title_norm = match[0]
            sch_row = scholar_titles_map.loc[match_title_norm]
            
            matched_scholar_titles.add(match_title_norm)
            match_count += 1
            
            base_row.update({
                "year": s_row.get("year", sch_row.get("year", "")),
                "citations_scopus": s_row.get("citations_scopus", 0),
                "citations_scholar": sch_row.get("citations_scholar", 0),
                "venue": s_row.get("venue_scopus", sch_row.get("venue", "")),
                "source": "Scopus + Scholar"
            })
        else:
            base_row.update({
                "year": s_row.get("year", ""),
                "citations_scopus": s_row.get("citations_scopus", 0),
                "citations_scholar": 0,
                "venue": s_row.get("venue_scopus", ""),
                "source": "Scopus"
            })
        merged_rows.append(base_row)

    # =========================================================
    # 3.CONTROLLO PERCENTUALE
    # =========================================================
    
    total_scopus = len(scopus_df)
    match_ratio = match_count / total_scopus if total_scopus > 0 else 0

    print(f"📊 Match trovati: {match_count}/{total_scopus} ({match_ratio:.1%})")

    if match_ratio < 0.60:
        print(f"⚠️ Match < 60% ({match_ratio:.1%}): Probabilmente non sono la stessa persona.")
    
        raise ValueError("LOW_MATCH_SCORE") 
  
    print("✅ Percentuale valida. Integrazione dati in corso...")

 

    # Aggiunta record Scholar 
    unmatched_scholar = scholar_df[~scholar_df["title_norm"].isin(matched_scholar_titles)]
    for _, row in unmatched_scholar.iterrows():
        merged_rows.append({
            "title": row["title"].title(),
            "year": row.get("year", ""),
            "citations_scopus": 0,
            "citations_scholar": row.get("citations_scholar", 0),
            "venue": row.get("venue", ""),
            "source": "Scholar",
            "type": "", "source_type": "", "doi": ""
        })

    merged_df = pd.DataFrame(merged_rows)
    merged_df["venue_norm"] = merged_df["venue"].fillna("").apply(normalize_venue)

    # Merge con CORE
    core_df, core_rank_col = load_core_data()
    if not core_df.empty:
        core_list = core_df["venue_norm"].unique().tolist()
        merged_df["core_match"] = merged_df["venue_norm"].apply(lambda v: find_best_match(v, core_list))
        merged_df = merged_df.merge(core_df, how="left", left_on="core_match", right_on="venue_norm", suffixes=("", "_core"))
        if core_rank_col: merged_df.rename(columns={core_rank_col: "core_rank"}, inplace=True)

    # Merge con SCIMAGO
    sjr_df = load_scimago_data()
    if not sjr_df.empty:
        sjr_list = sjr_df["venue_norm"].unique().tolist()
        merged_df["sjr_match"] = merged_df["venue_norm"].apply(lambda v: find_best_match(v, sjr_list))
        merged_df = merged_df.merge(sjr_df, how="left", left_on="sjr_match", right_on="venue_norm", suffixes=("", "_sjr"))
        
        for col in merged_df.columns:
            if "quartile" in col: merged_df.rename(columns={col: "scimago_quartile"}, inplace=True)
            if "sjr" in col and "match" not in col: merged_df.rename(columns={col: "sjr_score"}, inplace=True)

    # Pulizia Finale
    keep_cols = ["title", "year", "citations_scopus", "citations_scholar", "venue", "doi", "core_rank", "scimago_quartile", "sjr_score", "type", "source"]
    for c in keep_cols:
        if c not in merged_df.columns: merged_df[c] = ""
    
    merged_df = merged_df[keep_cols]
    
    merged_df["core_rank"] = merged_df["core_rank"].fillna("N/A").replace("", "N/A")
    merged_df["scimago_quartile"] = merged_df["scimago_quartile"].fillna("N/A").replace("", "N/A")

    print("✅ Merge completato.")
    return merged_df