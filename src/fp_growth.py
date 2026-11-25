'''Implement FP-Growth Algorithm'''

from collections import Counter 
import math

class Node:
    def __init__(self, item, parent=None):
        self.item = item
        self.count = 1
        self.parent = parent
        self.children = {}
        self.link = None

class FPTree:
    def __init__(self, data, minsup, weights=None):
        self.root = Node("ROOT")
        self.root.count = 0
        self.minsup = minsup
        self.header_table = {}
        self.build_tree(data, weights)

    def build_tree(self, data, weights=None):
        """Build the FP-Tree and its header table."""
        if weights is None:
            weights = [1] * len(data)

        # Count items, remove infrequent ones 
        counts = Counter() 
        for transaction, weight in zip(data, weights):
            for item in set(transaction):
                counts[item] += weight

        # Keep only frequent items 
        frequent = {
            item: count
            for item, count in counts.items()
            if count >= self.minsup
        }

        # Build header table 
        self.header_table = {
            item: [count, None, None] 
            for item, count in frequent.items()
        }

        # Sort transactions and insert them into the FPTree
        frequent = dict(sorted(frequent.items(), key=lambda x: (-x[1], x[0])))
        for transaction, weight in zip(data, weights):
            filtered = set(transaction) & frequent.keys()
            ordered = sorted(filtered, key=lambda x: (-frequent[x], x))
            self.insert_node(ordered, weight)


    def insert_node(self, transaction, weight=1):
        """Insert a transaction into the FP-Tree."""
        current = self.root

        for item in transaction:
            # Incremet an exisiting node or create a new one
            if item in current.children:
                current.children[item].count += weight
            else:
                new_node = Node(item, current)
                new_node.count = weight
                current.children[item] = new_node

                header = self.header_table[item]
                if header[1] is None:
                    header[1] = new_node
                else:
                    header[2].link = new_node

                header[2] = new_node

            current = current.children[item]


def get_prefix_path(node):
    """Retrieve te prefix path of a node"""
    path = []
    current = node.parent

    while current is not None and current.item != "ROOT":
        path.append(current.item)
        current = current.parent

    return path[::-1]

def mine_tree(tree, minsup, prefix, patterns):
    """Recursively mine frequent patterns from an FP-Tree."""

    # Iterate through the header table
    for item, info in tree.header_table.items():
        support_count = info[0]
        node = info[1]

        # Generate the new frequent pattern
        frequent_pattern = prefix | {item}
        patterns[frozenset(frequent_pattern)] = support_count

        # Build the conditional pattern base 
        conditional_pattern_base = []

        while node is not None:
            path = get_prefix_path(node)
            if path:
                conditional_pattern_base.append((path, node.count))

            node = node.link

        if conditional_pattern_base:
            conditional_data = [path for path, count in conditional_pattern_base]
            conditional_weights = [count for path, count in conditional_pattern_base]
            conditional_tree = FPTree(conditional_data, minsup, conditional_weights)

            # Recursively mine conditional tree
            if conditional_tree.header_table:
                mine_tree(conditional_tree, minsup, frequent_pattern, patterns)

    return patterns

def fp_growth(data, minsup):
    """Apply FP-Growth to identify frequent itemsets"""

    if not data:
        return {}
    
    # Convert relative support to absolute support for mining purpose
    abs_minsup = math.ceil(minsup * len(data))

    # Build initial FP-Tree
    tree = FPTree(data, abs_minsup)
    patterns = {}

    # Start mining
    mine_tree(tree, abs_minsup, set(), patterns)

    # Convert absolute support counts to relative support
    frequent_itemsets = {
        itemset: abs_support / len(data)
        for itemset, abs_support in patterns.items()
    }

    return frequent_itemsets

