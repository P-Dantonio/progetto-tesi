# diagnose_config.py
import pybliometrics
from pathlib import Path

print(f"Pybliometrics version: {pybliometrics.__version__}\n")

# Check what the startup module is looking for
import pybliometrics.utils.startup as startup

print("Checking startup module functions...\n")

# Try to see what config_dir it's using
try:
    import inspect
    source = inspect.getsource(startup.get_config)
    print("get_config source code:")
    print("-" * 60)
    print(source)
    print("-" * 60)
except Exception as e:
    print(f"Can't get source: {e}")

# Check default paths
print("\nChecking possible config paths:")
possible_paths = [
    Path.home() / '.pybliometrics' / 'config.ini',
    Path.home() / '.config' / 'pybliometrics' / 'config.ini',
    Path.home() / '.pybliometrics.ini',
    Path('.pybliometrics') / 'config.ini',
]

for p in possible_paths:
    print(f"  {p}")
    print(f"    Exists: {p.exists()}")