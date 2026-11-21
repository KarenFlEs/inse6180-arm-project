from src import data_loader, data_exploration, data_preprocessing, evaluation

def main():
    print("\n========== MITRE ATT&CK ARM PROJECT ==========")

    # Load MITRE ATT&CK dataset
    print("\n1. Loading MITRE ATT&CK dataset...")
    raw_data = data_loader.load_dataset()

    # 2. Explore dataset
    print("\n2. Exploring dataset...")
    data_exploration.info_dataset(raw_data)

    # 3. Preprocess dataset
    print("\n3. Preprocessing dataset...")
    transactions = data_preprocessing.preprocess_dataset(raw_data)
    print("Preprocessing completed!")
    print("Number of transactions:", len(transactions))

    # 4. Extract techniques only
    print("\n4. Extracting ATT&CK techniques...")
    technique_transactions = data_preprocessing.extract_techniques(transactions)
    print("Technique extraction completed!")

    # 5. Run association rule mining
    print("\n5. Running association rule mining...")
    support_thresholds = [0.05, 0.15, 0.25, 0.35, 0.45]
    results = evaluation.run_experiments(technique_transactions, support_thresholds)

    print("\n========== Project executed successfully ==========")


if __name__ == "__main__":
    main()
