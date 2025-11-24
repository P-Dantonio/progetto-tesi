# Nel file tests/test_processing.py

import pytest
import os
import pandas as pd
from unittest.mock import patch, MagicMock
from src.core.processing_logic import process_chosen_author 


# L'ordine dei decoratori (dall'alto verso il basso) è l'ordine inverso dell'iniezione nella funzione.
@patch('os.remove')                                        
@patch('src.fetchers.scholar.fetch_scholar_by_id')          
@patch('src.fetchers.scopus.save_to_csv')                  
@patch('src.fetchers.scopus.fetch_author_details')          
@patch('src.merge.fuzzy_merge.fuzzy_merge_datasets')        
@patch('pathlib.Path.exists')                               
def test_process_mismatch(mock_path_exists, mock_merge, 
                          mock_fetch_details, mock_save_csv,
                          mock_scholar, mock_os_remove): 
    
    
    # Sequenza di Path.exists() che permette di testare il merge error:
    mock_path_exists.side_effect = [
        False, # 1. Cache Check
        True,  # 2. Scopus File Check (Bypass download)
        True,  # 3. Scholar File Check (Bypass download)
        True,  # 4. Scopus File Check (Merge block)
        True,  # 5. Scholar File Check (Merge block)
        True,  # 6. Scopus File Check (Pulizia)
        True,  # 7. Scholar File Check (Pulizia)
    ]

    
    # Simula che il merge lanci l'errore che la funzione deve gestire.
    mock_merge.side_effect = ValueError("LOW_MATCH_SCORE")


    # Fetch details deve ritornare dati per non innescare l'errore "dati vuoti" nel codice
    mock_fetch_details.return_value = ["fake data"] 
 

    # 4. Chiamiamo la funzione principale
    result = process_chosen_author("123", "Mario Rossi", "SCH_123")


    # Verifichiamo che l'errore sia stato gestito e lo stato sia quello speciale "mismatch"
    assert result['status'] == "mismatch"
    assert "Attenzione: Gli autori sembrano diversi." in result['message']
    

    mock_os_remove.assert_called()