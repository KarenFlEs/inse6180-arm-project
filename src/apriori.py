'''Implement Apriori Algorithm'''

from itertools import combinations

def apriori (db, minsup):
    """
    Apriori algorithm.

    Parameters:
        db: List of transactions (each transaction is a set of items).
        minsup: Minimum support threshold (between 0 and 1).

    Returns:
        Dictionary containing frequent itemsets and their support.
    """
    if not db:
        return {}

    # Find frequent 1-itemsets
    items = set (item for t in db for item in t)
    L = {}

    for item in items:
        support = sum(item in t for t in db) / len(db)
        if support >= minsup:
            L[frozenset([item])] = support

    frequent = L.copy()
    k = 1

    while L:
        # Generatye candidates 
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

        # Calculate support
        L_next = {}

        for candidate in candidates:
            support = sum(candidate.issubset(t) for t in db) / len(db)
            if support >= minsup:
                L_next[candidate] = support

        L = L_next
        frequent.update(L)
        k += 1

    return frequent