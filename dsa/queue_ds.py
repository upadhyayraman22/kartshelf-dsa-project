"""
dsa/queue_ds.py - Queue and Deque Data Structures
Implemented from scratch without collections.deque or list.pop(0).

Classes:
1. Queue: Standard FIFO queue using head index on a contiguous array.
2. CircularQueue: Fixed-capacity ring buffer with modulo wrap-around (Recent Searches).
3. Deque: Circular double-ended queue (Recently Viewed Products).
4. InputRestrictedDeque: Insertion only at rear; deletion at both front and rear.
5. OutputRestrictedDeque: Deletion only at front; insertion at both front and rear.
"""

from typing import Any, List, Optional, Dict


class Queue:
    """
    Standard FIFO (First-In-First-Out) Queue implemented with head pointer
    to avoid O(N) element shifting of list.pop(0).
    
    Operations:
        - enqueue(item): O(1) amortized
        - dequeue(): O(1)
        - peek(): O(1)
        - is_empty(): O(1)
        - size(): O(1)
    """

    def __init__(self, capacity: int = 100):
        self._capacity = capacity
        self._items: List[Any] = [None] * capacity
        self._head = 0
        self._tail = 0
        self._count = 0

    def enqueue(self, item: Any) -> bool:
        if self._count == self._capacity:
            raise IndexError("Queue Overflow: capacity reached")
        self._items[self._tail] = item
        self._tail = (self._tail + 1) % self._capacity
        self._count += 1
        return True

    def dequeue(self) -> Any:
        if self.is_empty():
            raise IndexError("Queue Underflow: cannot dequeue from empty queue")
        item = self._items[self._head]
        self._items[self._head] = None
        self._head = (self._head + 1) % self._capacity
        self._count -= 1
        return item

    def peek(self) -> Any:
        if self.is_empty():
            return None
        return self._items[self._head]

    def is_empty(self) -> bool:
        return self._count == 0

    def is_full(self) -> bool:
        return self._count == self._capacity

    def size(self) -> int:
        return self._count

    def to_list(self) -> List[Any]:
        res = []
        idx = self._head
        for _ in range(self._count):
            res.append(self._items[idx])
            idx = (idx + 1) % self._capacity
        return res

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "Queue",
            "capacity": self._capacity,
            "size": self._count,
            "head": self._head,
            "tail": self._tail,
            "items": self.to_list(),
            "is_empty": self.is_empty(),
            "is_full": self.is_full()
        }


class CircularQueue:
    """
    Fixed-capacity Circular Queue (Ring Buffer).
    
    Purpose:
        Powers 'Recent Searches' (capacity 6). Overwrite mode allows the newest
        search to replace the oldest when the buffer is saturated.
    Operations:
        - enqueue(item, overwrite=True): O(1)
        - dequeue(): O(1)
        - peek(): O(1)
    Complexities:
        Time: O(1) for all operations.
        Space: O(N) bounded memory.
    """

    def __init__(self, capacity: int = 6):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity
        self._buffer: List[Any] = [None] * capacity
        self.front = 0
        self.rear = -1
        self.count = 0

    def enqueue(self, item: Any, overwrite: bool = True) -> bool:
        """
        Enqueues item. If full and overwrite=True, drops oldest item (advances front).
        If item already exists, moves it to the most recent position without duplicates.
        """
        # Deduplication for recent searches: remove existing instance if present
        existing_items = self.to_list()
        dedup_items = [x for x in existing_items if x != item]
        if len(dedup_items) < len(existing_items):
            # Rebuild queue without the duplicate
            self.clear()
            for x in dedup_items:
                self.enqueue(x, overwrite=True)

        if self.is_full():
            if not overwrite:
                raise IndexError("CircularQueue is full")
            # Overwrite oldest by advancing front
            self.front = (self.front + 1) % self.capacity
            self.count -= 1

        self.rear = (self.rear + 1) % self.capacity
        self._buffer[self.rear] = item
        self.count += 1
        return True

    def dequeue(self) -> Any:
        if self.is_empty():
            raise IndexError("CircularQueue is empty")
        item = self._buffer[self.front]
        self._buffer[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.count -= 1
        return item

    def peek(self) -> Any:
        if self.is_empty():
            return None
        return self._buffer[self.front]

    def is_empty(self) -> bool:
        return self.count == 0

    def is_full(self) -> bool:
        return self.count == self.capacity

    def size(self) -> int:
        return self.count

    def clear(self) -> None:
        self._buffer = [None] * self.capacity
        self.front = 0
        self.rear = -1
        self.count = 0

    def to_list(self) -> List[Any]:
        res = []
        curr = self.front
        for _ in range(self.count):
            res.append(self._buffer[curr])
            curr = (curr + 1) % self.capacity
        return res

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "CircularQueue",
            "capacity": self.capacity,
            "size": self.count,
            "front": self.front,
            "rear": self.rear,
            "items": self.to_list(),
            "raw_buffer": [repr(x) if x is not None else "_" for x in self._buffer],
            "is_full": self.is_full(),
            "is_empty": self.is_empty()
        }


