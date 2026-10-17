"""
dsa/linked_list.py - Linked List Data Structures & Applications
Implemented from scratch without built-in linked structures.

Classes:
1. Node: Basic singly linked node.
2. SinglyLinkedList: Fundamental pointer-based chain.
3. HeaderLinkedList: Singly linked list with metadata in header node (Powers Shopping Cart).
4. CircularLinkedList: Circular chain (Powers Featured Product Infinite Carousel).
5. Polynomial: Linked list polynomial arithmetic (Add & Multiply).
6. SparseMatrix: Triplet linked list for user-product ratings & recommendations.
"""

from typing import Any, List, Optional, Dict, Tuple


class Node:
    def __init__(self, data: Any, next_node=None):
        self.data = data
        self.next: Optional['Node'] = next_node


class SinglyLinkedList:
    """
    Standard Singly Linked List.
    Operations:
        - insert_head(data): O(1)
        - insert_tail(data): O(N) or O(1) with tail pointer
        - delete(key): O(N)
        - search(key): O(N)
    """

    def __init__(self):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self.count = 0

    def is_empty(self) -> bool:
        return self.head is None

    def size(self) -> int:
        return self.count

    def insert_head(self, data: Any) -> None:
        new_node = Node(data, self.head)
        self.head = new_node
        if self.tail is None:
            self.tail = new_node
        self.count += 1

    def insert_tail(self, data: Any) -> None:
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            assert self.tail is not None
            self.tail.next = new_node
            self.tail = new_node
        self.count += 1

    def delete(self, key_func) -> bool:
        """Deletes first node where key_func(node.data) is True."""
        curr = self.head
        prev = None
        while curr:
            if key_func(curr.data):
                if prev is None:
                    self.head = curr.next
                    if self.head is None:
                        self.tail = None
                else:
                    prev.next = curr.next
                    if curr == self.tail:
                        self.tail = prev
                self.count -= 1
                return True
            prev = curr
            curr = curr.next
        return False

    def search(self, key_func) -> Optional[Any]:
        curr = self.head
        while curr:
            if key_func(curr.data):
                return curr.data
            curr = curr.next
        return None

    def to_list(self) -> List[Any]:
        res = []
        curr = self.head
        while curr:
            res.append(curr.data)
            curr = curr.next
        return res

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "SinglyLinkedList",
            "size": self.count,
            "items": self.to_list()
        }


class CartItem:
    def __init__(self, product_id: int, name: str, price: float, quantity: int = 1, image_seed: str = "", sku: str = "", image_url: str = ""):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.image_seed = image_seed
        self.sku = sku
        self.image_url = image_url

    def subtotal(self) -> float:
        return self.price * self.quantity

    def to_dict(self) -> Dict[str, Any]:
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "subtotal": self.subtotal(),
            "image_seed": self.image_seed,
            "image_url": self.image_url,
            "sku": self.sku
        }


class HeaderNode:
    """Header node storing aggregate list metadata."""
    def __init__(self):
        self.total_item_count = 0
        self.grand_total_price = 0.0
        self.next: Optional[Node] = None


class HeaderLinkedList:
    """
    Header Linked List powering the Shopping Cart.
    
    Purpose:
        The dummy header node maintains total item count and grand total price in O(1)
        access, eliminating the need to traverse the entire list for cart badges and totals.
    Operations:
        - add_item(product_id, name, price, qty): O(N) check if exists, then update or append
        - remove_item(product_id): O(N)
        - update_quantity(product_id, qty): O(N)
        - get_summary(): O(1)
    """

    def __init__(self):
        self.header = HeaderNode()

    def _recalculate_header(self) -> None:
        """Internal recalculation to guarantee integrity."""
        count = 0
        total = 0.0
        curr = self.header.next
        while curr:
            item: CartItem = curr.data
            count += item.quantity
            total += item.subtotal()
            curr = curr.next
        self.header.total_item_count = count
        self.header.grand_total_price = round(total, 2)

    def add_item(self, product_id: int, name: str, price: float, quantity: int = 1, image_seed: str = "", sku: str = "", image_url: str = "") -> None:
        # Check if product is already in cart
        curr = self.header.next
        while curr:
            item: CartItem = curr.data
            if item.product_id == product_id:
                item.quantity += quantity
                if image_url and not item.image_url:
                    item.image_url = image_url
                self._recalculate_header()
                return
            curr = curr.next

        # New item: insert after header
        new_item = CartItem(product_id, name, price, quantity, image_seed, sku, image_url)
        new_node = Node(new_item, self.header.next)
        self.header.next = new_node
        self._recalculate_header()

    def remove_item(self, product_id: int) -> bool:
        prev = self.header
        curr = self.header.next
        while curr:
            item: CartItem = curr.data
            if item.product_id == product_id:
                prev.next = curr.next
                self._recalculate_header()
                return True
            prev = curr
            curr = curr.next
        return False

    def update_quantity(self, product_id: int, quantity: int) -> bool:
        if quantity <= 0:
            return self.remove_item(product_id)

        curr = self.header.next
        while curr:
            item: CartItem = curr.data
            if item.product_id == product_id:
                item.quantity = quantity
                self._recalculate_header()
                return True
            curr = curr.next
        return False

    def clear(self) -> None:
        self.header.next = None
        self.header.total_item_count = 0
        self.header.grand_total_price = 0.0

    def get_items(self) -> List[Dict[str, Any]]:
        res = []
        curr = self.header.next
        while curr:
            res.append(curr.data.to_dict())
            curr = curr.next
        return res

    def get_summary(self) -> Dict[str, Any]:
        return {
            "total_items": self.header.total_item_count,
            "grand_total": self.header.grand_total_price,
            "items": self.get_items()
        }

    def to_dict(self) -> Dict[str, Any]:
        summary = self.get_summary()
        summary["type"] = "HeaderLinkedList"
        return summary


