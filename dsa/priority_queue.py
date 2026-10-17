"""
dsa/priority_queue.py - Priority Queue & Binary Heap Data Structures
Implemented from scratch without heapq or sort shortcuts.

Classes:
1. BinaryHeap: Array-based Max-Heap / Min-Heap with O(N) build_heap, O(log N) insert/extract.
2. LinkedListPriorityQueue: Singly linked-list based priority queue for complexity comparison.
"""

from typing import Any, List, Optional, Tuple, Dict


class HeapNode:
    def __init__(self, item: Any, priority: float):
        self.item = item
        self.priority = priority

    def __repr__(self):
        return f"Node(p={self.priority}, item={self.item})"


class BinaryHeap:
    """
    Array-based Binary Heap (default: Max-Heap).
    
    Purpose:
        Powers 'Top Deals' (prioritized by discount_pct) and 'Best Rated' (prioritized by rating).
    Operations:
        - insert(item, priority): O(log N)
        - extract_max(): O(log N)
        - peek(): O(1)
        - build_heap(items): O(N) bottom-up heapification
    Complexities:
        Time: Insert O(log N), Extract-Max O(log N), Find-Max O(1), Build O(N).
        Space: O(N) array representation.
    """

    def __init__(self, is_max_heap: bool = True):
        self.is_max_heap = is_max_heap
        self._heap: List[HeapNode] = []
        self.comparison_count = 0

    def _compares_higher(self, p1: float, p2: float) -> bool:
        self.comparison_count += 1
        if self.is_max_heap:
            return p1 > p2
        return p1 < p2

    def size(self) -> int:
        return len(self._heap)

    def is_empty(self) -> bool:
        return len(self._heap) == 0

    def peek(self) -> Optional[Tuple[Any, float]]:
        if self.is_empty():
            return None
        node = self._heap[0]
        return (node.item, node.priority)

    def _parent(self, i: int) -> int:
        return (i - 1) // 2

    def _left_child(self, i: int) -> int:
        return 2 * i + 1

    def _right_child(self, i: int) -> int:
        return 2 * i + 2

    def _sift_up(self, index: int) -> None:
        curr = index
        while curr > 0:
            parent = self._parent(curr)
            if self._compares_higher(self._heap[curr].priority, self._heap[parent].priority):
                # Swap
                self._heap[curr], self._heap[parent] = self._heap[parent], self._heap[curr]
                curr = parent
            else:
                break

    def _sift_down(self, index: int) -> None:
        curr = index
        n = len(self._heap)
        while True:
            left = self._left_child(curr)
            right = self._right_child(curr)
            best = curr

            if left < n and self._compares_higher(self._heap[left].priority, self._heap[best].priority):
                best = left
            if right < n and self._compares_higher(self._heap[right].priority, self._heap[best].priority):
                best = right

            if best != curr:
                self._heap[curr], self._heap[best] = self._heap[best], self._heap[curr]
                curr = best
            else:
                break

    def insert(self, item: Any, priority: float) -> None:
        node = HeapNode(item, priority)
        self._heap.append(node)
        self._sift_up(len(self._heap) - 1)

    def extract(self) -> Optional[Tuple[Any, float]]:
        """Extracts and returns (item, priority) with highest/lowest priority."""
        if self.is_empty():
            return None
        if len(self._heap) == 1:
            node = self._heap.pop()
            return (node.item, node.priority)

        root = self._heap[0]
        self._heap[0] = self._heap.pop()
        self._sift_down(0)
        return (root.item, root.priority)

    def build_heap(self, items_with_priority: List[Tuple[Any, float]]) -> None:
        """O(N) bottom-up heap construction from arbitrary input."""
        self._heap = [HeapNode(item, p) for item, p in items_with_priority]
        # Sift down from last non-leaf node up to root
        start_idx = (len(self._heap) // 2) - 1
        for i in range(start_idx, -1, -1):
            self._sift_down(i)

    def to_list(self) -> List[Dict[str, Any]]:
        return [{"item": node.item, "priority": node.priority} for node in self._heap]

    def to_tree_dict(self, index: int = 0) -> Optional[Dict[str, Any]]:
        """Generates hierarchical dict for tree visualization."""
        if index >= len(self._heap):
            return None
        node = self._heap[index]
        return {
            "name": f"{node.priority}",
            "item": str(node.item),
            "priority": node.priority,
            "children": [
                c for c in [
                    self.to_tree_dict(self._left_child(index)),
                    self.to_tree_dict(self._right_child(index))
                ] if c is not None
            ]
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "BinaryHeap",
            "heap_type": "Max-Heap" if self.is_max_heap else "Min-Heap",
            "size": self.size(),
            "comparisons": self.comparison_count,
            "array": [{"index": i, "priority": node.priority, "item": node.item} for i, node in enumerate(self._heap)],
            "tree": self.to_tree_dict(0)
        }


class LLNode:
    def __init__(self, item: Any, priority: float, next_node=None):
        self.item = item
        self.priority = priority
        self.next = next_node


class LinkedListPriorityQueue:
    """
    Singly linked-list based Priority Queue.
    Maintains descending order of priority upon insertion (Sorted Linked List).
    
    Complexities:
        Time: Insert O(N), Extract O(1), Peek O(1).
        Comparison to Binary Heap:
            Binary Heap: Insert O(log N), Extract O(log N) -> superior for dynamic workloads.
            Linked List PQ: Insert O(N), Extract O(1) -> fast extract, slow insert.
    """

    def __init__(self, is_max: bool = True):
        self.head: Optional[LLNode] = None
        self.count = 0
        self.is_max = is_max
        self.comparison_count = 0

    def is_empty(self) -> bool:
        return self.head is None

    def size(self) -> int:
        return self.count

    def insert(self, item: Any, priority: float) -> None:
        """O(N) insertion to keep list sorted."""
        new_node = LLNode(item, priority)
        self.count += 1

        def _should_come_before(p1, p2):
            self.comparison_count += 1
            return p1 > p2 if self.is_max else p1 < p2

        if self.head is None or _should_come_before(priority, self.head.priority):
            new_node.next = self.head
            self.head = new_node
            return

        curr = self.head
        while curr.next is not None and not _should_come_before(priority, curr.next.priority):
            curr = curr.next

        new_node.next = curr.next
        curr.next = new_node

    def extract(self) -> Optional[Tuple[Any, float]]:
        """O(1) removal of highest/lowest priority item from head."""
        if self.is_empty():
            return None
        node = self.head
        self.head = self.head.next
        self.count -= 1
        return (node.item, node.priority)

    def peek(self) -> Optional[Tuple[Any, float]]:
        if self.is_empty():
            return None
        return (self.head.item, self.head.priority)

    def to_list(self) -> List[Dict[str, Any]]:
        res = []
        curr = self.head
        while curr:
            res.append({"item": curr.item, "priority": curr.priority})
            curr = curr.next
        return res

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "LinkedListPriorityQueue",
            "size": self.count,
            "comparisons": self.comparison_count,
            "items": self.to_list()
        }
