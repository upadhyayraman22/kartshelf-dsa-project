"""
dsa/bst.py - Binary Search Tree & Threaded BST
Implemented from scratch without recursion shortcuts.

Classes:
1. BSTNode: Standard binary tree node.
2. BST: Binary Search Tree with recursive AND iterative traversals using explicit Stack.
3. ThreadedBST: Threaded Binary Search Tree enabling stackless, non-recursive inorder traversal.
"""

from typing import Any, List, Optional, Tuple, Dict
from dsa.stack import Stack


class BSTNode:
    def __init__(self, key: float, value: Any = None):
        self.key = key
        self.value = value
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None


class BST:
    """
    Binary Search Tree.
    
    Purpose:
        Powers the 'Price-range filter' (key = price) with inorder range query.
    Operations:
        - insert(key, value): O(H) where H is tree height.
        - search(key): O(H)
        - delete(key): O(H)
        - range_query(min_k, max_k): O(H + K) where K is elements in range.
        - Traversals (Inorder, Preorder, Postorder): Recursive and Iterative with Stack.
    """

    def __init__(self):
        self.root: Optional[BSTNode] = None
        self.node_count = 0
        self.comparison_count = 0

    def insert(self, key: float, value: Any = None) -> None:
        new_node = BSTNode(key, value)
        if self.root is None:
            self.root = new_node
            self.node_count += 1
            return

        curr = self.root
        while True:
            self.comparison_count += 1
            if key < curr.key:
                if curr.left is None:
                    curr.left = new_node
                    self.node_count += 1
                    break
                curr = curr.left
            else:
                if curr.right is None:
                    curr.right = new_node
                    self.node_count += 1
                    break
                curr = curr.right

    def search(self, key: float) -> Optional[Any]:
        curr = self.root
        while curr:
            self.comparison_count += 1
            if key == curr.key:
                return curr.value
            elif key < curr.key:
                curr = curr.left
            else:
                curr = curr.right
        return None

    def delete(self, key: float) -> bool:
        def _delete_node(root: Optional[BSTNode], target_key: float) -> Tuple[Optional[BSTNode], bool]:
            if root is None:
                return None, False

            self.comparison_count += 1
            if target_key < root.key:
                root.left, deleted = _delete_node(root.left, target_key)
                return root, deleted
            elif target_key > root.key:
                root.right, deleted = _delete_node(root.right, target_key)
                return root, deleted
            else:
                # Case 1 & 2: 0 or 1 child
                if root.left is None:
                    return root.right, True
                elif root.right is None:
                    return root.left, True

                # Case 3: 2 children - find inorder successor (min in right subtree)
                succ_parent = root
                succ = root.right
                while succ.left is not None:
                    succ_parent = succ
                    succ = succ.left

                root.key = succ.key
                root.value = succ.value
                # Delete successor
                if succ_parent != root:
                    succ_parent.left = succ.right
                else:
                    succ_parent.right = succ.right
                return root, True

        self.root, was_deleted = _delete_node(self.root, key)
        if was_deleted:
            self.node_count -= 1
        return was_deleted

    def range_query(self, min_key: float, max_key: float) -> List[Any]:
        """
        Returns all values whose keys satisfy min_key <= key <= max_key.
        Prunes subtrees that fall outside the query range.
        """
        results = []

        def _traverse(node: Optional[BSTNode]):
            if not node:
                return
            if node.key > min_key:
                _traverse(node.left)
            if min_key <= node.key <= max_key:
                results.append(node.value)
            if node.key < max_key:
                _traverse(node.right)

        _traverse(self.root)
        return results

    # --- Recursive Traversals ---
    def inorder_recursive(self) -> List[float]:
        res = []
        def _in(n):
            if n:
                _in(n.left)
                res.append(n.key)
                _in(n.right)
        _in(self.root)
        return res

    def preorder_recursive(self) -> List[float]:
        res = []
        def _pre(n):
            if n:
                res.append(n.key)
                _pre(n.left)
                _pre(n.right)
        _pre(self.root)
        return res

    def postorder_recursive(self) -> List[float]:
        res = []
        def _post(n):
            if n:
                _post(n.left)
                _post(n.right)
                res.append(n.key)
        _post(self.root)
        return res

    # --- Iterative Traversals with Explicit Stack ---
    def inorder_iterative(self) -> List[float]:
        res = []
        stack = Stack(200)
        curr = self.root

        while curr is not None or not stack.is_empty():
            while curr is not None:
                stack.push(curr)
                curr = curr.left

            curr = stack.pop()
            res.append(curr.key)
            curr = curr.right

        return res

    def preorder_iterative(self) -> List[float]:
        if not self.root:
            return []
        res = []
        stack = Stack(200)
        stack.push(self.root)

        while not stack.is_empty():
            node: BSTNode = stack.pop()
            res.append(node.key)
            if node.right:
                stack.push(node.right)
            if node.left:
                stack.push(node.left)

        return res

    def postorder_iterative(self) -> List[float]:
        """Postorder using two explicit Stacks."""
        if not self.root:
            return []
        s1 = Stack(200)
        s2 = Stack(200)
        s1.push(self.root)

        while not s1.is_empty():
            node: BSTNode = s1.pop()
            s2.push(node)
            if node.left:
                s1.push(node.left)
            if node.right:
                s1.push(node.right)

        res = []
        while not s2.is_empty():
            res.append(s2.pop().key)
        return res

    def height(self, node: Optional[BSTNode] = None) -> int:
        if node is None:
            node = self.root
        if node is None:
            return 0

        def _h(n):
            if not n:
                return 0
            return 1 + max(_h(n.left), _h(n.right))

        return _h(node)

    def to_tree_dict(self, node: Optional[BSTNode] = None, is_root: bool = True) -> Optional[Dict[str, Any]]:
        if is_root:
            node = self.root
        if node is None:
            return None
        return {
            "name": f"₹{node.key}",
            "key": node.key,
            "value": str(node.value) if node.value is not None else None,
            "children": [
                c for c in [
                    self.to_tree_dict(node.left, False),
                    self.to_tree_dict(node.right, False)
                ] if c is not None
            ]
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "BST",
            "count": self.node_count,
            "height": self.height(),
            "inorder": self.inorder_recursive(),
            "preorder": self.preorder_recursive(),
            "postorder": self.postorder_recursive(),
            "tree": self.to_tree_dict()
        }