class CircularLinkedList:
    """
    Circular Singly Linked List.
    
    Purpose:
        Powers the 'Featured Product Carousel' that loops infinitely.
        The last node's pointer points back to head.
    Operations:
        - insert(data): O(1) or O(N)
        - rotate_forward(): O(1)
        - rotate_backward(): O(N)
        - get_current(): O(1)
    """

    def __init__(self):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self.current: Optional[Node] = None
        self.count = 0

    def is_empty(self) -> bool:
        return self.head is None

    def size(self) -> int:
        return self.count

    def insert(self, data: Any) -> None:
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            new_node.next = self.head
            self.current = new_node
        else:
            assert self.tail is not None
            self.tail.next = new_node
            new_node.next = self.head
            self.tail = new_node
        self.count += 1

    def rotate_forward(self) -> Optional[Any]:
        if not self.current:
            return None
        self.current = self.current.next
        return self.current.data

    def rotate_backward(self) -> Optional[Any]:
        if not self.current or self.count <= 1:
            return self.get_current()
        # Find node whose next is self.current
        curr = self.head
        assert curr is not None
        while curr.next != self.current:
            curr = curr.next
        self.current = curr
        return self.current.data

    def get_current(self) -> Optional[Any]:
        return self.current.data if self.current else None

    def to_list(self) -> List[Any]:
        if self.head is None:
            return []
        res = []
        curr = self.head
        for _ in range(self.count):
            res.append(curr.data)
            curr = curr.next
        return res

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "CircularLinkedList",
            "size": self.count,
            "current": self.get_current(),
            "items": self.to_list()
        }


class PolyTermNode:
    def __init__(self, coeff: float, exp: int, next_node=None):
        self.coeff = coeff
        self.exp = exp
        self.next: Optional['PolyTermNode'] = next_node


