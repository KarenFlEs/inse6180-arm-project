# INSE6180 Project: Association-Rule Mining for Cyber Threat Intelligence

## Overview

This project applies association rule mining to the MITRE ATT&CK Enterprise dataset to identify relationships between techniques used by threat groups. It implements and compares two algorithms: Apriori and FP-Growth.

Each intrusion set is treated as a transaction containing the attack techniques associated with it through MITRE ATT&CK `uses` relationships.

## Dataset

The project uses **MITRE ATT&CK Enterprise version 20.0** in STIX 2.1 JSON format.

- **Source:** [MITRE ATT&CK STIX Data](https://github.com/mitre-attack/attack-stix-data)
- **File:** `enterprise-attack-20.0.json`
- **Location:** `data/raw/`

The dataset is downloaded automatically if it is not already available locally. See [`data/README.md`](data/README.md) for more information.

## Algorithms

- **Apriori:** Identifies frequent itemsets by generating and testing candidate itemsets.
- **FP-Growth:** Uses an FP-Tree to mine frequent itemsets without candidate generation.

Both algorithms are applied to the same transaction data so their results and execution times can be compared.

## Experimental Configuration

The experiments use the following settings:

- **Minimum support:** 0.15, 0.20, 0.25, 0.30, and 0.35
- **Minimum confidence:** 0.60
- **Repetitions:** 10 runs per algorithm and support threshold

The project compares execution time, frequent itemsets, and generated association rules. Mean execution time and standard deviation are reported for each algorithm.

## Installation

1. Clone the repository and open the project directory:

   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Project

Run the main program from the project directory:

```bash
python main.py
```

**Note:** The program may take a few seconds to run while importing the required packages and executing both algorithms.

## Results and Visualizations

The program displays dataset information, preprocessing results, algorithm comparisons, and association rules in the console.

It also generates and saves the following visualizations in `results/figures/`:

- Execution time comparison
- Frequent itemsets comparison
- Association rules comparison
- Confidence vs. lift
- Top 10 association rules

## Project Structure

```text
.
├── data/
│   ├── README.md
│   └── raw/
├── results/
│   └── figures/
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── data_exploration.py
│   ├── data_preprocessing.py
│   ├── apriori.py
│   ├── fp_growth.py
│   ├── evaluation.py
│   └── visualization.py
├── main.py
├── requirements.txt
└── README.md
```

## Notes

- The raw dataset is not included in the repository. It is downloaded automatically when needed.
- Generated visualizations are saved in `results/figures/`.
- Association rules show co-occurrence patterns in the dataset; they do not establish causation or the order in which techniques are used.