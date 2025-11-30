import os, sys
from pathlib import Path
import pandas as pd


current_file = Path(__file__).resolve()
project_root = current_file.parents[2] 
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))


from src.fetchers import scopus
from src.fetchers import scholar
from src.merge import fuzzy_merge
from pyblio_config import AuthorSearch

RAW_DIR = Path("data/raw")
MERGE_DIR = Path("data/merged")
CACHE_DIR = Path("data/cache")

# Crea cartelle se non esistono
for d in (RAW_DIR, MERGE_DIR, CACHE_DIR):
    d.mkdir(parents=True, exist_ok=True)


# ============================================================
#  1. FUNZIONI DI SUPPORTO (Salvataggio e Metriche)
# ============================================================

def save_author_cache(merged_df, author_name, scholar_id, metrics):
    """
    Salva i risultati finali (divisi per categoria) nella cartella cache.
    Viene chiamata SOLO se il merge ha avuto successo.
    """
    safe_name = author_name.replace(",", "").replace(" ", "_")
    author_dir = CACHE_DIR / f"{safe_name}_{scholar_id}"
    author_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n Salvataggio risultati in: {author_dir}")

    # 1. Salva le metriche riassuntive
    pd.DataFrame(metrics.items(), columns=["Metric", "Value"]).to_csv(author_dir/"metrics.csv", index=False)

    # 2. Salva Conferenze (Ordinate per Rank Core: A*, A, B, C)
    conf_path = author_dir / "conferences.csv"
    if "type" in merged_df.columns:
        # Filtra solo le conferenze
        conf_df = merged_df[merged_df["type"].str.lower().str.contains("conference", na=False)].copy()
        if not conf_df.empty:
            # Logica di ordinamento custom
            rank_order = {"A*": 1, "A": 2, "B": 3, "C": 4}
            conf_df["rank_order"] = conf_df["core_rank"].map(rank_order).fillna(99)
            conf_df.sort_values(by=["year", "rank_order"], ascending=[False, True], inplace=True)
            conf_df.drop(columns=["rank_order"], inplace=True, errors="ignore")
            conf_df.drop(columns=["scimago_quartile", "sjr_core", "sjr_score"], inplace=True, errors="ignore")
            conf_df.to_csv(conf_path, index=False)
        else:
            pd.DataFrame().to_csv(conf_path, index=False) # File vuoto se non ci sono conferenze
    else:
        pd.DataFrame().to_csv(conf_path, index=False)

    # 3. Salva Journal (Ordinati per Quartile SJR: Q1, Q2...)
    journ_path = author_dir / "journals.csv"
    if "type" in merged_df.columns:
        journ_df = merged_df[merged_df["type"].str.lower().str.contains("journal", na=False)].copy()
        if not journ_df.empty:
            q_order = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4}
            journ_df["q_order"] = journ_df["scimago_quartile"].map(q_order).fillna(99)
            journ_df.sort_values(by=["year", "q_order"], ascending=[False, True], inplace=True)
            journ_df.drop(columns=["q_order"], inplace=True, errors="ignore")
            journ_df.to_csv(journ_path, index=False)
        else:
            pd.DataFrame().to_csv(journ_path, index=False)
    else:
        pd.DataFrame().to_csv(journ_path, index=False)

    # 4. Salva Altro (Other Works)
    other_path = author_dir / "other_works.csv"
    if "type" in merged_df.columns:
        other_df = merged_df[~merged_df["type"].str.lower().str.contains("conference|journal", na=False)].copy()
        if not other_df.empty:
            other_df.sort_values(by=["year"], ascending=False, inplace=True)
            other_df.to_csv(other_path, index=False)
        else:
            pd.DataFrame().to_csv(other_path, index=False)
    else:
        pd.DataFrame().to_csv(other_path, index=False)


# ============================================================
#  2. LOGICA DI RICERCA (Disambiguazione)
# ============================================================

def search_scopus_candidates(full_name):
    """
    Cerca autori su Scopus. NON blocca il server.
    Ritorna una lista pulita di candidati per il frontend.
    """
    print(f"🔎 Ricerca Scopus: {full_name}")
    try:
        # Parsing sicuro del nome
        parts = full_name.strip().split()
        if not parts: return []
        last, first = parts[-1], parts[0] if len(parts) > 1 else ""
        
        # Costruzione query
        if first:
            query = f'AUTHLASTNAME({last}) AND AUTHFIRST({first})'
        else:
            query = f'AUTHLASTNAME({last})'
            
        s = AuthorSearch(query)

        candidates = []
        if s.authors:
            for a in s.authors:
                try:
                    # Estrazione degli attributi 
                    raw_id = getattr(a, 'identifier', getattr(a, 'eid', None))
                    if not raw_id: continue
                    
                    clean_id = str(raw_id).split('-')[-1]
                    
                    candidates.append({
                        'id': clean_id,
                        'name': f"{a.surname}, {a.givenname}",
                        'aff': str(a.affiliation) if a.affiliation else "N/A",
                        'documents': getattr(a, 'documents', '0'),
                        'city': str(a.city) if a.city else ""
                    })
                except Exception:
                    continue # Salta singolo autore corrotto
                    
        return candidates

    except Exception as e:
        print(f"❌ Errore Scopus Critico: {e}")
        return []


