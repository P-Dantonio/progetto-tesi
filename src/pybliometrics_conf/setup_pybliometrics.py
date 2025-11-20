"""
script per la configurazione di Pybliometrics
Esegui questo script una sola volta all'inizio per configurare Pybliometrics.
"""

from pathlib import Path
import os

def setup_pybliometrics():
    """
    Crea la struttura delle directory di configurazione per Pybliometrics
    """
    print("=" * 70)
    print("CONFIGURAZIONE PYBLIOMETRICS")
    print("=" * 70)
    print("\nQuesto script configurerà Pybliometrics per il tuo progetto.\n")
    
    # Ottieni le credenziali API dall'utente
    api_key = input("Inserisci la tua Chiave API Scopus: ").strip()
    if not api_key:
        print("ERRORE: La Chiave API è obbligatoria!")
        return False
    
    insttoken = input("Inserisci il tuo InstToken (opzionale, premi Invio per saltare): ").strip()
    
    # Crea la directory di configurazione
    config_dir = Path.home() / '.pybliometrics'
    config_dir.mkdir(exist_ok=True)
    
    config_file = config_dir / 'config.ini'
    
    # Crea il contenuto della configurazione
    # (Nota: I nomi delle sezioni come [Authentication] non vanno tradotti perché la libreria li richiede così)
    config_content = f"""[Authentication]
APIKey = {api_key}
InstToken = {insttoken}

[Directories]
AbstractRetrieval = {config_dir}/Scopus/abstract_retrieval
AuthorRetrieval = {config_dir}/Scopus/author_retrieval
AuthorSearch = {config_dir}/Scopus/author_search
AffiliationRetrieval = {config_dir}/Scopus/affiliation_retrieval
AffiliationSearch = {config_dir}/Scopus/affiliation_search
CitationOverview = {config_dir}/Scopus/citation_overview
ScopusSearch = {config_dir}/Scopus/scopus_search
SerialSearch = {config_dir}/Scopus/serial_search
SerialTitle = {config_dir}/Scopus/serial_title
PlumXMetrics = {config_dir}/Scopus/plumx
SubjectClassifications = {config_dir}/Scopus/subject_classification
"""
    
    # Scrivi il file di configurazione
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print(f"\n✓ File di configurazione creato in: {config_file}")
    
    # Crea la struttura delle directory con tutti i tipi di visualizzazione (view types)
    subdirs = [
        'abstract_retrieval/STANDARD', 'abstract_retrieval/COMPLETE',
        'abstract_retrieval/FULL', 'abstract_retrieval/REF',
        'author_retrieval/STANDARD', 'author_retrieval/COMPLETE', 
        'author_retrieval/ENHANCED', 'author_search',
        'affiliation_retrieval', 'affiliation_search',
        'citation_overview', 'scopus_search', 'serial_search',
        'serial_title', 'plumx', 'subject_classification'
    ]
    
    for subdir in subdirs:
        (config_dir / 'Scopus' / subdir).mkdir(parents=True, exist_ok=True)
    
    print("✓ Tutte le directory sono state create")
    print("\n" + "=" * 70)
    print("CONFIGURAZIONE COMPLETATA!")
    print("=" * 70)
    print("\nProssimo passo: Esegui 'python scripts/00_install_and_test.py'")
    print("\nOra puoi eliminare questo script di configurazione se lo desideri.")
    
    return True

if __name__ == "__main__":
    setup_pybliometrics()