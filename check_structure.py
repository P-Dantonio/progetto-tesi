# check_structure.py
import pybliometrics

print("Pybliometrics version:", pybliometrics.__version__)
print("\nAvailable modules in pybliometrics:")

import pkgutil
for importer, modname, ispkg in pkgutil.iter_modules(pybliometrics.__path__):
    print(f"  - {modname}")

print("\nChecking scopus submodule:")
try:
    import pybliometrics.scopus
    for importer, modname, ispkg in pkgutil.iter_modules(pybliometrics.scopus.__path__):
        print(f"  - scopus.{modname}")
except Exception as e:
    print(f"  Error: {e}")

print("\nTrying to find utils:")
try:
    from pybliometrics import utils
    print("  ✓ Found: pybliometrics.utils")
except:
    try:
        from pybliometrics.scopus import utils
        print("  ✓ Found: pybliometrics.scopus.utils")
    except:
        print("  ✗ Utils not found in expected locations")