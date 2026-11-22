from matplotlib import pyplot
from pathlib import Path
import seaborn as sns
import pandas as pd

def prepare_execution_time_data(results):
    execution_time_data = [
        {"min_support": result ["min_support"],
        "apriori_avg_time": result ["apriori"]['average_time'],
        "apriori_std": result ["apriori"]['std_deviation'],
        "fp_growth_avg_time": result ["fp_growth"]['average_time'],
        "fp_growth_std": result ["fp_growth"]['std_deviation']}
        for result in results
        if result.get("apriori") and result.get("fp_growth")
    ]
    
    return execution_time_data

def prepare_itemset_data(results):
    itemset_data = [
        {"min_support": result["min_support"],
        "apriori_frequent_itemsets": result ["apriori"]['number_of_itemsets'],
        "fp_growth_frequent_itemsets": result ["fp_growth"]['number_of_itemsets']}
        for result in results
        if result.get("apriori") and result.get("fp_growth")
    ]
    return itemset_data

def prepare_rule_data(results):
    rule_data = [
        {"min_support": result["min_support"],
        "apriori_rules": len(result ["apriori_rules"]),
        "fp_growth_rules": len(result ["fp_growth_rules"]),
        "apriori_filtered_rules": len(result ["apriori_filtered_rules"]),
        "fp_growth_filtered_rules": len(result ["fp_growth_filtered_rules"])}
        for result in results
    ]
    return rule_data

def prepare_rule_metrics_data(results):
    rule_metrics_data = []

    for result in results:
        for algorithm in ["apriori", "fp_growth"]:
            filtered_rules = result[f"{algorithm}_filtered_rules"]

            for rule in filtered_rules:
                rule_metrics_data.append({
                    "min_support": result["min_support"],
                    "algorithm": algorithm,
                    "antecedent": rule["antecedent"],
                    "consequent": rule["consequent"],
                    "support": rule["support"],
                    "confidence": rule["confidence"],
                    "lift": rule["lift"]
                })

    return rule_metrics_data



def plot_execution_time(data):
    return 0

def plot_frequent__itemsets(data):
    return 0

def plot_association_rules(data):
    return 0

def confidence_vs_list(data):
    return 0

def plot_rule_support(data):
    return 0

def visualize_results(results): 
    return 0