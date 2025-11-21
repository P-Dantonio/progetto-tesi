"""
TEST PROCESSING.PY
===========================================
Test per le funzioni di core/processing_logic.py
testa i seguenti aspetti:
- gestione mismatch tra Scopus e Scholar
"""


import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.core.processing_logic import process_chosen_author

# Mockiamo sia Scopus che Scholar fetcher per non scaricare nulla
@patch('src.fetchers.scholar.fetch_scholar_by_id')
@patch('src.fetchers.scopus.fetch_author_details')
# Mockiamo anche la funzione di merge per simulare il risultato
@patch('src.merge.fuzzy_merge.fuzzy_merge_datasets') 
def test_process_mismatch(mock_merge, mock_scopus, mock_scholar):
    
    # Simuliamo che il merge lanci l'errore LOW_MATCH_SCORE
    mock_merge.side_effect = ValueError("LOW_MATCH_SCORE")

    # Chiamiamo la funzione principale
    # Nota: userà file che non esistono, ma li abbiamo mockati quindi ok
    result = process_chosen_author("123", "Mario Rossi", "SCH_123")

    # Verifichiamo che ritorni lo status speciale
    assert result['status'] == "mismatch"
    assert "Match < 60%" in result['message']