class Deque:
    """
    Double-Ended Queue implemented on a circular array.
    
    Purpose:
        Powers 'Recently Viewed Products'. Supports adding to front, dropping
        oldest from rear, and removing specific items if re-browsed.
    Operations:
        - add_front(item), add_rear(item): O(1)
        - remove_front(), remove_rear(): O(1)
        - peek_front(), peek_rear(): O(1)
    """

    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        self._items: List[Any] = [None] * capacity
        self.front = -1
        self.rear = -1
        self.count = 0

    def is_empty(self) -> bool:
        return self.count == 0

    def is_full(self) -> bool:
        return self.count == self.capacity

    def size(self) -> int:
        return self.count

    def add_front(self, item: Any) -> None:
        if self.is_full():
            # Drop oldest from rear to make room
            self.remove_rear()

        if self.is_empty():
            self.front = 0
            self.rear = 0
        else:
            self.front = (self.front - 1 + self.capacity) % self.capacity

        self._items[self.front] = item
        self.count += 1

    def add_rear(self, item: Any) -> None:
        if self.is_full():
            # Drop oldest from front
            self.remove_front()

        if self.is_empty():
            self.front = 0
            self.rear = 0
        else:
            self.rear = (self.rear + 1) % self.capacity

        self._items[self.rear] = item
        self.count += 1

    def remove_front(self) -> Any:
        if self.is_empty():
            raise IndexError("Deque is empty")
        item = self._items[self.front]
        self._items[self.front] = None
        if self.front == self.rear:
            self.front = -1
            self.rear = -1
        else:
            self.front = (self.front + 1) % self.capacity
        self.count -= 1
        return item

    def remove_rear(self) -> Any:
        if self.is_empty():
            raise IndexError("Deque is empty")
        item = self._items[self.rear]
        self._items[self.rear] = None
        if self.front == self.rear:
            self.front = -1
            self.rear = -1
        else:
            self.rear = (self.rear - 1 + self.capacity) % self.capacity
        self.count -= 1
        return item

    def peek_front(self) -> Any:
        if self.is_empty():
            return None
        return self._items[self.front]

    def peek_rear(self) -> Any:
        if self.is_empty():
            return None
        return self._items[self.rear]

    def remove_item(self, item: Any) -> bool:
        """Removes a specific item if found (used when re-visiting a product)."""
        current_list = self.to_list()
        found = False
        new_list = []
        for x in current_list:
            if x == item and not found:
                found = True
            else:
                new_list.append(x)

        if found:
            self.clear()
            for x in new_list:
                self.add_rear(x)
        return found

    def clear(self) -> None:
        self._items = [None] * self.capacity
        self.front = -1
        self.rear = -1
        self.count = 0

    def to_list(self) -> List[Any]:
        res = []
        if self.is_empty():
            return res
        curr = self.front
        for _ in range(self.count):
            res.append(self._items[curr])
            curr = (curr + 1) % self.capacity
        return res

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "Deque",
            "capacity": self.capacity,
            "size": self.count,
            "front": self.front,
            "rear": self.rear,
            "items": self.to_list(),
            "raw_slots": [repr(x) if x is not None else "_" for x in self._items],
            "is_full": self.is_full(),
            "is_empty": self.is_empty()
        }


class InputRestrictedDeque:
    """
    Input-Restricted Deque:
    Insertion allowed ONLY at rear end.
    Deletion allowed at BOTH front and rear ends.
    """

    def __init__(self, capacity: int = 8):
        self._deque = Deque(capacity)

    def insert(self, item: Any) -> None:
        """Insertion permitted only at rear."""
        self._deque.add_rear(item)

    def delete_front(self) -> Any:
        return self._deque.remove_front()

    def delete_rear(self) -> Any:
        return self._deque.remove_rear()

    def peek_front(self) -> Any:
        return self._deque.peek_front()

    def peek_rear(self) -> Any:
        return self._deque.peek_rear()

    def size(self) -> int:
        return self._deque.size()

    def is_empty(self) -> bool:
        return self._deque.is_empty()

    def to_dict(self) -> Dict[str, Any]:
        d = self._deque.to_dict()
        d["variant"] = "InputRestrictedDeque (Insert Rear Only; Delete Both)"
        return d


class OutputRestrictedDeque:
    """
    Output-Restricted Deque:
    Deletion allowed ONLY at front end.
    Insertion allowed at BOTH front and rear ends.
    """

    def __init__(self, capacity: int = 8):
        self._deque = Deque(capacity)

    def insert_front(self, item: Any) -> None:
        self._deque.add_front(item)

    def insert_rear(self, item: Any) -> None:
        self._deque.add_rear(item)

    def delete(self) -> Any:
        """Deletion permitted only at front."""
        return self._deque.remove_front()

    def peek(self) -> Any:
        return self._deque.peek_front()

    def size(self) -> int:
        return self._deque.size()

    def is_empty(self) -> bool:
        return self._deque.is_empty()

    def to_dict(self) -> Dict[str, Any]:
        d = self._deque.to_dict()
        d["variant"] = "OutputRestrictedDeque (Delete Front Only; Insert Both)"
        return d
