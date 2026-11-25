'''Implement Apriori Algorithm'''

from itertools import combinations

def apriori (data, minsup):
    """Apply Apriori algorithm to identify frequent itemsets"""
    if not data:
        return {}

    # Find frequent 1-itemsets
    items = set (item for transaction in data for item in transaction)
    L = {}

    for item in items:
        support = sum(item in transaction for transaction in data) / len(data)
        if support >= minsup:
            L[frozenset([item])] = support

    frequent = L.copy()
    k = 1

    while L:
        # Generate candidates 
        candidates = set()
        frequent_itemsets = list(L.keys())

        for i in range (len(frequent_itemsets)):
            for j in range(i + 1, len(frequent_itemsets)): 
                candidate = (frequent_itemsets[i] | frequent_itemsets[j])

                # Only generate candidates of size k+1
                if len(candidate) == k + 1:

                    # Prune candidates
                    if all(
                        frozenset(subset) in L
                        for subset in combinations(candidate, k)
                    ):
                        candidates.add(candidate)

        # Calculate support for candidate itemsets
        L_next = {}

        for candidate in candidates:
            support = sum(candidate.issubset(transaction) for transaction in data) / len(data)
            if support >= minsup:
                L_next[candidate] = support

        L = L_next
        frequent.update(L)
        k += 1

    return frequent