class TBSTNode:
    """Node for Threaded Binary Search Tree."""
    def __init__(self, key: float, value: Any = None):
        self.key = key
        self.value = value
        self.left: Optional['TBSTNode'] = None
        self.right: Optional['TBSTNode'] = None
        self.left_thread: bool = False   # True if left points to predecessor
        self.right_thread: bool = False  # True if right points to successor


class ThreadedBST:
    """
    Double-Threaded Binary Search Tree.
    
    Purpose:
        Null links are replaced by threads to inorder predecessor (left) and successor (right).
        Enables O(N) inorder traversal using O(1) auxiliary space (no stack, no recursion).
    """

    def __init__(self):
        self.root: Optional[TBSTNode] = None
        self.node_count = 0

    def insert(self, key: float, value: Any = None) -> None:
        new_node = TBSTNode(key, value)
        if self.root is None:
            self.root = new_node
            self.node_count += 1
            return

        curr = self.root
        while True:
            if key < curr.key:
                if curr.left_thread or curr.left is None:
                    new_node.left = curr.left
                    new_node.left_thread = curr.left_thread
                    new_node.right = curr
                    new_node.right_thread = True
                    curr.left = new_node
                    curr.left_thread = False
                    self.node_count += 1
                    break
                else:
                    curr = curr.left
            elif key > curr.key:
                if curr.right_thread or curr.right is None:
                    new_node.right = curr.right
                    new_node.right_thread = curr.right_thread
                    new_node.left = curr
                    new_node.left_thread = True
                    curr.right = new_node
                    curr.right_thread = False
                    self.node_count += 1
                    break
                else:
                    curr = curr.right
            else:
                # Key already exists
                curr.value = value
                break

    def inorder_traversal(self) -> List[float]:
        """Stackless, non-recursive inorder traversal in O(N) time and O(1) extra space."""
        if self.root is None:
            return []

        # Find leftmost node
        curr = self.root
        while curr.left is not None and not curr.left_thread:
            curr = curr.left

        res = []
        while curr is not None:
            res.append(curr.key)
            if curr.right_thread:
                curr = curr.right
            else:
                curr = curr.right
                while curr is not None and curr.left is not None and not curr.left_thread:
                    curr = curr.left

        return res

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "ThreadedBST",
            "count": self.node_count,
            "inorder": self.inorder_traversal(),
            "description": "Threads replace null pointers with direct predecessor/successor links for O(1) space traversal"
        }
