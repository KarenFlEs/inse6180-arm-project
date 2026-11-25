# Dataset

This project uses the **MITRE ATT&CK Enterprise dataset, version 20.0**, in STIX 2.1 JSON format.

## Source

The dataset is obtained from the official MITRE ATT&CK GitHub repository:

https://github.com/mitre-attack/attack-stix-data

## Dataset File

- **Filename:** `enterprise-attack-20.0.json`
- **Location:** `data/raw/`
- **Format:** JSON (STIX 2.1)
- **Version:** 20.0

## Download

The dataset is automatically downloaded by `data_loader.py` if the local dataset file is not found.

Alternatively, it can be downloaded manually from the official MITRE ATT&CK repository and placed in the `data/raw/` directory.

## Usage

The dataset provides information about MITRE ATT&CK Enterprise intrusion sets, attack patterns, and relationships. This project uses these objects to construct transactions representing the techniques associated with each intrusion set for association rule mining using Apriori and FP-Growth.