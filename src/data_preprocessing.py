'''
Preprocess the MITRE ATT&CK Dataset 
and convert it into Transactions for ARM

Each intrusion set represents a transaction
containing the attack techniques associated with that group 
'''

import data_loader

raw_data = data_loader.load_dataset()

def extract_relevant_objects(raw_data):
    objects = raw_data.get('objects', [])

    intrusion_sets = {
        obj["id"]: obj
        for obj in objects
        if obj["type"] == "intrusion-set"
    }

    attack_patterns = {
        obj["id"]: obj
        for obj in objects
        if obj["type"] == "attack-pattern"
    }

    relationships = [
        obj for obj in objects
        if obj["type"] == "relationship"
    ]

    return intrusion_sets, attack_patterns, relationships

def extract_group_technique_relationships(intrusion_sets, attack_patterns, relationships):
    group_technique_relationships = []
    for rel in relationships:
        if rel.get("relationship_type") != "uses":
            continue

        source_ref = intrusion_sets.get(rel.get("source_ref"))
        target_ref = attack_patterns.get(rel.get("target_ref"))

        if source_ref in intrusion_sets and target_ref in attack_patterns:
            group_technique_relationships.append(rel)
    
    return group_technique_relationships

def create_transactions(intrusion_sets, attack_patterns, group_technique_relationships):
    transactions = []
    return transactions