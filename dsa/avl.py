"""
dsa/avl.py - AVL (Adelson-Velsky and Landis) Self-Balancing Tree
Implemented from scratch with LL, RR, LR, RL rotations and rotation counters.

Classes:
1. AVLNode: Node with height tracking.
2. AVLTree: Self-balancing BST guaranteeing O(log N) worst-case time complexity.
"""

from typing import Any, List, Optional, Tuple, Dict


class AVLNode:
    def __init__(self, key: Any, value: Any = None):
        self.key = key
        self.value = value
        self.height: int = 1
        self.left: Optional['AVLNode'] = None
        self.right: Optional['AVLNode'] = None


class AVLTree:
    """
    AVL Self-Balancing Binary Search Tree.
    
    Purpose:
        Powers fast 'Product lookup by ID' with guaranteed O(log N) search.
    Properties:
        Balance Factor = height(left) - height(right) in {-1, 0, 1}.
    Rotations:
        - LL: Right rotation at root when left child is left-heavy.
        - RR: Left rotation at root when right child is right-heavy.
        - LR: Left rotation on left child, then Right rotation on root.
        - RL: Right rotation on right child, then Left rotation on root.
    Complexities:
        Search: O(log N) guaranteed.
        Insert: O(log N) with at most 1 rotation (or double rotation).
        Delete: O(log N) with up to O(log N) rotations along path to root.
        Space: O(N).
    """

    def __init__(self):
        self.root: Optional[AVLNode] = None
        self.node_count = 0
        self.rotations = {
            "LL": 0,
            "RR": 0,
            "LR": 0,
            "RL": 0,
            "total": 0
        }

    def _height(self, node: Optional[AVLNode]) -> int:
        if node is None:
            return 0
        return node.height

    def _balance_factor(self, node: Optional[AVLNode]) -> int:
        if node is None:
            return 0
        return self._height(node.left) - self._height(node.right)

    def _update_height(self, node: AVLNode) -> None:
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _rotate_right(self, y: AVLNode) -> AVLNode:
        r"""
        Right rotation (LL case):
               y                     x
              / \                   / \
             x   T3   ===>         T1  y
            / \                       / \
           T1  T2                    T2  T3
        """
        x = y.left
        assert x is not None
        t2 = x.right

        # Perform rotation
        x.right = y
        y.left = t2

        # Update heights
        self._update_height(y)
        self._update_height(x)

        return x

    def _rotate_left(self, x: AVLNode) -> AVLNode:
        r"""
        Left rotation (RR case):
             x                         y
            / \                       / \
           T1  y        ===>         x   T3
              / \                   / \
             T2  T3                T1  T2
        """
        y = x.right
        assert y is not None
        t2 = y.left

        # Perform rotation
        y.left = x
        x.right = t2

        # Update heights
        self._update_height(x)
        self._update_height(y)

        return y

    def insert(self, key: Any, value: Any = None) -> None:
        def _insert(node: Optional[AVLNode], k: Any, v: Any) -> AVLNode:
            if node is None:
                self.node_count += 1
                return AVLNode(k, v)

            if k < node.key:
                node.left = _insert(node.left, k, v)
            elif k > node.key:
                node.right = _insert(node.right, k, v)
            else:
                # Update existing value
                node.value = v
                return node

            self._update_height(node)
            balance = self._balance_factor(node)

            # Left Left Case
            if balance > 1 and self._balance_factor(node.left) >= 0:
                self.rotations["LL"] += 1
                self.rotations["total"] += 1
                return self._rotate_right(node)

            # Left Right Case
            if balance > 1 and self._balance_factor(node.left) < 0:
                self.rotations["LR"] += 1
                self.rotations["total"] += 1
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)

            # Right Right Case
            if balance < -1 and self._balance_factor(node.right) <= 0:
                self.rotations["RR"] += 1
                self.rotations["total"] += 1
                return self._rotate_left(node)

            # Right Left Case
            if balance < -1 and self._balance_factor(node.right) > 0:
                self.rotations["RL"] += 1
                self.rotations["total"] += 1
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)

            return node

        self.root = _insert(self.root, key, value)

    def search(self, key: Any) -> Optional[Any]:
        curr = self.root
        while curr:
            if key == curr.key:
                return curr.value
            elif key < curr.key:
                curr = curr.left
            else:
                curr = curr.right
        return None

    def delete(self, key: Any) -> bool:
        deleted = False

        def _min_value_node(node: AVLNode) -> AVLNode:
            curr = node
            while curr.left is not None:
                curr = curr.left
            return curr

        def _delete(node: Optional[AVLNode], k: Any) -> Optional[AVLNode]:
            nonlocal deleted
            if node is None:
                return None

            if k < node.key:
                node.left = _delete(node.left, k)
            elif k > node.key:
                node.right = _delete(node.right, k)
            else:
                deleted = True
                if node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left

                temp = _min_value_node(node.right)
                node.key = temp.key
                node.value = temp.value
                node.right = _delete(node.right, temp.key)

            if node is None:
                return None

            self._update_height(node)
            balance = self._balance_factor(node)

            # Left Left
            if balance > 1 and self._balance_factor(node.left) >= 0:
                self.rotations["LL"] += 1
                self.rotations["total"] += 1
                return self._rotate_right(node)

            # Left Right
            if balance > 1 and self._balance_factor(node.left) < 0:
                self.rotations["LR"] += 1
                self.rotations["total"] += 1
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)

            # Right Right
            if balance < -1 and self._balance_factor(node.right) <= 0:
                self.rotations["RR"] += 1
                self.rotations["total"] += 1
                return self._rotate_left(node)

            # Right Left
            if balance < -1 and self._balance_factor(node.right) > 0:
                self.rotations["RL"] += 1
                self.rotations["total"] += 1
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)

            return node

        self.root = _delete(self.root, key)
        if deleted:
            self.node_count -= 1
        return deleted

    def to_tree_dict(self, node: Optional[AVLNode] = None, is_root: bool = True) -> Optional[Dict[str, Any]]:
        if is_root:
            node = self.root
        if node is None:
            return None
        return {
            "name": f"ID #{node.key}",
            "key": node.key,
            "value": str(node.value) if node.value is not None else None,
            "height": node.height,
            "balance": self._balance_factor(node),
            "children": [
                c for c in [
                    self.to_tree_dict(node.left, False),
                    self.to_tree_dict(node.right, False)
                ] if c is not None
            ]
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "AVLTree",
            "node_count": self.node_count,
            "height": self._height(self.root),
            "rotations": self.rotations,
            "tree": self.to_tree_dict()
        }