class Polynomial:
    """
    Single-Variable Polynomial P(x) represented as a linked list of terms.
    Terms are maintained in strictly descending order of exponent.
    
    Operations:
        - add(other): O(N + M) merges two ordered linked lists.
        - multiply(other): O(N * M) multiplies each term and accumulates.
        - evaluate(x): O(N) computes value for given x.
    """

    def __init__(self):
        self.head: Optional[PolyTermNode] = None

    def add_term(self, coeff: float, exp: int) -> None:
        if abs(coeff) < 1e-9:
            return

        new_node = PolyTermNode(coeff, exp)
        if self.head is None or exp > self.head.exp:
            new_node.next = self.head
            self.head = new_node
            return

        prev = None
        curr = self.head
        while curr and curr.exp > exp:
            prev = curr
            curr = curr.next

        if curr and curr.exp == exp:
            curr.coeff += coeff
            # If coefficient becomes 0, remove term
            if abs(curr.coeff) < 1e-9:
                if prev is None:
                    self.head = curr.next
                else:
                    prev.next = curr.next
            return

        new_node.next = curr
        if prev is None:
            self.head = new_node
        else:
            prev.next = new_node

    def add(self, other: 'Polynomial') -> 'Polynomial':
        res = Polynomial()
        p1 = self.head
        p2 = other.head
        while p1 and p2:
            if p1.exp > p2.exp:
                res.add_term(p1.coeff, p1.exp)
                p1 = p1.next
            elif p2.exp > p1.exp:
                res.add_term(p2.coeff, p2.exp)
                p2 = p2.next
            else:
                res.add_term(p1.coeff + p2.coeff, p1.exp)
                p1 = p1.next
                p2 = p2.next

        while p1:
            res.add_term(p1.coeff, p1.exp)
            p1 = p1.next
        while p2:
            res.add_term(p2.coeff, p2.exp)
            p2 = p2.next

        return res

    def multiply(self, other: 'Polynomial') -> 'Polynomial':
        res = Polynomial()
        p1 = self.head
        while p1:
            p2 = other.head
            while p2:
                res.add_term(p1.coeff * p2.coeff, p1.exp + p2.exp)
                p2 = p2.next
            p1 = p1.next
        return res

    def evaluate(self, x: float) -> float:
        total = 0.0
        curr = self.head
        while curr:
            total += curr.coeff * (x ** curr.exp)
            curr = curr.next
        return total

    def to_string(self) -> str:
        if self.head is None:
            return "0"
        parts = []
        curr = self.head
        while curr:
            c = curr.coeff
            e = curr.exp
            c_str = f"{c:g}" if abs(c) != 1 or e == 0 else ("" if c > 0 else "-")
            if e == 0:
                parts.append(f"{c:g}")
            elif e == 1:
                parts.append(f"{c_str}x")
            else:
                parts.append(f"{c_str}x^{e}")
            curr = curr.next
        return " + ".join(parts).replace("+ -", "- ")

    def to_dict(self) -> Dict[str, Any]:
        terms = []
        curr = self.head
        while curr:
            terms.append({"coeff": curr.coeff, "exp": curr.exp})
            curr = curr.next
        return {
            "type": "Polynomial",
            "string": self.to_string(),
            "terms": terms
        }


class MatrixNode:
    def __init__(self, row: int, col: int, val: float, next_node=None):
        self.row = row
        self.col = col
        self.val = val
        self.next: Optional['MatrixNode'] = next_node


class SparseMatrix:
    """
    Sparse Matrix implemented via Linked List of Triplet Elements (row, col, value).
    
    Purpose:
        Models user-product ratings matrix where >95% of entries are zero/unrated.
        Powers the 'You may also like' collaborative product recommendation in Lab.
    Operations:
        - set_value(r, c, v): O(N)
        - get_value(r, c): O(N)
        - transpose(): O(N)
        - to_dict(): O(N)
    """

    def __init__(self, num_rows: int, num_cols: int):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.head: Optional[MatrixNode] = None
        self.non_zero_count = 0

    def set_value(self, row: int, col: int, val: float) -> None:
        if not (0 <= row < self.num_rows and 0 <= col < self.num_cols):
            raise IndexError("Matrix index out of bounds")

        prev = None
        curr = self.head
        while curr:
            if curr.row == row and curr.col == col:
                if abs(val) < 1e-9:
                    # Delete zero element
                    if prev is None:
                        self.head = curr.next
                    else:
                        prev.next = curr.next
                    self.non_zero_count -= 1
                else:
                    curr.val = val
                return
            prev = curr
            curr = curr.next

        if abs(val) >= 1e-9:
            new_node = MatrixNode(row, col, val, self.head)
            self.head = new_node
            self.non_zero_count += 1

    def get_value(self, row: int, col: int) -> float:
        curr = self.head
        while curr:
            if curr.row == row and curr.col == col:
                return curr.val
            curr = curr.next
        return 0.0

    def transpose(self) -> 'SparseMatrix':
        trans = SparseMatrix(self.num_cols, self.num_rows)
        curr = self.head
        while curr:
            trans.set_value(curr.col, curr.row, curr.val)
            curr = curr.next
        return trans

    def to_triplets(self) -> List[Tuple[int, int, float]]:
        res = []
        curr = self.head
        while curr:
            res.append((curr.row, curr.col, curr.val))
            curr = curr.next
        return res

    def to_dict(self) -> Dict[str, Any]:
        density = (self.non_zero_count / (self.num_rows * self.num_cols)) * 100 if self.num_rows * self.num_cols > 0 else 0
        return {
            "type": "SparseMatrix",
            "rows": self.num_rows,
            "cols": self.num_cols,
            "non_zero_count": self.non_zero_count,
            "sparsity_pct": round(100 - density, 2),
            "triplets": [{"row": r, "col": c, "val": v} for r, c, v in self.to_triplets()]
        }
