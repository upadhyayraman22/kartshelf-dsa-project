"""
dsa/btree.py - B-Tree & B+ Tree Data Structures
Implemented from scratch for multi-way indexing and external storage simulation.

Classes:
1. BTree: Balanced multi-way search tree with configurable minimum degree t.
2. BPlusTree: B+ Tree with leaf node linked-list for optimal range scans.
"""

from typing import Any, List, Optional, Tuple, Dict


class BTreeNode:
    def __init__(self, leaf: bool = True):
        self.leaf = leaf
        self.keys: List[Any] = []
        self.values: List[Any] = []
        self.children: List['BTreeNode'] = []


class BTree:
    """
    B-Tree of configurable minimum degree t.
    
    Properties:
        Every node except root has at least (t - 1) keys.
        Every node has at most (2t - 1) keys and 2t children.
        All leaves are at the exact same depth.
    Operations:
        - insert(key, value): O(t * log_t N)
        - search(key): O(log_t N)
        - delete(key): O(t * log_t N)
    """

    def __init__(self, t: int = 2):
        if t < 2:
            raise ValueError("Minimum degree t must be >= 2")
        self.t = t
        self.root = BTreeNode(leaf=True)
        self.size = 0

    def search(self, key: Any, node: Optional[BTreeNode] = None) -> Optional[Any]:
        if node is None:
            node = self.root

        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and key == node.keys[i]:
            return node.values[i]

        if node.leaf:
            return None

        return self.search(key, node.children[i])

    def _split_child(self, parent: BTreeNode, i: int) -> None:
        t = self.t
        full_child = parent.children[i]
        new_child = BTreeNode(leaf=full_child.leaf)

        # Middle key goes to parent
        mid_key = full_child.keys[t - 1]
        mid_val = full_child.values[t - 1]

        # Right half keys/values go to new_child
        new_child.keys = full_child.keys[t:]
        new_child.values = full_child.values[t:]
        full_child.keys = full_child.keys[:t - 1]
        full_child.values = full_child.values[:t - 1]

        if not full_child.leaf:
            new_child.children = full_child.children[t:]
            full_child.children = full_child.children[:t]

        parent.children.insert(i + 1, new_child)
        parent.keys.insert(i, mid_key)
        parent.values.insert(i, mid_val)

    def _insert_non_full(self, node: BTreeNode, key: Any, value: Any) -> None:
        i = len(node.keys) - 1
        if node.leaf:
            # Check if key already exists
            for idx, k in enumerate(node.keys):
                if k == key:
                    node.values[idx] = value
                    return

            # Insert in sorted order
            node.keys.append(None)
            node.values.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                node.values[i + 1] = node.values[i]
                i -= 1
            node.keys[i + 1] = key
            node.values[i + 1] = value
            self.size += 1
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == (2 * self.t - 1):
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
                elif key == node.keys[i]:
                    node.values[i] = value
                    return
            self._insert_non_full(node.children[i], key, value)

    def insert(self, key: Any, value: Any) -> None:
        root = self.root
        if len(root.keys) == (2 * self.t - 1):
            new_root = BTreeNode(leaf=False)
            new_root.children.append(root)
            self._split_child(new_root, 0)
            self.root = new_root
            self._insert_non_full(new_root, key, value)
        else:
            self._insert_non_full(root, key, value)

    def delete(self, key: Any) -> bool:
        """Educational B-Tree deletion."""
        # Simple deletion supporting leaf and basic internal removals
        def _delete_from_node(node: BTreeNode, k: Any) -> bool:
            i = 0
            while i < len(node.keys) and k > node.keys[i]:
                i += 1
            if i < len(node.keys) and node.keys[i] == k:
                if node.leaf:
                    node.keys.pop(i)
                    node.values.pop(i)
                    self.size -= 1
                    return True
                else:
                    # Replace with predecessor from left child
                    pred_child = node.children[i]
                    while not pred_child.leaf:
                        pred_child = pred_child.children[-1]
                    pred_key = pred_child.keys[-1]
                    pred_val = pred_child.values[-1]
                    node.keys[i] = pred_key
                    node.values[i] = pred_val
                    return _delete_from_node(node.children[i], pred_key)
            elif not node.leaf:
                return _delete_from_node(node.children[i], k)
            return False

        return _delete_from_node(self.root, key)

    def to_tree_dict(self, node: Optional[BTreeNode] = None) -> Dict[str, Any]:
        if node is None:
            node = self.root
        return {
            "name": f"Keys: {node.keys}",
            "keys": node.keys,
            "values": node.values,
            "is_leaf": node.leaf,
            "children": [self.to_tree_dict(c) for c in node.children]
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "BTree",
            "t": self.t,
            "size": self.size,
            "tree": self.to_tree_dict()
        }


class BPlusNode:
    def __init__(self, leaf: bool = True):
        self.leaf = leaf
        self.keys: List[Any] = []
        # In leaf: values contains actual records
        # In internal node: children contains pointers to BPlusNode
        self.values: List[Any] = []
        self.children: List['BPlusNode'] = []
        self.next_leaf: Optional['BPlusNode'] = None  # Pointer to next leaf


