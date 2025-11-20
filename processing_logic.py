import os
from pathlib import Path
import pandas as pd
from pybliometrics.scopus import AuthorSearch 
import fetcher_scopus
from src.fetchers import scholar_fetch
from src.merge import fuzzy_merge

RAW_DIR = Path("data/raw")
MERGE_DIR = Path("data/merged")
CACHE_DIR = Path("data/cache")
for d in (RAW_DIR, MERGE_DIR, CACHE_DIR): d.mkdir(parents=True, exist_ok=True)

# --- FUNZIONI SUPPORTO ---

def check_cache(selected_name: str, source: str) -> bool:
    return (RAW_DIR / f"{selected_name}_{source}.csv").exists()

def save_author_cache(merged_df, author_name, scholar_id, metrics):
    author_dir = CACHE_DIR / f"{author_name}_{scholar_id}"
    author_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n📁 Salvataggio in: {author_dir}")

    pd.DataFrame(metrics.items(), columns=["Metric", "Value"]).to_csv(author_dir/"metrics.csv", index=False)

    conf_path = author_dir / "conferences.csv"
    if "type" in merged_df.columns:
        conf_df = merged_df[merged_df["type"].str.lower().str.contains("conference", na=False)].copy()
        if not conf_df.empty:
            rank_order = {"A*": 1, "A": 2, "B": 3, "C": 4}
            conf_df["rank_order"] = conf_df["core_rank"].map(rank_order).fillna(99)
            conf_df.sort_values(by=["year", "rank_order"], ascending=[False, True], inplace=True)
            conf_df.drop(columns=["rank_order"], inplace=True, errors="ignore")
            conf_df.to_csv(conf_path, index=False)
        else: pd.DataFrame().to_csv(conf_path, index=False)
    else: pd.DataFrame().to_csv(conf_path, index=False)

    journ_path = author_dir / "journals.csv"
    if "type" in merged_df.columns:
        journ_df = merged_df[merged_df["type"].str.lower().str.contains("journal", na=False)].copy()
        if not journ_df.empty:
            q_order = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4}
            journ_df["q_order"] = journ_df["scimago_quartile"].map(q_order).fillna(99)
            journ_df.sort_values(by=["year", "q_order"], ascending=[False, True], inplace=True)
            journ_df.drop(columns=["q_order"], inplace=True, errors="ignore")
            journ_df.to_csv(journ_path, index=False)
        else: pd.DataFrame().to_csv(journ_path, index=False)
    else: pd.DataFrame().to_csv(journ_path, index=False)

    other_path = author_dir / "other_works.csv"
    if "type" in merged_df.columns:
        other_df = merged_df[~merged_df["type"].str.lower().str.contains("conference|journal", na=False)].copy()
        if not other_df.empty:
            other_df.sort_values(by=["year"], ascending=False, inplace=True)
            other_df.to_csv(other_path, index=False)
        else: pd.DataFrame().to_csv(other_path, index=False)
    else: pd.DataFrame().to_csv(other_path, index=False)

# --- LOGICA PRINCIPALE ---

def search_scopus_candidates(full_name):
    print(f"🔎 Ricerca Scopus: {full_name}")
    try:
        s = AuthorSearch(f'AUTHLASTNAME({full_name.split()[-1]}) AND AUTHFIRST({full_name.split()[0]})')
        return [{
            'id': a.eid.split('-')[-1],
            'name': f"{a.surname}, {a.givenname}",
            'aff': a.affiliation or "N/A",
            'documents': a.documents,
            'city': a.city or ""
        } for a in s.authors] if s.authors else []
    except Exception as e:
        print(f"Errore Scopus: {e}")
        return []

def process_chosen_author(scopus_id, scopus_name, scholar_id):
    """
    Gestisce il processo completo: Download -> Merge -> Salvataggio.
    Gestisce Cache esistente, Mismatch e Pulizia file.
    """
    print(f" Avvio elaborazione finale: {scopus_name} ({scopus_id}) - Scholar: {scholar_id}")
    
    safe_name = scopus_name.replace(",","").replace(" ","_")
    author_dir = CACHE_DIR / f"{safe_name}_{scholar_id}"
    
    # 1. CONTROLLO CACHE 
    if author_dir.exists():
        print(f"⚡ Cache già presente: {safe_name}. Recupero dati esistenti.")
        return {"status": "success", "folder": author_dir.name}

    # Percorsi dei file temporanei
    scopus_file = RAW_DIR / f"{safe_name}_Scopus.csv"
    scholar_file = RAW_DIR / f"{safe_name}_Scholar.csv"

    # 2. DOWNLOAD 
    if not scopus_file.exists():
        try:
            print("📡 Download Scopus...")
            data = fetcher_scopus.fetch_author_details(scopus_id)
            if data: fetcher_scopus.save_to_csv(data, safe_name)
            else: return {"status": "error", "msg": "Scopus API vuota"}
        except Exception as e: return {"status": "error", "msg": f"Errore Scopus: {e}"}

    if not scholar_file.exists():
        try:
            print("📡 Download Scholar...")
            scholar_fetch.fetch_scholar_by_id(scholar_id, output_name=safe_name)
        except Exception as e: return {"status": "error", "msg": f"Errore Scholar: {e}"}

    # 3. MERGE E GESTIONE MISMATCH
    if scopus_file.exists() and scholar_file.exists():
        try:
            # Tenta il merge 
            merged_df = fuzzy_merge.fuzzy_merge_datasets(scopus_file, scholar_file)

            if merged_df.empty:
                 return {"status": "error", "msg": "Merge vuoto (nessun dato)"}

            # --- Calcolo Metriche  ---
            for c in ["citations_scopus", "citations_scholar", "year"]:
                merged_df[c] = pd.to_numeric(merged_df[c], errors="coerce").fillna(0)
            
            miss_yrs = "N/A"
            if "year" in merged_df.columns:
                yrs = merged_df.loc[merged_df["year"]>0, "year"].astype(int)
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
            
            # Salva Cache 
            save_author_cache(merged_df, safe_name, scholar_id, metrics)
            
            return {"status": "success", "folder": author_dir.name}

        except ValueError as ve:
            # === GESTIONE MISMATCH  ===
            if str(ve) == "LOW_MATCH_SCORE":
                print("Interrotto: Match < 60%.")
                
                # CANCELLAZIONE FILE RAW 
                print("Cancellazione file raw non validi...")
                try:
                    if scopus_file.exists(): os.remove(scopus_file)
                    if scholar_file.exists(): os.remove(scholar_file)
                except Exception as e:
                    print(f" Errore pulizia file: {e}")

                return {"status": "mismatch"} # Segnale per il JS
            else:
                return {"status": "error", "msg": str(ve)}
        except Exception as e:
            return {"status": "error", "msg": f"Errore Merge: {e}"}
            
    else:
        return {"status": "error", "msg": "File CSV mancanti"}