'''Investigate the structure of the dataset to understand its objects, distributions and relationships.'''

import data_loader
from collections import Counter

raw_data = data_loader.load_dataset()

# [Adversary (Intrusion Set) - Techniques associated]
# Understand the overall dataset structure
def info_dataset(raw_data):
    print("\n========== DATASET OVERVIEW ==========")
    print('Raw Data Keys: ', raw_data.keys())
    objects = raw_data.get("objects", [])
    print("Total number of objects:", len(objects))

    if objects:
        print('\nExample object structure: ')
        print(objects[0].keys())

    # Investigate the distribution of STIX Objects 
    print("\n========== OBJECT DISTRIBUTION ==========")
    object_types = Counter(
        obj.get("type") for obj in objects
    )
    for obj_type, count in object_types.most_common():
        print(f"{obj_type}: {count}")

    # Identify relevant objects for ARM
    print("\n========== RELEVANT OBJECTS ==========")
    intrusion_sets = {
        obj["id"]: obj
        for obj in objects
        if obj.get("type") == "intrusion-set"
        and obj.get("id")
    }

    attack_patterns = {
        obj["id"]: obj
        for obj in objects
        if obj.get("type") == "attack-pattern"
        and obj.get("id")
    }

    relationships = [
        obj for obj in objects
        if obj.get("type") == "relationship"
    ]

    print("Intrusion sets:", len(intrusion_sets))
    print("Attack patterns:", len(attack_patterns))
    print("Total relationships:", len(relationships))

    # Investigate revoked and deprecated objects
    print("\n========== OBJECT STATUS ==========")
    print("Revoked objects:", sum(obj.get("revoked", False) for obj in objects))
    print("Deprecated objects:", sum(obj.get("x_mitre_deprecated", False) for obj in objects))
    
    # Investigate relationships between groups and techniques
    print("\n========== GROUP-TECHNIQUE RELATIONSHIPS ==========")
    group_technique_relationships = []

    for rel in relationships:
        # Only focused in relationships that uses techniques
        if rel.get("relationship_type") != "uses":
            continue

        source = intrusion_sets.get(rel.get("source_ref"))
        target = attack_patterns.get(rel.get("target_ref"))

        if source and target:
            group_technique_relationships.append(rel)

    print("Number of [Intrusion set]-[Technique] relationships:", len(group_technique_relationships))

    # Count unique group-techniques associations
    unique_pairs = {
        (rel["source_ref"], rel["target_ref"])
        for rel in group_technique_relationships
    }
    print("Number of unique group-technique pairs:", len(unique_pairs))

    # Display and example relationshhip
    print("\n========== EXAMPLE RELATIONSHIP ==========")
    rel = group_technique_relationships[0]
    group = intrusion_sets[rel["source_ref"]]
    technique = attack_patterns[rel["target_ref"]]
        
    group_external_ids = [
        ref.get("external_id")
        for ref in group.get("external_references", [])
        if ref.get("external_id")
    ]
    technique_external_ids = [
        ref.get("external_id")
        for ref in technique.get("external_references", [])
        if ref.get("external_id")
    ]
    print("\nIntrusion Set:")
    print("  Name:", group.get("name"))
    print("  STIX ID:", group.get("id"))
    print("  MITRE ID:", group_external_ids)
    
    print("Attack Pattern:")
    print("  Name:", technique.get("name"))
    print("  STIX ID:", technique.get("id"))
    print("  MITRE ID:", technique_external_ids)

    print("Relationship Type:", rel.get("relationship_type"))

   
info_dataset(raw_data)