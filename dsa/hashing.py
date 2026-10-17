"""
dsa/hashing.py - Hash Table with Custom Hash Functions & Collision Strategies
Implemented completely from scratch without Python's built-in dict for bucket storage.

Hash Functions:
1. Division Method: h(k) = k mod m
2. Mid-Square Method: square key, extract middle bits/digits mod m
3. Folding Method: chunk key into pieces, sum them mod m

Collision Strategies:
1. Chaining (Open Hashing / Separate Chaining via Singly Linked List)
2. Linear Probing (Closed Hashing / Open Addressing)
3. Quadratic Probing (Closed Hashing / Open Addressing)

Classes:
- HashTable: Generic hash table with selectable function and collision mode.
- SymbolTable: SKU -> Product record index.
- ProductDictionary: SKU -> Stock & Inventory status.
"""

from typing import Any, List, Optional, Tuple, Dict
from dsa.linked_list import Node


class HashEntry:
    def __init__(self, key: Any, value: Any):
        self.key = key
        self.value = value
        self.is_deleted = False  # Tombstone for open addressing deletion


class HashTable:
    """
    Hash Table implemented with an array buffer.
    
    Purpose:
        Powers SKU -> Product (Symbol Table) and Inventory/Stock lookups.
    Features:
        - Configurable hash function: 'division', 'mid_square', 'folding'
        - Configurable collision resolution: 'chaining', 'linear', 'quadratic'
        - Telemetry: tracks collision count, probe count, load factor.
    """

    def __init__(self, capacity: int = 17, hash_fn: str = "division", collision_strategy: str = "chaining"):
        self.capacity = capacity
        self.hash_fn_name = hash_fn
        self.collision_strategy = collision_strategy

        # Array buffer
        self.table: List[Any] = [None] * capacity
        self.count = 0
        self.collision_count = 0
        self.probe_count = 0

    def _to_int_key(self, key: Any) -> int:
        """Converts arbitrary string or int key to an integer for mathematical hashing."""
        if isinstance(key, int):
            return abs(key)
        # Horner's polynomial accumulation for string keys
        h = 0
        for char in str(key):
            h = (h * 31 + ord(char)) & 0xFFFFFFFF
        return h

    def compute_hash(self, key: Any) -> int:
        k = self._to_int_key(key)
        m = self.capacity

        if self.hash_fn_name == "division":
            return k % m

        elif self.hash_fn_name == "mid_square":
            # Square the key and extract middle decimal digits
            squared = k * k
            s_str = str(squared)
            mid_len = max(1, len(s_str) // 3)
            start = max(0, (len(s_str) - mid_len) // 2)
            mid_slice = s_str[start:start + mid_len]
            mid_val = int(mid_slice) if mid_slice else 0
            return mid_val % m

        elif self.hash_fn_name == "folding":
            # 2-digit partition folding
            s_str = str(k)
            fold_sum = 0
            for i in range(0, len(s_str), 2):
                chunk = s_str[i:i + 2]
                if chunk:
                    fold_sum += int(chunk)
            return fold_sum % m

        return k % m

    def load_factor(self) -> float:
        return round(self.count / self.capacity, 3)

    def insert(self, key: Any, value: Any) -> bool:
        base_hash = self.compute_hash(key)

        if self.collision_strategy == "chaining":
            head: Optional[Node] = self.table[base_hash]
            if head is None:
                self.table[base_hash] = Node(HashEntry(key, value))
                self.count += 1
                return True

            # Collision occurred
            self.collision_count += 1
            curr = head
            while curr:
                entry: HashEntry = curr.data
                if entry.key == key:
                    entry.value = value  # update
                    return True
                if curr.next is None:
                    break
                curr = curr.next

            # Append to chain
            curr.next = Node(HashEntry(key, value))
            self.count += 1
            return True

        # Open Addressing: Linear or Quadratic Probing
        i = 0
        while i < self.capacity:
            self.probe_count += 1
            if self.collision_strategy == "linear":
                slot = (base_hash + i) % self.capacity
            elif self.collision_strategy == "quadratic":
                slot = (base_hash + i + i * i) % self.capacity
            else:
                slot = (base_hash + i) % self.capacity

            entry: Optional[HashEntry] = self.table[slot]

            if entry is None or entry.is_deleted:
                if i > 0:
                    self.collision_count += 1
                self.table[slot] = HashEntry(key, value)
                self.count += 1
                return True
            elif entry.key == key:
                entry.value = value
                return True

            i += 1

        raise OverflowError("Hash Table Overflow: No available slot found with current probing strategy")

    def get(self, key: Any) -> Optional[Any]:
        base_hash = self.compute_hash(key)

        if self.collision_strategy == "chaining":
            curr: Optional[Node] = self.table[base_hash]
            while curr:
                entry: HashEntry = curr.data
                if entry.key == key:
                    return entry.value
                curr = curr.next
            return None

        # Open Addressing
        i = 0
        while i < self.capacity:
            if self.collision_strategy == "linear":
                slot = (base_hash + i) % self.capacity
            else:
                slot = (base_hash + i + i * i) % self.capacity

            entry: Optional[HashEntry] = self.table[slot]
            if entry is None:
                return None
            if not entry.is_deleted and entry.key == key:
                return entry.value
            i += 1

        return None

    def delete(self, key: Any) -> bool:
        base_hash = self.compute_hash(key)

        if self.collision_strategy == "chaining":
            curr: Optional[Node] = self.table[base_hash]
            prev = None
            while curr:
                entry: HashEntry = curr.data
                if entry.key == key:
                    if prev is None:
                        self.table[base_hash] = curr.next
                    else:
                        prev.next = curr.next
                    self.count -= 1
                    return True
                prev = curr
                curr = curr.next
            return False

        # Open Addressing tombstone deletion
        i = 0
        while i < self.capacity:
            if self.collision_strategy == "linear":
                slot = (base_hash + i) % self.capacity
            else:
                slot = (base_hash + i + i * i) % self.capacity

            entry: Optional[HashEntry] = self.table[slot]
            if entry is None:
                return False
            if not entry.is_deleted and entry.key == key:
                entry.is_deleted = True
                self.count -= 1
                return True
            i += 1

        return False

    def to_dict(self) -> Dict[str, Any]:
        buckets = []
        for i in range(self.capacity):
            slot = self.table[i]
            if slot is None:
                buckets.append({"index": i, "status": "empty", "entries": []})
            elif self.collision_strategy == "chaining":
                chain = []
                curr = slot
                while curr:
                    chain.append({"key": str(curr.data.key), "value": str(curr.data.value)})
                    curr = curr.next
                buckets.append({
                    "index": i,
                    "status": f"chain ({len(chain)})",
                    "entries": chain
                })
            else:
                entry: HashEntry = slot
                if entry.is_deleted:
                    buckets.append({"index": i, "status": "tombstone", "entries": []})
                else:
                    buckets.append({
                        "index": i,
                        "status": "occupied",
                        "entries": [{"key": str(entry.key), "value": str(entry.value)}]
                    })

        return {
            "type": "HashTable",
            "capacity": self.capacity,
            "count": self.count,
            "load_factor": self.load_factor(),
            "hash_function": self.hash_fn_name,
            "collision_strategy": self.collision_strategy,
            "total_collisions": self.collision_count,
            "total_probes": self.probe_count,
            "buckets": buckets
        }


class SymbolTable:
    """
    Symbol Table abstraction mapping SKU string -> Product Metadata.
    """

    def __init__(self, capacity: int = 101):
        self._table = HashTable(capacity, hash_fn="folding", collision_strategy="chaining")

    def put(self, sku: str, product_data: Any) -> None:
        self._table.insert(sku, product_data)

    def get(self, sku: str) -> Optional[Any]:
        return self._table.get(sku)

    def contains(self, sku: str) -> bool:
        return self._table.get(sku) is not None

    def to_dict(self) -> Dict[str, Any]:
        return self._table.to_dict()


class ProductDictionary:
    """
    Dictionary mapping Product SKU -> Current Real-time Inventory Stock.
    """

    def __init__(self, capacity: int = 101):
        self._table = HashTable(capacity, hash_fn="division", collision_strategy="linear")

    def set_stock(self, sku: str, stock: int) -> None:
        self._table.insert(sku, stock)

    def get_stock(self, sku: str) -> Optional[int]:
        return self._table.get(sku)

    def decrement_stock(self, sku: str, qty: int = 1) -> bool:
        curr = self.get_stock(sku)
        if curr is not None and curr >= qty:
            self.set_stock(sku, curr - qty)
            return True
        return False

    def to_dict(self) -> Dict[str, Any]:
        return self._table.to_dict()