class BPlusTree:
    """
    B+ Tree with linked leaf nodes for rapid range queries.
    
    Purpose:
        Powers 'Price range scans' and simulates database index structures (e.g., MySQL InnoDB).
    Properties:
        - Internal nodes only route searches.
        - All actual data is stored in the leaf nodes.
        - Leaf nodes form a singly linked list (self.next_leaf).
    Range Query:
        O(log_M N + K) by descending to initial leaf and walking the linked list.
    """

    def __init__(self, order: int = 4):
        if order < 3:
            raise ValueError("B+ Tree order must be >= 3")
        self.order = order
        self.root = BPlusNode(leaf=True)
        self.size = 0

    def search(self, key: Any) -> Optional[Any]:
        curr = self.root
        while not curr.leaf:
            i = 0
            while i < len(curr.keys) and key >= curr.keys[i]:
                i += 1
            curr = curr.children[i]

        for i, k in enumerate(curr.keys):
            if k == key:
                return curr.values[i]
        return None

    def insert(self, key: Any, value: Any) -> None:
        def _insert_in_leaf(leaf: BPlusNode, k: Any, v: Any):
            i = 0
            while i < len(leaf.keys) and leaf.keys[i] < k:
                i += 1
            if i < len(leaf.keys) and leaf.keys[i] == k:
                leaf.values[i] = v
                return
            leaf.keys.insert(i, k)
            leaf.values.insert(i, v)
            self.size += 1

        def _split_leaf(leaf: BPlusNode) -> Tuple[BPlusNode, Any]:
            mid = len(leaf.keys) // 2
            new_leaf = BPlusNode(leaf=True)
            new_leaf.keys = leaf.keys[mid:]
            new_leaf.values = leaf.values[mid:]
            leaf.keys = leaf.keys[:mid]
            leaf.values = leaf.values[:mid]

            # Connect linked list
            new_leaf.next_leaf = leaf.next_leaf
            leaf.next_leaf = new_leaf
            return new_leaf, new_leaf.keys[0]

        # Top-down or recursive insert
        def _insert(node: BPlusNode, k: Any, v: Any) -> Optional[Tuple[BPlusNode, Any]]:
            if node.leaf:
                _insert_in_leaf(node, k, v)
                if len(node.keys) >= self.order:
                    return _split_leaf(node)
                return None

            # Internal node: navigate to child
            i = 0
            while i < len(node.keys) and k >= node.keys[i]:
                i += 1

            split_res = _insert(node.children[i], k, v)
            if split_res is not None:
                new_child, split_key = split_res
                # Insert split_key into internal node
                node.keys.insert(i, split_key)
                node.children.insert(i + 1, new_child)

                if len(node.keys) >= self.order:
                    # Split internal node
                    mid = len(node.keys) // 2
                    up_key = node.keys[mid]
                    new_internal = BPlusNode(leaf=False)
                    new_internal.keys = node.keys[mid + 1:]
                    new_internal.children = node.children[mid + 1:]
                    node.keys = node.keys[:mid]
                    node.children = node.children[:mid + 1]
                    return new_internal, up_key

            return None

        split_root = _insert(self.root, key, value)
        if split_root is not None:
            new_child, split_key = split_root
            new_root = BPlusNode(leaf=False)
            new_root.keys = [split_key]
            new_root.children = [self.root, new_child]
            self.root = new_root

    def range_query(self, min_key: Any, max_key: Any) -> List[Any]:
        """
        Ultra-fast range query using linked leaves!
        Time Complexity: O(log N + K) where K is matching keys.
        """
        curr = self.root
        while not curr.leaf:
            i = 0
            while i < len(curr.keys) and min_key >= curr.keys[i]:
                i += 1
            curr = curr.children[i]

        results = []
        leaf: Optional[BPlusNode] = curr
        done = False
        while leaf and not done:
            for i, k in enumerate(leaf.keys):
                if k > max_key:
                    done = True
                    break
                if k >= min_key:
                    results.append(leaf.values[i])
            leaf = leaf.next_leaf

        return results

    def to_tree_dict(self, node: Optional[BPlusNode] = None) -> Dict[str, Any]:
        if node is None:
            node = self.root
        return {
            "name": f"Keys: {node.keys}" + (" (Leaf)" if node.leaf else " (Index)"),
            "keys": node.keys,
            "is_leaf": node.leaf,
            "children": [self.to_tree_dict(c) for c in node.children] if not node.leaf else []
        }

    def to_dict(self) -> Dict[str, Any]:
        # Collect leaf linked chain
        chain = []
        curr = self.root
        while curr and not curr.leaf:
            curr = curr.children[0]
        while curr:
            chain.append({"keys": curr.keys, "values_count": len(curr.values)})
            curr = curr.next_leaf

        return {
            "type": "BPlusTree",
            "order": self.order,
            "size": self.size,
            "tree": self.to_tree_dict(),
            "leaf_chain": chain
        }
