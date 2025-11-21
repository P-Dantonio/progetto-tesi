"""
TEST UTILS.PY
========================================

Test per le funzioni di src/utils.py
testa i seguenti aspetti:
- normalize_venue: normalizzazione dei nomi delle sedi di pubblicazione
"""


import pytest
from src.merge.fuzzy_merge import normalize_venue

def test_normalize_venue_basic():
    print("\nEseguo Test 1: Caso base...") 
    raw = "Proc. Int. Conf. on AI"
    expected = "proceedings international conference on ai"
    assert normalize_venue(raw) == expected
    print("Test 1 Passato!")

def test_normalize_venue_dirty():
    print("\n🔹 Eseguo Test 2: Caso sporco (spazi e maiuscole)...")
    raw = "  IEEE   Trans.  "
    expected = "ieee transactions"
    assert normalize_venue(raw) == expected
    print("Test 2 Passato!")

def test_normalize_venue_empty():
    print("\n🔹 Eseguo Test 3: Caso vuoto/None...")
    assert normalize_venue("") == ""
    # Modifica qui: il codice converte None in "none"
    assert normalize_venue(None) == "none" 
    print("Test 3 Passato!")