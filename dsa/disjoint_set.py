"""
dsa/disjoint_set.py - Disjoint Set Union (Union-Find)
Implemented from scratch with Union by Rank and Path Compression.

Classes:
1. DisjointSet: Near O(1) amortized set partition data structure.
"""

from typing import Any, List, Dict, Optional, Set


class DisjointSet:
    """
    Disjoint-Set (Union-Find) with Path Compression and Union by Rank.
    
    Purpose:
        1. Powers 'Product variants / same-family grouping' (e.g., color/size variants).
        2. Cycle detection in Kruskal's Minimum Spanning Tree algorithm.
    Operations:
        - make_set(x): O(1)
        - find(x): O(alpha(N)) amortized with path compression (Ackermann inverse <= 4).
        - union(x, y): O(alpha(N)) amortized with union by rank.
        - connected(x, y): O(alpha(N))
    """

    def __init__(self):
        # We use dicts here strictly as key-to-index storage, with list/tree logic for parents & ranks
        self.parent: Dict[Any, Any] = {}
        self.rank: Dict[Any, int] = {}
        self.operations_count = 0

    def make_set(self, x: Any) -> None:
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0

    def find(self, x: Any) -> Any:
        """Finds representative with two-pass Path Compression."""
        if x not in self.parent:
            self.make_set(x)

        self.operations_count += 1
        root = x
        while self.parent[root] != root:
            root = self.parent[root]

        # Path compression: point all ancestors directly to root
        curr = x
        while curr != root:
            nxt = self.parent[curr]
            self.parent[curr] = root
            curr = nxt

        return root

    def union(self, x: Any, y: Any) -> bool:
        """Merges sets containing x and y using Union by Rank."""
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False  # Already in same set (cycle)

        # Attach smaller rank tree under root of higher rank tree
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        return True

    def connected(self, x: Any, y: Any) -> bool:
        return self.find(x) == self.find(y)

    def get_components(self) -> Dict[Any, List[Any]]:
        """Groups all elements by their canonical set representative."""
        components: Dict[Any, List[Any]] = {}
        for elem in self.parent:
            root = self.find(elem)
            if root not in components:
                components[root] = []
            components[root].append(elem)
        return components

    def to_dict(self) -> Dict[str, Any]:
        comps = self.get_components()
        return {
            "type": "DisjointSet",
            "total_elements": len(self.parent),
            "num_components": len(comps),
            "operations_count": self.operations_count,
            "components": [
                {"representative": root, "members": members, "size": len(members)}
                for root, members in comps.items()
            ]
        }