# ============================================================
#  3. LOGICA DI ELABORAZIONE (Main Pipeline)
# ============================================================

def process_chosen_author(scopus_id, scopus_name, scholar_id):
    """
    Gestisce il processo completo: Download -> Merge -> Salvataggio.
    Gestisce Cache esistente, Mismatch (<60%) e Pulizia file.
    """
    print(f" Avvio elaborazione finale: {scopus_name} ({scopus_id}) - Scholar: {scholar_id}")
    
    safe_name = scopus_name.replace(",", "").replace(" ", "_")
    author_dir = CACHE_DIR / f"{safe_name}_{scholar_id}"
    
    # --- 1. CONTROLLO CACHE ---
    if author_dir.exists():
        print(f"⚡ Cache già presente: {safe_name}. Recupero dati esistenti.")
        return {"status": "success", "folder": author_dir.name}

    # Percorsi dei file temporanei (Raw Data)
    scopus_file = RAW_DIR / f"{safe_name}_Scopus.csv"
    scholar_file = RAW_DIR / f"{safe_name}_Scholar.csv"

    # --- 2. DOWNLOAD DATI ---
    if not scopus_file.exists():
        try:
            print(" Download Scopus in corso...")
            data = scopus.fetch_author_details(scopus_id)
            if data: 
               scopus.save_to_csv(data, safe_name)
            else: 
                return {"status": "error", "msg": "Scopus API ha restituito dati vuoti"}
        except Exception as e: 
            return {"status": "error", "msg": f"Errore Download Scopus: {e}"}

    if not scholar_file.exists():
        try:
            print("📡 Download Scholar in corso...")
            scholar.fetch_scholar_by_id(scholar_id, output_name=safe_name)
        except Exception as e: 
            return {"status": "error", "msg": f"Errore Download Scholar: {e}"}

    # --- 3. MERGE E GESTIONE INTELLIGENTE ERRORI ---
    if scopus_file.exists() and scholar_file.exists():
        try:
            # Tenta il merge. 
            # Se il match è < 60%, fuzzy_merge lancerà ValueError("LOW_MATCH_SCORE")
            merged_df = fuzzy_merge.fuzzy_merge_datasets(scopus_file, scholar_file)

            if merged_df.empty:
                 return {"status": "error", "msg": "Il merge ha prodotto un risultato vuoto."}

            # --- SE SIAMO QUI, IL MERGE È ANDATO BENE (MATCH >= 60%) ---
            
            # Calcolo delle metriche aggregate per il report
            for c in ["citations_scopus", "citations_scholar", "year"]:
                merged_df[c] = pd.to_numeric(merged_df[c], errors="coerce").fillna(0)
            
            # Calcolo anni mancanti (buchi temporali)
            miss_yrs = "N/A"
            if "year" in merged_df.columns:
                yrs = merged_df.loc[merged_df["year"] > 0, "year"].astype(int)
                if not yrs.empty:
                    miss_yrs = ", ".join(map(str, sorted(set(range(yrs.min(), yrs.max()+1)) - set(yrs)))) or "Nessuno"

            metrics = {
                "Totale pubblicazioni": len(merged_df),
                "Totale citazioni Scopus": int(merged_df["citations_scopus"].sum()),
                "Totale citazioni Scholar": int(merged_df["citations_scholar"].sum()),
                "Percentuale Q1": f"{(merged_df['scimago_quartile'].eq('Q1').mean()*100):.1f}%",
                "Percentuale A": f"{(merged_df['core_rank'].eq('A').mean()*100):.1f}%",
                "Percentuale A*": f"{(merged_df['core_rank'].eq('A*').mean()*100):.1f}%",
                "Numero Journal": len(merged_df[merged_df["type"].str.lower()=="journal"]),
                "Numero Conference": len(merged_df[merged_df["type"].str.lower()=="conference proceeding"]),
                "Numero Other Works": len(merged_df[~merged_df["type"].str.lower().isin(["journal","conference proceeding"])]),
                "Anni di non pubblicazione": miss_yrs
            }
            
            # SALVATAGGIO CACHE (Solo ora salviamo i risultati definitivi)
            save_author_cache(merged_df, safe_name, scholar_id, metrics)
            return {"status": "success", "folder": author_dir.name}

        except ValueError as ve:
            error_msg = str(ve)
            
            # === CASO: MATCH TROPPO BASSO (< 60%) ===
            if error_msg == "LOW_MATCH_SCORE":
                print(" Interrotto: Match < 60%. Nessuna cache salvata.")
                
            
                try:
                    if scopus_file.exists(): os.remove(scopus_file)
                    if scholar_file.exists(): os.remove(scholar_file)
                except Exception as e:
                    print(f" Errore pulizia file: {e}")

                # Ritorna status speciale 'mismatch' con messaggio chiaro per l'utente
                return {
                    "status": "mismatch", 
                    "message": "Attenzione: Gli autori sembrano diversi."
                }
            
            elif error_msg == "NO_MATCHES":
                return {"status": "error", "message": "Nessuna corrispondenza trovata."}
            
            else:
                return {"status": "error", "message": f"Errore dati: {error_msg}"}

        except Exception as e:
            return {"status": "error", "message": f"Errore imprevisto nel Merge: {e}"}
            
    else:
        return {"status": "error", "message": "File CSV mancanti, impossibile procedere."}
            
    

       