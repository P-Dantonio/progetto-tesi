# ANALISI BIBLIOMETRICA RICERCATORI

**Progetto di Tesi di Laurea**
*Tool automatizzato per l'aggregazione, l'analisi e la visualizzazione unificata della produzione scientifica da Scopus e Google Scholar.*

---

## DESCRIZIONE DEL PROGETTO

Questo software nasce dall'esigenza di superare la frammentazione dei dati bibliometrici. Le piattaforme accademiche (come Scopus e Google Scholar) offrono metriche diverse e spesso non comunicanti.

Il sistema sviluppato permette di:
1. **Interrogare automaticamente** le API di Scopus e Scholar.
2. **Unificare i dati** riconoscendo pubblicazioni duplicate tramite algoritmi di matching.
3. **Calcolare metriche avanzate** non disponibili sulle singole piattaforme (confronto citazioni, ranking conferenze CORE, quartili Scimago).
4. **Visualizzare i risultati** su una dashboard web interattiva.

## FUNZIONALITÀ CHIAVE

* **Multi-Source Fetching**
    * **Scopus:** Integrazione nativa tramite la libreria `pybliometrics`.
    * **Google Scholar:** Scraping resiliente tramite `SerpApi`.
* **Intelligent Merging**
    * Unisce i record basandosi su similarità del titolo e anno di pubblicazione, gestendo discrepanze nei metadati.
* **Analisi Qualitativa**
    * Mapping automatico dei **Quartili Scimago (Q1-Q4)** per i Journal.
    * Mapping del **CORE Ranking (A*, A, B, C)** per le Conferenze.
* **User Experience**
    * Feedback visivo in tempo reale nel terminale durante il download.
    * Interfaccia web per l'utente finale.
* **Robustezza**
    * Sistema di **Caching locale** per ridurre le chiamate API e velocizzare le ricerche successive.

---

## ARCHITETTURA DEL SISTEMA

Il progetto adotta la seguente struttura di cartelle professionale:

