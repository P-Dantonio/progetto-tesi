from pathlib import Path
import os 

def setuppybliometrics():
    """Set up pybliometrics by creating necessary directories and configuration files."""
    config_dir = Path.home() / '.pybliometrics'
    config_file = config_dir / 'config.ini'
    
    # Create configuration directory if it doesn't exist
    if not config_dir.exists():
        os.makedirs(config_dir)
        print(f"Created configuration directory at {config_dir}")
    
    # Create a default configuration file if it doesn't exist
    if not config_file.exists():
        with open(config_file, 'w') as f:
            f.write("[DEFAULT]\n")
            f.write("api_key = YOUR_API_KEY_HERE\n")
        print(f"Created default configuration file at {config_file}")
    else:
        print(f"Configuration file already exists at {config_file}")