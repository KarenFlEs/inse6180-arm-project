import apriori
import fp_growth
import time
import statistics
from itertools import combinations

def generate_association_rules(frequent_itemsets):
    # Generate rules from frequent itemsets
    rules = set()

    for itemset in frequent_itemsets:
        if len(itemset) < 2:
            continue

        # Generate subsets of different size 
        for size in range(1, len(itemset)):
            for subset in combinations(itemset, size):
                # Generate possible antecedents and its consequent
                antecedent = frozenset(subset)
                consequent = itemset - antecedent
                rules.add((antecedent, consequent))

    return rules

def evaluate_rules(rules, transactions):
    # Calculate support, confidence and lift
    if not transactions:
        raise ValueError("Transactions cannot be empty.")

    total_transactions = len(transactions)

    metrics = []

    for antecedent, consequent in rules:
        # Count transactions containing antecedent 
        count_antecedent = 0
        count_consequent = 0
        count_both = 0

        for transaction in transactions:
            has_antecedent = antecedent.issubset(transaction)
            has_consequent = consequent.issubset(transaction)

            if has_antecedent:
                count_antecedent += 1

            if has_consequent:
                count_consequent += 1

            if has_antecedent and has_consequent:
                count_both += 1

        support = count_both / total_transactions
        confidence = count_both / count_antecedent if count_antecedent > 0 else 0
        lift = confidence / (count_consequent / total_transactions) if count_consequent > 0 else 0

        metrics.append({
            "antecedent": antecedent,
            "consequent": consequent,
            "support": support,
            "confidence": confidence,
            "lift": lift
        })

    return metrics

# Filter association rules
def filter_rules(rule_metrics, min_confidence):
    filtered_rules = [
        rule for rule in rule_metrics
        if rule["confidence"] >= min_confidence
    ]

    return filtered_rules


# Normalize frequent itemsets
def normalize_itemsets(itemsets, algorithm, total_transactions):
    if total_transactions == 0:
        raise ValueError("Transactions cannot be empty.")

    normalized = {}

    for itemset, value in itemsets.items():

        if algorithm == "apriori":
            support = value

        elif algorithm == "fp_growth":
            support = value / total_transactions

        else:
            raise ValueError("Unknown algorithm.")

        normalized[frozenset(itemset)] = support

    return normalized

#Compare frequent itemsets
def compare_itemsets(apriori_itemsets, fp_itemsets):
    # Check whether both algorithms discover the same frequent itemsets
    if set(apriori_itemsets) != set(fp_itemsets):
        return False

    # Compare support values
    for itemset in apriori_itemsets:
        if abs(apriori_itemsets[itemset] - fp_itemsets[itemset]) > 1e-9:
            return False

    return True

# Alorithm performance evaluation
def evaluation_algorithm(algorithm, transactions, min_support, algorithm_name, repetitions=5):
    if repetitions < 1:
        raise ValueError("Repetitions must be at least 1.")

    execution_times = []
    frequent_itemsets = None
    
    # Run algoritm and measure its performance
    for _ in range(repetitions):
        start_time = time.perf_counter()
        current_itemsets = algorithm(transactions, min_support)
        end_time = time.perf_counter()

        execution_times.append(end_time - start_time)
        frequent_itemsets = current_itemsets

    # Normalize frequent itemsets
    normalized_itemsets = normalize_itemsets(frequent_itemsets, algorithm_name, len(transactions))
    
    # Calculate average execution time
    average_time = statistics.mean(execution_times)

    # Calculate execution time standard deviation
    std_deviation = (statistics.stdev(execution_times) if repetitions > 1 else 0)

    algo_results = {
        "frequent_itemsets": normalized_itemsets,
        "number_of_itemsets": len(normalized_itemsets),
        "average_time": average_time,
        "std_deviation": std_deviation,
        "execution_times": execution_times
    }

    return algo_results

