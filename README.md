
Il sistema sviluppato permette di:

1.  **Interrogare automaticamente** le API di Scopus e Scholar.
    
2.  **Unificare i dati** riconoscendo pubblicazioni duplicate tramite algoritmi di matching.
    
3.  **Calcolare metriche avanzate** non disponibili sulle singole piattaforme (confronto citazioni, ranking conferenze CORE, quartili Scimago).
    
4.  **Visualizzare i risultati** su una dashboard web interattiva.
    

----------

## FUNZIONALITÀ CHIAVE

### Multi-Source Fetching

-   **Scopus:** Integrazione nativa tramite la libreria `pybliometrics`.
    
-   **Google Scholar:** Scraping resiliente tramite `SerpApi`.
    

### Intelligent Merging

-   Unisce i record basandosi su similarità del titolo e anno di pubblicazione, gestendo discrepanze nei metadati.
    

### Analisi Qualitativa

-   Mapping automatico dei **Quartili Scimago (Q1–Q4)** per i Journal.
    
-   Mapping del **CORE Ranking (A*, A, B, C)** per le Conferenze.
    

### User Experience

-   Feedback visivo in tempo reale nel terminale durante il download.
    
-   Interfaccia web per l’utente finale.
    

### Robustezza

-   Sistema di **Caching locale** per ridurre le chiamate API e velocizzare le ricerche successive.
    

----------

AnalisiRicercatori-tesi/
│
├── data/                     # Dati locali o file CSV generati
│
├── set_up/                   # Script e file per configurazione e installazione
│ ├── requirements.txt        # Librerie Python necessarie
│ └── setup_pybliometrics.py  # Configurazione Pybliometrics (Scopus API)
│
├── src/                      # Codice sorgente principale
│ ├── core/                   # Logica centrale del progetto
│ │ └── processing_logic.py   # Funzioni di elaborazione dei dati
│ │
│ ├── fetchers/               # Moduli per il recupero dati da fonti esterne
│ │ ├── scholar.py            # Fetcher per Google Scholar
│ │ └── scopus.py             # Fetcher per Scopus (Pybliometrics)
│ │
│ └── merge/                  # Logica di fusione e pulizia dei dati
│   └── fuzzy_merge.py        # Merge fuzzy dei record simili
│
├── static/                   # File statici per il frontend
│ ├── dashboard.js            # Script JavaScript del dashboard
│ └── style.css               # Stile CSS della pagina
│
├── templates/                # Template HTML
│ └── index.html              # Pagina principale del dashboard
│
├── tests/                    # Test automatici dei vari componenti
│ ├── pyblio_config_test.py   # Test configurazione Pybliometrics
│ ├── scholar_test.py         # Test fetcher Google Scholar
│ ├── test_installazione.py   # Verifica delle dipendenze
│ ├── test_processing.py      # Test della logica di elaborazione
│ ├── test_profilo_autore.py  # Test profili autori
│ ├── test_scopus.py          # Test fetcher Scopus
│ └── test_utils.py           # Test utility varie
│
├── app.py                    # Entry point dell'applicazione web
├── pyblio_config.py          # Configurazione API Scopus
├── .gitignore                # File da ignorare in Git
├── .env                      # Variabili d'ambiente sensibili
└── README.md                 # Documentazione generale del progetto


----------

# Installazione e configurazione

I prerequisiti per poter utilizzare il software sono:

-   **Python 3.10**
    
-   **Account Developer Elsevier** per ottenere la API key Scopus
    
-   **Account SerpApi** per Google Scholar
    

----------

## Setup ambiente

### 1. Creazione virtual environment

`python -m venv .venv` 

### 2. Attivazione (Windows)

`.venv\Scripts\activate` 

### 3. Installazione dipendenze

`pip install -r requirements.txt` 

----------

## Configurazioni

### Google Scholar (SerpApi)

Inserisci la tua chiave API nel file:

`src/fetchers/scholar.py` 

Nota: Il piano gratuito SerpApi ha un limite mensile di 250 ricerche. Monitora l’utilizzo per evitare blocchi.

----------

### Scopus (Pybliometrics)

Scopus richiede credenziali specifiche e spesso l’accesso tramite VPN universitaria.

Requisiti:

-   API Key (da dev.elsevier.com)
    
-   InstToken
    
-   Connessione autorizzata (rete universitaria o VPN)
    

Consiglio anti-blocco:  
Invia una mail a:

`datasupportRD@elsevier.com` 

indicando:

-   Nome istituto
    
-   Scopo della ricerca
    

per ottenere un InstToken e un profilo senza limitazioni.

----------

## Installazione di Pybliometrics su Windows

Esegui la configurazione iniziale:

`python pybliometrics_conf/setup_pybliometrics.py` 

Inserisci API Key e InstToken quando richiesto.

----------

## Come si usa?

`from pyblio_config import AuthorRetrieval, ScopusSearch # Il tuo codice qui` 

Nota: attualmente, se i file `pybliometrics` vengono spostati in altre cartelle, la libreria potrebbe non trovarli correttamente. Per stabilità si è scelto di metterli nelle cartelle con i file che li utilizzano.
