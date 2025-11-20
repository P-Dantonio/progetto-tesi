"""
SCRIPT DI TEST INSTALLAZIONE
========================================

Questo script verifica che Pybliometrics sia installato e configurato correttamente.
Esegui questo script dopo aver lanciato setup_pybliometrics.py

Esegue due test:
1. Recupero Autore - Recupera i dati del profilo di un autore
2. Ricerca Pubblicazioni - Cerca delle pubblicazioni

Se entrambi i test hanno successo, l'installazione è completa!
"""
import os, sys
current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.dirname(os.path.dirname(current_dir))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Importa dal nostro modulo di configurazione
from pyblio_config_test import AuthorRetrieval, ScopusSearch

def test_author_retrieval():
    """
    Test 1: Recupera profilo autore
    Usa un ID autore Scopus reale per testare la connessione
    """
    print("\n" + "="*70)
    print("TEST 1: RECUPERO AUTORE")
    print("="*70)
    print("Tentativo di recupero profilo autore in corso...")
    
    try:
        # Recupera l'autore con ID 7004212771 (John R. Kitchin dalla CMU)
        au = AuthorRetrieval("7004212771")
        
        print("\n✓ SUCCESSO! Il recupero autore funziona!\n")
        print(f"  Nome: {au.given_name} {au.surname}")
        print(f"  Affiliazione: {au.affiliation_current}")
        print(f"  Documenti: {au.document_count}")
        print(f"  Citazioni: {au.citation_count}")
        print(f"  h-index: {au.h_index}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ FALLITO: {e}")
        print("\nRisoluzione problemi:")
        print("  1. Sei connesso alla VPN universitaria?")
        print("  2. La tua chiave API è valida? Controlla su https://dev.elsevier.com/")
        print("  3. La tua istituzione ha accesso a Scopus?")
        return False


def test_publication_search():
    """
    Test 2: Cerca pubblicazioni
    Esegue una semplice ricerca per parole chiave per testare la funzionalità di ricerca
    """
    print("\n" + "="*70)
    print("TEST 2: RICERCA PUBBLICAZIONI")
    print("="*70)
    print("Ricerca pubblicazioni su 'machine learning'...")
    
    try:
        # Cerca pubblicazioni con il titolo contenente "machine learning"
        query = "TITLE(machine learning)"
        results = ScopusSearch(query, download=False)
        
        print(f"\n✓ SUCCESSO! La ricerca funziona!\n")
        print(f"  Trovati {results.get_results_size()} risultati totali")
        
        # Mostra i primi 3 risultati
        if results.results:
            print(f"\n  Primi 3 risultati:")
            for i, doc in enumerate(results.results[:3], 1):
                print(f"\n    {i}. {doc.title}")
                print(f"       Autori: {doc.author_names}")
                print(f"       Anno: {doc.coverDate}")
                print(f"       Citazioni: {doc.citedby_count}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ FALLITO: {e}")
        print("\nRisoluzione problemi:")
        print("  1. Controlla la connessione VPN")
        print("  2. Verifica la chiave API")
        print("  3. Controlla la connessione internet")
        return False


def main():
    """
    Esegue tutti i test e riporta i risultati
    """
    print("\n" + "="*70)
    print("TEST INSTALLAZIONE PYBLIOMETRICS")
    print("="*70)
    print("Questo script testa la tua installazione di Pybliometrics")
    
    # Esegui i test
    test1_passed = test_author_retrieval()
    test2_passed = test_publication_search()
    
    # Riepilogo
    print("\n" + "="*70)
    print("RIEPILOGO TEST")
    print("="*70)
    
    if test1_passed and test2_passed:
        print("\n✓✓✓ TUTTI I TEST SUPERATI! ✓✓✓")
        print("\nLa tua installazione di Pybliometrics è completa e funzionante!")
        print("Ora puoi usare Pybliometrics nei tuoi script.")
        print("\nProssimi passi:")
        print("  1. Esamina gli altri script nella cartella 'scripts/'")
        print("  2. Modificali per la tua ricerca")
        print("  3. Inizia ad analizzare i dati Scopus!")
    else:
        print("\n✗ ALCUNI TEST FALLITI")
        print("Per favore controlla le informazioni di risoluzione problemi qui sopra.")
        print("Se i problemi persistono, verifica la tua configurazione e l'accesso VPN.")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    main()