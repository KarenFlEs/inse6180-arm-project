from src import data_loader, data_exploration, data_preprocessing

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

    

    # 4. Run association rule mining
    print("\n4. Running association rule mining...")


    print("\n========== Project executed successfully ==========")


if __name__ == "__main__":
    main()
