import apriori
import fp_growth
import time

def generate_association_rules(frequent_itemsets):
    # Generate rules from frequent itemsets
    rules = []
    return rules

def evaluate_rules(rules, transactions):
    # Calculate support, confidence and lift
    metrics = []
    return metrics

def evaluation_algoritm(algorithm, transactions, min_support):
    # Run algoritm and measure its performance
    start_time = time.perf_counter()
    frequent_itemsets = algorithm(transactions, min_support)
    end_time = time.perf_counter

    execution_time = end_time - start_time
    algo_results = {
        "frequent_itemsets": frequent_itemsets,
        "execution_time": execution_time,
        "number_of_itemsets": len(frequent_itemsets)
    }
    return algo_results

def run_experiments(transactions, support_thresholds):
    # Run both algorithms accross different minimum supports
    results = []

    for min_support in support_thresholds:
        apriori_results = evaluation_algoritm(apriori.apriori(transactions, min_support), transactions, min_support)
        fp_growth_results = evaluation_algoritm(fp_growth.fp_growth(transactions, min_support), transactions, min_support)

    return results
