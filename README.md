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


Ti appare "così" (cioè come testo semplice con dei simboli strani tipo #, *, ```) per due motivi principali:

Stai guardando il "codice sorgente": Il linguaggio si chiama Markdown. Quei simboli servono a dire al computer "questo è un titolo" o "questo è grassetto". È normale vederlo così mentre lo scrivi.

Forse l'estensione è sbagliata: Se il file si chiama README.txt, il computer non sa che deve formattarlo. Deve chiamarsi README.md.

Come vederlo "bello" subito (in VS Code)
Assicurati che il file si chiami README.md.

Mentre hai il file aperto, premi sulla tastiera: Ctrl + Shift + V.

Vedrai aprirsi un'anteprima formattata con i titoli grandi, i grassetti e i colori, esattamente come apparirà su GitHub o ai professori.

⚠️ Attenzione: c'erano errori nel testo che hai incollato
Nel testo che mi hai mostrato sopra c'erano dei piccoli errori di sintassi (mancavano delle chiusure dei blocchi di codice ```) e c'erano ancora i percorsi vecchi (pybliometrics_conf/...).

Copia e incolla questo blocco qui sotto. È corretto, pulito e usa i percorsi giusti della tua nuova struttura (scripts/, src/, ecc.).

Markdown

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




INSTALLAZIONE E SETUP
1. Prerequisiti
Per il corretto funzionamento del software sono necessari:

Python 3.10 o superiore.

Account Developer Elsevier (per ottenere la API key per Scopus).

Account SerpApi (per interrogare Google Scholar).

VPN Universitaria (necessaria per l'autenticazione IP di Scopus).


## Setup ambiente

# 1. Creazione virtual environment
python -m venv .venv

# 2. Attivazione (Windows)
.venv\Scripts\activate

# 3. Installazione dipendenze
pip install -r requirements.txt


1. Google Scholar (SerpApi)
Inserisci la tua chiave API nel file src/fetchers/scholar.py.

Nota: Il piano gratuito di SerpApi ha un limite di ricerche mensili (circa 250). Monitora l'utilizzo per evitare interruzioni.

2. Scopus (Pybliometrics)
Scopus richiede credenziali specifiche e una connessione autorizzata. Requisiti:

API Key (da dev.elsevier.com)

InstToken

VPN Universitaria attiva

Consiglio anti-blocco: Prima di iniziare, invia una mail a datasupportRD@elsevier.com indicando istituto e scopo della ricerca per evitare limitazioni sulle chiamate API.
> chiave API 
> InstToken
> VPN universitaria

## Guida all'installazione di pybliometrics su windows

1. Esegui la configurazione iniziale

python pybliometrics_conf/setup_pybliometrics.py

inserisci la tua chiave scopus e l'instoken quando richiesto

2. Testa l'installazione

python pybliometrics_conf/scripts/00_install_and_test.py

## Come si usa?

from config.pyblio_config import AuthorRetrieval, ScopusSearch

# Il tuo codice qui




