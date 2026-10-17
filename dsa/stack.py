"""
dsa/stack.py - Stack Data Structures
Implemented from scratch without built-in queue or stack packages.

Classes:
1. Stack: Fixed or standard array-based LIFO stack.
2. DynamicStack: Auto-resizing LIFO stack (doubles when full, shrinks when 1/4 full).
3. MultiStack: Manages 3 independent stacks inside a single contiguous array.
4. NavigationStackManager: Two-stack back/forward navigation + undo/redo filter manager.
5. Simulated recursion: Depth-first traversal using an explicit Stack.
"""

from typing import Any, List, Optional, Dict


class Stack:
    """
    Fixed or bounded array-based LIFO (Last-In-First-Out) Stack.
    
    Purpose:
        Store elements where the last element inserted is the first one removed.
    Operations:
        - push(item): Insert item at top. O(1)
        - pop(): Remove and return top item. O(1)
        - peek(): Return top item without removing. O(1)
        - is_empty(): True if no items. O(1)
        - is_full(): True if max capacity reached. O(1)
        - size(): Current count. O(1)
    Complexities:
        Time: O(1) for all operations.
        Space: O(N) where N is capacity.
    """

    def __init__(self, capacity: int = 100):
        self._capacity = capacity
        self._items: List[Any] = [None] * capacity
        self._top = -1  # Index of top item

    def push(self, item: Any) -> bool:
        if self.is_full():
            raise IndexError("Stack Overflow: cannot push to full stack")
        self._top += 1
        self._items[self._top] = item
        return True

    def pop(self) -> Any:
        if self.is_empty():
            raise IndexError("Stack Underflow: cannot pop from empty stack")
        item = self._items[self._top]
        self._items[self._top] = None
        self._top -= 1
        return item

    def peek(self) -> Any:
        if self.is_empty():
            return None
        return self._items[self._top]

    def is_empty(self) -> bool:
        return self._top == -1

    def is_full(self) -> bool:
        return self._top == self._capacity - 1

    def size(self) -> int:
        return self._top + 1

    def clear(self) -> None:
        while not self.is_empty():
            self.pop()

    def to_list(self) -> List[Any]:
        """Returns items from bottom to top."""
        result = []
        for i in range(self._top + 1):
            result.append(self._items[i])
        return result

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "Stack",
            "capacity": self._capacity,
            "size": self.size(),
            "top_index": self._top,
            "items": self.to_list(),
            "is_empty": self.is_empty(),
            "is_full": self.is_full()
        }


class DynamicStack:
    """
    Auto-resizing Stack with geometric amortized O(1) time complexity.
    
    Purpose:
        Overcomes fixed capacity limitations by doubling memory allocation when full,
        and halving when occupancy falls below 25% (with hysteresis to prevent thrashing).
    Operations:
        - push(item): O(1) amortized
        - pop(): O(1) amortized
        - resize(new_capacity): O(N)
    Complexities:
        Time: O(1) amortized for push/pop. O(N) worst-case on resize.
        Space: O(N) where N is current capacity.
    """

    def __init__(self, initial_capacity: int = 4):
        self._initial_capacity = max(2, initial_capacity)
        self._capacity = self._initial_capacity
        self._items: List[Any] = [None] * self._capacity
        self._top = -1
        self.resize_events: List[Dict[str, Any]] = []

    def _resize(self, new_capacity: int, reason: str) -> None:
        old_cap = self._capacity
        new_items = [None] * new_capacity
        for i in range(self._top + 1):
            new_items[i] = self._items[i]
        self._items = new_items
        self._capacity = new_capacity
        self.resize_events.append({
            "reason": reason,
            "old_capacity": old_cap,
            "new_capacity": new_capacity,
            "size_at_resize": self._top + 1
        })

    def push(self, item: Any) -> None:
        if self._top == self._capacity - 1:
            self._resize(self._capacity * 2, "Double capacity on overflow")
        self._top += 1
        self._items[self._top] = item

    def pop(self) -> Any:
        if self.is_empty():
            raise IndexError("Stack Underflow")
        item = self._items[self._top]
        self._items[self._top] = None
        self._top -= 1

        # Shrink condition: size <= 1/4 of capacity, but don't drop below initial
        current_size = self._top + 1
        if current_size > 0 and current_size <= self._capacity // 4 and self._capacity // 2 >= self._initial_capacity:
            self._resize(self._capacity // 2, "Halve capacity on underutilization (<=25%)")

        return item

    def peek(self) -> Any:
        if self.is_empty():
            return None
        return self._items[self._top]

    def is_empty(self) -> bool:
        return self._top == -1

    def size(self) -> int:
        return self._top + 1

    def capacity(self) -> int:
        return self._capacity

    def to_list(self) -> List[Any]:
        return [self._items[i] for i in range(self._top + 1)]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "DynamicStack",
            "capacity": self._capacity,
            "initial_capacity": self._initial_capacity,
            "size": self.size(),
            "items": self.to_list(),
            "raw_slots": [repr(x) if x is not None else "None" for x in self._items],
            "resize_events": self.resize_events[-5:],
            "is_empty": self.is_empty()
        }