```text
AnalisiRicercatori-tesi/
│
├── data/                   # Gestione Dati (ignorata da Git)
│   ├── raw/                # Dati grezzi scaricati (CSV)
│   ├── merged/             # Dataset unificati post-processing
│   └── cache/              # Dati finali pronti per la dashboard
│__ set_up
|   |__ requirements.txt    # Dipendenze del progetto
|   |__ setup_pybliometrics.py # File di configurazione per pybliometrics
|
├── src/                    # Codice Sorgente
│   ├── config/             # Configurazioni e API Keys
│   ├── core/               # Logica di Business (Orchestrator)
│   ├── fetchers/           # Moduli di connessione (Scopus, Scholar)
│   └── merge/              # Logica di Fuzzy Matching
│
├── scripts/                # Script di utilità (test connessioni, setup)
├── templates/              # Frontend (HTML)
├── static/                 # Assets (CSS, JS)
├── tests/                  # Unit Testing (Pytest)
├── app.py                  # Entry point Web (Flask)


'''

## Installazione e configurazione:

I prerequisiti per poter far funzionare questo progetto sono:
 > Python 3.10
 > Account Developer Elseiver (per ottenere la API key per Scopus)
 > Account SerpApi per Scholar


## Setup ambiente

# 1. Creazione virtual environment
python -m venv .venv

# 2. Attivazione (Windows)
.venv\Scripts\activate

# 3. Installazione dipendenze
pip install -r requirements.txt


1. Google Scholar (SerpApi)
Inserisci la tua chiave API nel file src/fetchers/scholar.py.

Nota: Il piano gratuito di SerpApi ha un limite di ricerche mensili (max 250). Monitora l'utilizzo per evitare interruzioni.

2. Scopus (Pybliometrics)
Scopus richiede credenziali specifiche e una connessione autorizzata. Requisiti:

>API Key (da dev.elsevier.com)
>InstToken
>VPN Universitaria attiva

Consiglio anti-blocco: Prima di iniziare, invia una mail a datasupportRD@elsevier.com indicando istituto e scopo della ricerca per evitare limitazioni sulle chiamate API. Loro ti forniranno l'Instoken.

## Guida all'installazione di pybliometrics su windows

1. Esegui la configurazione iniziale

python pybliometrics_conf/setup_pybliometrics.py

inserisci la tua chiave scopus e l'instoken quando richiesto

2. Testa l'installazione

python pybliometrics_conf/scripts/00_install_and_test.py

## Come si usa?

from config.pyblio_config import AuthorRetrieval, ScopusSearch

# Il tuo codice qui

---
 # AUTORE: D'Antonio Pia Eugenia



# ANALISI BIBLIOMETRICA RICERCATORI

**Progetto di Tesi di Laurea**
*Tool automatizzato per l'aggregazione, l'analisi e la visualizzazione unificata della produzione scientifica da Scopus e Google Scholar.*

---

## DESCRIZIONE DEL PROGETTO

Questo software nasce dall'esigenza di superare la frammentazione dei dati bibliometrici. Le piattaforme accademiche (come Scopus e Google Scholar) offrono metriche diverse e spesso non comunicanti.

Il sistema sviluppato permette di:
1. **Interrogare automaticamente** le API di Scopus e Scholar.
2. **Unificare i dati** riconoscendo pubblicazioni duplicate tramite algoritmi di matching.
3. **Calcolare metriche avanzate** non disponibili sulle singole piattaforme (confronto citazioni, ranking conferenze CORE, quartili Scimago).
4. **Visualizzare i risultati** su una dashboard web interattiva.

## FUNZIONALITÀ CHIAVE

* **Multi-Source Fetching**
    * **Scopus:** Integrazione nativa tramite la libreria `pybliometrics`.
    * **Google Scholar:** Scraping resiliente tramite `SerpApi`.
* **Intelligent Merging**
    * Unisce i record basandosi su similarità del titolo e anno di pubblicazione, gestendo discrepanze nei metadati.
* **Analisi Qualitativa**
    * Mapping automatico dei **Quartili Scimago (Q1-Q4)** per i Journal.
    * Mapping del **CORE Ranking (A*, A, B, C)** per le Conferenze.
* **User Experience**
    * Feedback visivo in tempo reale nel terminale durante il download.
    * Interfaccia web per l'utente finale.
* **Robustezza**
    * Sistema di **Caching locale** per ridurre le chiamate API e velocizzare le ricerche successive.

---

## ARCHITETTURA DEL SISTEMA

Il progetto adotta la seguente struttura di cartelle professionale:

```text
AnalisiRicercatori-tesi/
│
├── data/                   # Gestione Dati (ignorata da Git)
│   ├── raw/                # Dati grezzi scaricati (CSV)
│   ├── merged/             # Dataset unificati post-processing
│   └── cache/              # Dati finali pronti per la dashboard
│
├── src/                    # Codice Sorgente
│   ├── config/             # Configurazioni e API Keys
│   ├── core/               # Logica di Business (Orchestrator)
│   ├── fetchers/           # Moduli di connessione (Scopus, Scholar)
│   └── merge/              # Logica di Fuzzy Matching
│
├── scripts/                # Script di utilità (test connessioni, setup)
├── templates/              # Frontend (HTML)
├── static/                 # Assets (CSS, JS)
├── tests/                  # Unit Testing (Pytest)
├── app.py                  # Entry point Web (Flask)
└── requirements.txt        # Dipendenze del progetto

'''

## Installazione e configurazione:

I prerequisiti per poter far funzionare questo progetto sono:
 > Python 3.10
 > Account Developer Elseiver (per ottenere la API key per Scopus)
 > Account SerpApi per Scholar


## Setup ambiente

# 1. Creazione virtual environment
python -m venv .venv

# 2. Attivazione (Windows)
.venv\Scripts\activate

# 3. Installazione dipendenze
pip install -r requirements.txt


1. Google Scholar (SerpApi)
Inserisci la tua chiave API nel file src/fetchers/scholar.py.

Nota: Il piano gratuito di SerpApi ha un limite di ricerche mensili (max 250). Monitora l'utilizzo per evitare interruzioni.

2. Scopus (Pybliometrics)
Scopus richiede credenziali specifiche e una connessione autorizzata. Requisiti:

>API Key (da dev.elsevier.com)
>InstToken
>VPN Universitaria attiva

Consiglio anti-blocco: Prima di iniziare, invia una mail a datasupportRD@elsevier.com indicando istituto e scopo della ricerca per evitare limitazioni sulle chiamate API. Loro ti forniranno l'Instoken.

## Guida all'installazione di pybliometrics su windows

Esegui la configurazione iniziale

python pybliometrics_conf/setup_pybliometrics.py

inserisci la tua chiave scopus e l'instoken quando richiesto

## Come si usa?

from pyblio_config import AuthorRetrieval, ScopusSearch

# Il tuo codice qui


Nota: purtroppo per qualche motivo anche se sposto il file pybliometrics e i relativi file che lo utilizzano
in una cartella separata, nonostante le ripetute verifiche sul percorso file, qualcosa si rompe e così ho deciso
di lasciare invariata la configurazione dei file che utilizzano pybliometrics.
---





