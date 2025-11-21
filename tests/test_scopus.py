"""
TEST SCOPUS.PY
===========================================
Test unitari per le funzioni di fetchers/scopus.py

fa le seguenti verifiche:
- search_author_by_name: ricerca autori per nome
"""


import pytest
from unittest.mock import patch, MagicMock
from src.fetchers.scopus import search_author_by_name

# @patch sostituisce 'AuthorSearch' con un oggetto finto (mock)
@patch('src.fetchers.scopus.AuthorSearch')
def test_search_author_success(mock_search_class):
    
    # 1. PREPARIAMO IL FINTO SCOPUS
    # Creo un autore finto
    fake_author = MagicMock()
    fake_author.givenname = "Mario"
    fake_author.surname = "Rossi"
    fake_author.eid = "9-s2.0-123456789"
    fake_author.affiliation = "University of Test"
    fake_author.documents = "10"
    fake_author.city = "Rome"

    # Configuro il mock per restituire una lista con il mio autore finto
    mock_instance = mock_search_class.return_value
    mock_instance.authors = [fake_author]

    # 2. CHIAMO LA FUNZIONE DA TESTARE
    results = search_author_by_name("Mario Rossi")

    # 3. VERIFICO I RISULTATI
    assert len(results) == 1
    assert results[0]['name'] == "Rossi, Mario"
    assert results[0]['id'] == "123456789"
    
    # Verifico che AuthorSearch sia stato chiamato con la query corretta
    mock_search_class.assert_called_with("AUTHLASTNAME(Rossi) AND AUTHFIRST(Mario)")

@patch('src.fetchers.scopus.AuthorSearch')
def test_search_author_empty(mock_search_class):
    # testo il caso in cui non si trova nessuno
    mock_instance = mock_search_class.return_value
    mock_instance.authors = None # Scopus non trova nulla

    results = search_author_by_name("Fantasma Formaggino")
    
    assert results == [] # Deve tornare lista vuota