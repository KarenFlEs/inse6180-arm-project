'''Implement FP_Growth Algorithm'''

from collections import Counter 

class Node:
    def _init(self, item, parent=None):
        self.item = item
        self.count = 1
        self.parent = parent
        self.children = {}
        self.link = None

class FPTree:
    def _init_(self, data, minsup):
        self.root = Node(None, 0, None)
        self.minsup = minsup
        self.header_table = {}
        self.build_tree(data)

    def build_tree(self, data):
        # Count items, remove infrequent ones 
        # Build header table 
        # Sort data and insert 
        counts = Counter() 
        for d in data:
            counts.update(set(d))

        # Keep only frequent items 
        frequent = {
            item: count
            for item, count in counts.item()
            if count >= self.minsup
        }
    
        frequent = dict(sorted(frequent.items(), key=lambda x: x[1], reverse=True))
        return 0

    # Insert data transactions into FPTree
    def insert_node(root, node):
        current = root
        for item in node:
            # If a cild already exists, imcrement its count. Otherwise, create a new one 
            if item in current.children:
                current.children[item].count += 1
            else:
                new_node = Node(item, current)
                current.children[item] = new_node
            current = current.children[item]


def get_prefix_path(node):
    # Retrieve prefix path 
    path = []
    current = node.parent

    while current is not None and current.item != "ROOT":
        path.append(current.item)
        current = current.parent

    return path[::-1]

def mine_tree(tree, minsup, prefix, patterns):
    # Recursively mine frequent itemsets 
    return 0

def fp_growth(data, minsup):
    return 0

