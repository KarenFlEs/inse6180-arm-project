'''
Preprocess the MITRE ATT&CK Dataset 
and convert it into Transactions for ARM

Each intrusion set (group) represents a transaction
containing the attack techniques associated with that group 
'''

import data_loader

raw_data = data_loader.load_dataset()

# Extract Relevant STIX Objects
def extract_relevant_objects(raw_data):
    objects = raw_data.get('objects', [])

    # Intrusion Sets represent Threat Groups  
    intrusion_sets = {
        obj["id"]: obj
        for obj in objects
        if obj.get("type") == "intrusion-set"
        and not obj.get("revoked", False)
        and not obj.get("x_mitre_deprecated", False)
        and obj.get("id")
    }

    # Attack Patterns represent Attack Techniques
    attack_patterns = {
        obj["id"]: obj
        for obj in objects
        if obj.get("type") == "attack-pattern"
        and not obj.get("revoked", False)
        and not obj.get("x_mitre_deprecated", False)
        and obj.get("id")
    }

    # Relationnships: Connects Threat Groups to Attack Techniques
    relationships = [
        obj for obj in objects
        if obj.get("type") == "relationship"
        and not obj.get("revoked", False)
        and not obj.get("x_mitre_deprecated", False)
    ]

    return intrusion_sets, attack_patterns, relationships

# Extract Group-to-technique relationships 
def extract_group_technique_relationships(intrusion_sets, attack_patterns, relationships):
    group_technique_relationships = []
    
    for rel in relationships:
        if rel.get("relationship_type") != "uses":
            continue

        source_ref = rel.get("source_ref") # Src = Intrusion_Set 
        target_ref = rel.get("target_ref") # Tar = Attack_Pattern 

        if source_ref in intrusion_sets and target_ref in attack_patterns:
            group_technique_relationships.append(rel)
    
    return group_technique_relationships

# Create ARM Transactions
def create_transactions(intrusion_sets, attack_patterns, group_technique_relationships):
    transactions = []

    # Each key is an intrusion set ID and the values as the techniques used 
    group_techniques = {
        group_id: set()
        for group_id in intrusion_sets
    }

    for rel in group_technique_relationships:
        group_id = rel.get("source_ref")
        attack_pattern_id = rel.get("target_ref")

        # Extract the MITRE Technique external ID
        attack_pattern = attack_patterns.get(attack_pattern_id)

        # Skip missing attack patterns
        if not attack_pattern:
            continue

        for ref in attack_pattern.get("external_references", []):
            if ref.get("source_name") == "mitre-attack" and ref.get("external_id"):
                technique_external_id = ref.get("external_id")

                # Associate the technique with its group
                group_techniques[group_id].add(technique_external_id)
                break # No need to keep searching for further references

    # Keep only groups that have at least one technique (ARM does not need empty sets)
    transactions = []

    for group_id, techniques in group_techniques.items():

        if techniques:
            group_name = intrusion_sets[group_id].get("name")

            transactions.append({
                "group_id": group_id,
                "group_name": group_name,
                "techniques": sorted(techniques)
            })
    return transactions


# 4. Execute the preprocessing pipeline
intrusion_sets, attack_patterns, relationships = extract_relevant_objects(raw_data)
group_technique_relationships = extract_group_technique_relationships(intrusion_sets,attack_patterns,relationships)
transactions = create_transactions(intrusion_sets,attack_patterns,group_technique_relationships)


# 5. Display preprocessing results
print("\n========== PREPROCESSING RESULTS ==========")

# Extract unique techniques
unique_techniques = {
    technique
    for transaction in transactions
    for technique in transaction["techniques"]
}

# Identify groups without techniques
groups_with_transactions = {
    transaction["group_id"]
    for transaction in transactions
}

empty_groups = [
    group_id
    for group_id in intrusion_sets
    if group_id not in groups_with_transactions
]

# Display dataset statistics
print("Number of intrusion sets:", len(intrusion_sets))
print("Number of attack patterns:", len(attack_patterns))
print("Number of valid group-technique relationships:",
      len(group_technique_relationships))

# Display transaction statistics
print("\n========== TRANSACTION VALIDATION ==========")

print("Number of non-empty transactions:", len(transactions))
print("Number of empty groups:", len(empty_groups))
print("Number of unique techniques:", len(unique_techniques))

# Display example transactions
print("\n========== EXAMPLE TRANSACTIONS ==========")

for i, transaction in enumerate(transactions[:5], start=1):
    print(f"\nTransaction {i}")
    print("Group ID:", transaction["group_id"])
    print("Group Name:", transaction["group_name"])
    print("Number of techniques:", len(transaction["techniques"]))
    print("Techniques:", transaction["techniques"])
