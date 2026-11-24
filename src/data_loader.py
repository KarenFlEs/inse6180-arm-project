# Loads the MITRE ATT&CK dataset, automatically downloading it if necessary

import json
import urllib.request
import urllib.error
from pathlib import Path

# Project paths
PROJECT_ROOT =  Path(__file__).resolve().parents[1]
RAW_DATASET_DIR = PROJECT_ROOT / 'data/raw'
RAW_DATASET_PATH = RAW_DATASET_DIR / 'enterprise-attack-20.0.json'

# MITRE ATT&CK Enterprise dataset (version 20.0)
DATASET_URL = ('https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-20.0.json')

def validate_dataset(raw_data):
    """Validate the structure of the MITRE ATT&CK dataset."""

    if not isinstance(raw_data, dict):
        raise ValueError("Dataset must be a JSON object.")

    if not isinstance(raw_data.get("objects"), list):
        raise ValueError("Dataset must contain an objects list.")

    if not raw_data["objects"]:
        raise ValueError("MITRE ATT&CK dataset contains no objects.")

def download_dataset(): 
    '''Download the MITRE ATT&CK dataset and save it locally'''  
    RAW_DATASET_DIR.mkdir(parents=True, exist_ok=True)

    # Temporary download location in case error in download
    temp_path = RAW_DATASET_PATH.with_suffix(".tmp")
    try:
        # Download dataset from GitHub
        print('Downloading MITRE ATT&CK Enterprise Dataset...')
        with urllib.request.urlopen(DATASET_URL, timeout=30) as response:
            with open(temp_path, "wb") as file:
                file.write(response.read())

        # Validate the downloaded JSON
        with open(temp_path, "r", encoding="utf-8") as file:
            raw_data = json.load(file)

        validate_dataset(raw_data)
        
        # Replace the local dataset only after successful validation
        temp_path.replace(RAW_DATASET_PATH)
        print("Dataset downloaded successfully.")
        print(f'Saved to:  {RAW_DATASET_PATH}')

    except (urllib.error.URLError, OSError, ValueError, json.JSONDecodeError) as error:
        temp_path.unlink(missing_ok=True)
        raise RuntimeError(f"Dataset download failed: {error}") from error
    


def load_dataset():
    '''Load the MITRE ATT&CK dataset into Python'''

    # Download dataset only if missing locally
    if not RAW_DATASET_PATH.exists():
        download_dataset()
    else:
        print('Dataset already exists locally')

    # Load and validate the local dataset
    try:
        with open(RAW_DATASET_PATH, "r", encoding="utf-8") as file:
            raw_data = json.load(file)

        validate_dataset(raw_data)

    except (OSError, json.JSONDecodeError, ValueError) as error:
        raise RuntimeError(f"Failed to load or validate the MITRE ATT&CK dataset: {error}") from error

    print ('Dataset loaded successfully')
    return raw_data