def run_experiments(transactions, support_thresholds, min_confidence=0.6, repetitions=5):
    if not transactions:
        raise ValueError("Transactions cannot be empty.")

    if not support_thresholds:
        raise ValueError("Support thresholds cannot be empty.")

    if not 0 <= min_confidence <= 1:
        raise ValueError("Confidence must be between 0 and 1.")

    if repetitions < 1:
        raise ValueError("Repetitions must be at least 1.")
    
    # Run both algorithms accross different minimum supports
    results = []

    for min_support in support_thresholds:
        if not 0 < min_support <= 1:
            raise ValueError("Support must be between 0 and 1.")

        apriori_results = evaluation_algorithm(apriori.apriori, transactions, min_support, "apriori", repetitions)
        fp_growth_results = evaluation_algorithm(fp_growth.fp_growth, transactions, min_support, "fp_growth", repetitions)

        # Compare frequent itemsets
        algorithms_agree = compare_itemsets(apriori_results["frequent_itemsets"], fp_growth_results["frequent_itemsets"])

        # Evaluate association rules
        apriori_rules = generate_association_rules(apriori_results["frequent_itemsets"])
        fp_growth_rules = generate_association_rules(fp_growth_results["frequent_itemsets"])

        apriori_metrics = evaluate_rules(apriori_rules, transactions)
        fp_growth_metrics = evaluate_rules(fp_growth_rules, transactions)

        # Filter rules using confidence
        apriori_filtered = filter_rules(apriori_metrics, min_confidence)
        fp_filtered = filter_rules(fp_growth_metrics, min_confidence)

        results.append({
            "min_support": min_support,
            "apriori": apriori_results,
            "fp_growth": fp_growth_results,
            "algorithms_agree": algorithms_agree,
            "apriori_rules": apriori_metrics,
            "fp_growth_rules": fp_growth_metrics,
            "apriori_filtered_rules": apriori_filtered,
            "fp_growth_filtered_rules": fp_filtered
        })

    return results


# Display Experimental Results
def display_results(results):
    print("\n========== EXPERIMENTAL RESULTS ==========")

    for result in results:
        print("\nMinimum support:", result["min_support"])

        # Display Apriori and FP-Growth results
        for algorithm_name in ["apriori", "fp_growth"]:
            algorithm_result = result[algorithm_name]
            
            rules = result[algorithm_name + "_rules"]
            filtered_rules = result[algorithm_name + "_filtered_rules"]

            print("\n---", algorithm_name.upper(), "---")
            print("Frequent itemsets:", algorithm_result["number_of_itemsets"])
            print("Average execution time:", f"{algorithm_result['average_time']:.8f}", "seconds")
            print("Execution time standard deviation:", f"{algorithm_result['std_deviation']:.8f}")
            print("Generated rules:", len(rules))
            print("Rules after confidence filtering:", len(filtered_rules))

        print("\nApriori and FP-Growth agree:", result["algorithms_agree"])


# Display Association Rules
def display_rules(results):
    print("\n========== ASSOCIATION RULES ==========")

    for result in results:
        print("\nMinimum support:", result["min_support"])

        for algorithm_name in ["apriori", "fp_growth"]:
            filtered_rules = result[algorithm_name + "_filtered_rules"]
            print("\n---", algorithm_name.upper(), "---")

            for rule in filtered_rules:
                print(f"\n{set(rule['antecedent'])} -> "f"{set(rule['consequent'])}")
                print(f"Support: {rule['support']:.4f}")
                print(f"Confidence: {rule['confidence']:.4f}")
                print(f"Lift: {rule['lift']:.4f}")


# Small test dataset
transactions = [
    {'A', 'B', 'C'},
    {'A', 'B'},
    {'A', 'C'},
    {'B', 'C'},
    {'A', 'B', 'C'}
]

# Experimental parameters
support_thresholds = [0.2, 0.4, 0.6, 0.8]
min_confidence = 0.6
repetitions = 5

# Run experiments
results = run_experiments(transactions, support_thresholds, min_confidence, repetitions)

# Display results
display_results(results)
display_rules(results)

# Validation
print("\n========== VALIDATION ==========")

assert len(transactions) == 5
assert len(results) == len(support_thresholds)

# Both algorithms should agree at every threshold
assert all(
    result["algorithms_agree"]
    for result in results
)

# Check the expected results at support 0.4
test_result = next(
    result for result in results
    if result["min_support"] == 0.4
)

assert test_result["apriori"]["number_of_itemsets"] == 7
assert test_result["fp_growth"]["number_of_itemsets"] == 7
assert len(test_result["apriori_rules"]) == 12
assert len(test_result["fp_growth_rules"]) == 12

# Test rule generation and evaluation independently
test_rules = {(frozenset({'A'}), frozenset({'B'}))}
metrics = evaluate_rules(test_rules, transactions)

assert abs(metrics[0]["support"] - 0.6) < 1e-9
assert abs(metrics[0]["confidence"] - 0.75) < 1e-9
assert abs(metrics[0]["lift"] - 0.9375) < 1e-9

print("All tests passed!")