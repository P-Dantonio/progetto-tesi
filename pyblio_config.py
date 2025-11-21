
"""
MODULO DI CONFIGURAZIONE PYBLIOMETRICS
========================================

Questo modulo gestisce l'intera configurazione di Pybliometrics per i sistemi Windows.
Inizializza automaticamente la variabile CONFIG e crea le directory necessarie.

USO:
    from config.pyblio_config import AuthorRetrieval, ScopusSearch
    
    au = AuthorRetrieval("author_id")
    results = ScopusSearch("TITLE(keywords)")

Questo modulo DEVE essere importato in TUTTI i tuoi script invece di importare
direttamente da pybliometrics.scopus

IMPORTANTE: Configurazione specifica per Windows
Pybliometrics 4.x ha requisiti di configurazione specifici su Windows.
Questo modulo gestisce tutto ciò automaticamente.
"""

import os
from pathlib import Path
import configparser

# ============================================================================
# PASSO 1: Setup della Configurazione
# ============================================================================

# Definisce il percorso del file di configurazione
config_file = Path.home() / '.pybliometrics' / 'config.ini'
os.environ['PYB_CONFIG_FILE'] = str(config_file)

# ============================================================================
# PASSO 2: Inizializzazione della Variabile CONFIG
# ============================================================================
# Questo è critico per Pybliometrics 4.x su Windows
# La funzione get_config() verifica questa variabile globale

import pybliometrics.utils.startup as startup

# Legge il file di configurazione
config = configparser.ConfigParser()
config.read(config_file)

# Imposta la variabile CONFIG che Pybliometrics verifica
startup.CONFIG = config

# ============================================================================
# PASSO 3: Creazione della Struttura delle Directory
# ============================================================================
# Pybliometrics necessita di una specifica struttura di directory per il caching dei risultati.
# Queste vengono create automaticamente al primo avvio, ma qui ne garantiamo l'esistenza.

scopus_dir = Path.home() / '.pybliometrics' / 'Scopus'

subdirs = [
    'abstract_retrieval/STANDARD',
    'abstract_retrieval/COMPLETE',
    'abstract_retrieval/FULL',
    'abstract_retrieval/REF',
    'author_retrieval/STANDARD',
    'author_retrieval/COMPLETE', 
    'author_retrieval/ENHANCED',
    'author_search',
    'affiliation_retrieval',
    'affiliation_search',
    'citation_overview',
    'scopus_search',
    'serial_search',
    'serial_title',
    'plumx',
    'subject_classification'
]

for subdir in subdirs:
    (scopus_dir / subdir).mkdir(parents=True, exist_ok=True)

# ============================================================================
# PASSO 4: Importazione delle Classi Pybliometrics
# ============================================================================
# Ora che la configurazione è impostata, possiamo importare ed esportare le classi principali

from pybliometrics.scopus import (
    ScopusSearch,               # Ricerca di pubblicazioni
    AuthorRetrieval,            # Recupero informazioni autore
    AbstractRetrieval,          # Recupero dettagli pubblicazione
    AffiliationRetrieval,       # Recupero informazioni istituzione
    AuthorSearch,               # Ricerca di autori
    AffiliationSearch,          # Ricerca di istituzioni
    SerialSearch,               # Ricerca di riviste/serials
    SerialTitle,                # Recupero informazioni riviste
    PlumXMetrics,               # Recupero metriche PlumX (articoli)
    SubjectClassifications      # Recupero classificazioni aree tematiche
)

from pybliometrics.scopus.abstract_retrieval import AbstractRetrieval

# ============================================================================
# ESPORTO LE CLASSI
# ============================================================================
# Rendo disponibili tutte le classi principali per l'importazione diretta

__all__ = [
    'ScopusSearch',
    'AuthorRetrieval',
    'AbstractRetrieval',
    'AffiliationRetrieval',
    'AuthorSearch',
    'AffiliationSearch',
    'SerialSearch',
    'SerialTitle',
    'PlumXMetrics',
    'SubjectClassifications'
]

# ============================================================================
# ESEMPI DI UTILIZZO
# ============================================================================
"""
Esempio 1: Recupero Profilo Autore
    from pybliometrics.scopus import AuthorRetrieval
    
    au = AuthorRetrieval("7004212771")
    print(f"Nome: {au.given_name} {au.surname}")
    print(f"Documenti: {au.document_count}")
    print(f"Citazioni: {au.citation_count}")
    print(f"h-index: {au.h_index}")

Esempio 2: Ricerca Pubblicazioni
    from pybliometrics.scopus import ScopusSearch
    
    query = "TITLE-ABS-KEY(machine learning) AND PUBYEAR > 2020"
    results = ScopusSearch(query, download=False)
    print(f"Trovati {results.get_results_size()} risultati")

Esempio 3: Recupero Dettagli Pubblicazione
    from pybliometrics.scopus import AbstractRetrieval
    
    pub = AbstractRetrieval("doi_or_eid")
    print(f"Titolo: {pub.title}")
    print(f"Autori: {pub.author_names}")
    print(f"Citazioni: {pub.citedby_count}")
"""