class MultiStack:
    """
    Multiple Stacks (default 3) partitioned in a single contiguous 1D array.
    
    Purpose:
        Demonstrates memory efficiency by sharing one array buffer among K stacks.
    Division:
        For K=3 and array size N, stack i owns range [i * (N//K), (i+1) * (N//K) - 1].
    Complexities:
        Time: O(1) for push, pop, peek.
        Space: O(N) shared array.
    """

    def __init__(self, num_stacks: int = 3, total_capacity: int = 15):
        if num_stacks < 2:
            raise ValueError("MultiStack requires at least 2 stacks")
        self.num_stacks = num_stacks
        self.total_capacity = total_capacity
        self.stack_capacity = total_capacity // num_stacks
        self.array: List[Any] = [None] * total_capacity

        # Tops array stores the current absolute index for top of each stack
        # Base array stores the start index for each stack
        self.base: List[int] = [i * self.stack_capacity for i in range(num_stacks)]
        self.tops: List[int] = [self.base[i] - 1 for i in range(num_stacks)]

    def _validate_stack_idx(self, stack_idx: int) -> None:
        if not (0 <= stack_idx < self.num_stacks):
            raise IndexError(f"Invalid stack index {stack_idx}. Range: 0 to {self.num_stacks - 1}")

    def is_full(self, stack_idx: int) -> bool:
        self._validate_stack_idx(stack_idx)
        max_idx = self.base[stack_idx] + self.stack_capacity - 1
        return self.tops[stack_idx] >= max_idx

    def is_empty(self, stack_idx: int) -> bool:
        self._validate_stack_idx(stack_idx)
        return self.tops[stack_idx] < self.base[stack_idx]

    def push(self, stack_idx: int, value: Any) -> None:
        if self.is_full(stack_idx):
            raise IndexError(f"Stack {stack_idx} is full (MultiStack partition limit)")
        self.tops[stack_idx] += 1
        self.array[self.tops[stack_idx]] = value

    def pop(self, stack_idx: int) -> Any:
        if self.is_empty(stack_idx):
            raise IndexError(f"Stack {stack_idx} is empty")
        val = self.array[self.tops[stack_idx]]
        self.array[self.tops[stack_idx]] = None
        self.tops[stack_idx] -= 1
        return val

    def peek(self, stack_idx: int) -> Any:
        if self.is_empty(stack_idx):
            return None
        return self.array[self.tops[stack_idx]]

    def get_stack_items(self, stack_idx: int) -> List[Any]:
        self._validate_stack_idx(stack_idx)
        items = []
        start = self.base[stack_idx]
        top = self.tops[stack_idx]
        for idx in range(start, top + 1):
            items.append(self.array[idx])
        return items

    def to_dict(self) -> Dict[str, Any]:
        stacks_info = []
        for i in range(self.num_stacks):
            stacks_info.append({
                "stack_id": i,
                "base": self.base[i],
                "top": self.tops[i],
                "size": max(0, self.tops[i] - self.base[i] + 1),
                "capacity": self.stack_capacity,
                "items": self.get_stack_items(i),
                "is_empty": self.is_empty(i),
                "is_full": self.is_full(i)
            })
        return {
            "type": "MultiStack",
            "total_capacity": self.total_capacity,
            "num_stacks": self.num_stacks,
            "array": [x if x is not None else "_" for x in self.array],
            "stacks": stacks_info
        }


class NavigationStackManager:
    """
    Two-stack browser history navigation and filter undo/redo manager.
    
    Demonstration:
        - Visiting page pushes current to back_stack and clears forward_stack.
        - Back pops from back_stack and pushes current to forward_stack.
        - Forward pops from forward_stack and pushes current to back_stack.
        - Undo filter pops previous filter state.
    """

    def __init__(self, initial_page: str = "/"):
        self.back_stack = Stack(50)
        self.forward_stack = Stack(50)
        self.current_page = initial_page
        self.filter_undo_stack = Stack(50)

    def visit(self, url: str) -> None:
        if url != self.current_page:
            self.back_stack.push(self.current_page)
            self.current_page = url
            self.forward_stack.clear()

    def can_go_back(self) -> bool:
        return not self.back_stack.is_empty()

    def can_go_forward(self) -> bool:
        return not self.forward_stack.is_empty()

    def go_back(self) -> Optional[str]:
        if not self.can_go_back():
            return None
        self.forward_stack.push(self.current_page)
        self.current_page = self.back_stack.pop()
        return self.current_page

    def go_forward(self) -> Optional[str]:
        if not self.can_go_forward():
            return None
        self.back_stack.push(self.current_page)
        self.current_page = self.forward_stack.pop()
        return self.current_page

    def push_filter_state(self, state: Dict[str, Any]) -> None:
        self.filter_undo_stack.push(state)

    def undo_filter(self) -> Optional[Dict[str, Any]]:
        if self.filter_undo_stack.is_empty():
            return None
        return self.filter_undo_stack.pop()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "current_page": self.current_page,
            "back_stack": self.back_stack.to_list(),
            "forward_stack": self.forward_stack.to_list(),
            "can_back": self.can_go_back(),
            "can_forward": self.can_go_forward(),
            "filter_undo_count": self.filter_undo_stack.size()
        }


def simulated_category_traversal(category_tree: Dict[str, Any]) -> List[str]:
    """
    Category tree browsing without recursion using an explicit Stack.
    Simulates call-stack frames to perform depth-first traversal of categories/subcategories.
    
    Time Complexity: O(V + E) where V is nodes and E is edges.
    Space Complexity: O(H) where H is tree height.
    """
    traversal_order = []
    stack = Stack(200)

    # Push root nodes in reverse order so first child is processed first
    roots = list(category_tree.keys())
    for i in range(len(roots) - 1, -1, -1):
        stack.push((roots[i], category_tree[roots[i]], 0))

    while not stack.is_empty():
        name, children, depth = stack.pop()
        prefix = "  " * depth + ("└─ " if depth > 0 else "")
        traversal_order.append(f"{prefix}{name}")

        if isinstance(children, list):
            for i in range(len(children) - 1, -1, -1):
                stack.push((children[i], None, depth + 1))
        elif isinstance(children, dict):
            child_keys = list(children.keys())
            for i in range(len(child_keys) - 1, -1, -1):
                k = child_keys[i]
                stack.push((k, children[k], depth + 1))

    return traversal_order
