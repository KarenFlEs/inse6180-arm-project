# Loads the dataset wihtout requiring manual downloading

import json
import urllib.request
import urllib.error
from pathlib import Path

# Project paths
PROJECT_ROOT =  Path(__file__).resolve().parents[1]
RAW_DATASET_DIR = PROJECT_ROOT / 'data/raw'
RAW_DATASET_PATH = RAW_DATASET_DIR / 'enterprise-attack-20.0.json'

# MITRE ATT&CK Enterprise dataset
DATASET_URL = ('https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-20.0.json')


def download_dataset(): 
    '''Download the MITRE ATT&CK dataset and save it locally'''  
    RAW_DATASET_DIR.mkdir(parents=True, exist_ok=True)

    # Temporary downloaad location in case error in download
    temp_path = RAW_DATASET_PATH.with_suffix(".tmp")
    try:
        # Download dataset from GitHub
        print('Downloading MITRE ATT&CK Enterprise Dataset...')
        urllib.request.urlretrieve(DATASET_URL, temp_path)

        # Validate the downloaded JSON
        with open(temp_path, "r", encoding="utf-8") as file:
            raw_data = json.load(file)

        if not isinstance(raw_data, dict) or not isinstance(raw_data.get("objects"), list):
            raise ValueError("Invalid MITRE ATT&CK dataset.")

        if not raw_data["objects"]:
            raise ValueError("MITRE ATT&CK dataset contains no objects.") 
        
        # Save the validated file
        temp_path.replace(RAW_DATASET_PATH)
        print("Dataset downloaded successfully.")

    except (urllib.error.URLError, OSError, ValueError, json.JSONDecodeError) as error:
        temp_path.unlink(missing_ok=True)
        raise RuntimeError(f"Dataset download failed: {error}") from error
    
    print(f'Saved to:  {RAW_DATASET_PATH}')


def load_dataset():
    '''Load the MITRE ATT&CK dataset into Python'''

    # Download dataset only if missing
    if not RAW_DATASET_PATH.exists():
        download_dataset()
    else:
        print('Dataset already exists locally')

    # Load JSON into Python
    with open (RAW_DATASET_PATH, 'r', encoding='utf-8') as file: 
        raw_data = json.load(file)

    print ('Dataset loaded successfully')
    return raw_data

