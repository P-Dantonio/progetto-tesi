import pandas as pd
import os

# Nomi dei file
SCIMAGO_INPUT_FILE = "data/external/scimago.csv"
SCIMAGO_OUTPUT_FILE = "data/external/scimago_clean.csv"

# 1. Caricamento e pulizia del DataFrame
try:
    # Carica il CSV utilizzando il punto e virgola come separatore
    df_scimago = pd.read_csv(
        SCIMAGO_INPUT_FILE,
        sep=';',
        encoding='utf-8',
        on_bad_lines='skip'
    )

    # Rimuove le colonne completamente vuote (spesso generate da delimitatori finali)
    df_scimago = df_scimago.dropna(axis=1, how='all')

    # Pulizia dei nomi delle colonne (rimuove spazi e rende minuscolo)
    df_scimago.columns = [c.strip().lower() for c in df_scimago.columns]

    # 2. Salvataggio del DataFrame pulito
    # Usiamo il separatore virgola (standard CSV) per l'output, a meno che non sia specificato diversamente
    df_scimago.to_csv(SCIMAGO_OUTPUT_FILE, index=False, encoding='utf-8')

    print(f"✅ File SCImago pulito salvato con successo in '{SCIMAGO_OUTPUT_FILE}'")
    print(f"   Record salvati: {len(df_scimago)}")
    print("   Le colonne pulite sono ora in minuscolo e senza spazi iniziali/finali.")

except FileNotFoundError:
    print(f"⚠️ ERRORE: File di input non trovato: '{SCIMAGO_INPUT_FILE}'")
except Exception as e:
    print(f"⚠️ ERRORE durante l'elaborazione del file: {e}")

# Il DataFrame df_scimago contiene ora i dati puliti e può essere usato nel tuo script principale.