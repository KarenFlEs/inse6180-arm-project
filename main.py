from src.data_loader import load_dataset

def main():

    # Load MITRE ATT&CK dataset
    raw_data = load_dataset()

    # Display basic dataset information
    print(f"\nNumber of objects: {len(raw_data['objects'])}")

    print("\nProject executed successfully.")


if __name__ == "__main__":
    main()
