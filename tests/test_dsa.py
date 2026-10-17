"""
tests/test_dsa.py - Comprehensive Unit Test Suite for KartShelf DSA Engine
Tests every data structure and algorithm implementation from scratch.
"""

import pytest
from dsa.stack import Stack, DynamicStack, MultiStack, NavigationStackManager, simulated_category_traversal
from dsa.queue_ds import Queue, CircularQueue, Deque, InputRestrictedDeque, OutputRestrictedDeque
from dsa.priority_queue import BinaryHeap, LinkedListPriorityQueue
from dsa.linked_list import SinglyLinkedList, HeaderLinkedList, CircularLinkedList, Polynomial, SparseMatrix
from dsa.bst import BST, ThreadedBST
from dsa.avl import AVLTree
from dsa.btree import BTree, BPlusTree
from dsa.graph import Graph
from dsa.sorting import shell_sort, quick_sort, merge_sort, heap_sort, counting_sort, demonstrate_stability
from dsa.searching import linear_search, binary_search, compare_search_performance
from dsa.hashing import HashTable, SymbolTable, ProductDictionary
from dsa.trie import Trie
from dsa.disjoint_set import DisjointSet
from dsa.backtracking import BudgetBundleBuilder


# ==========================================
# UNIT I: Stacks
# ==========================================
def test_stack_basic_operations():
    s = Stack(5)
    assert s.is_empty()
    s.push(10)
    s.push(20)
    assert s.size() == 2
    assert s.peek() == 20
    assert s.pop() == 20
    assert s.pop() == 10
    assert s.is_empty()

def test_stack_overflow_and_underflow():
    s = Stack(2)
    s.push(1)
    s.push(2)
    with pytest.raises(IndexError):
        s.push(3)
    s.pop()
    s.pop()
    with pytest.raises(IndexError):
        s.pop()

def test_dynamic_stack_resizing():
    ds = DynamicStack(initial_capacity=2)
    ds.push("A")
    ds.push("B")
    assert ds.capacity() == 2
    ds.push("C")  # triggers double to 4
    assert ds.capacity() == 4
    ds.push("D")
    ds.push("E")  # triggers double to 8
    assert ds.capacity() == 8
    assert ds.pop() == "E"
    assert ds.pop() == "D"
    assert ds.pop() == "C"
    assert ds.pop() == "B"
    # Size is 1, capacity shrinks
    assert ds.capacity() <= 4

def test_multistack_three_partitions():
    ms = MultiStack(num_stacks=3, total_capacity=9)
    # Stack 0
    ms.push(0, "A0")
    ms.push(0, "A1")
    # Stack 1
    ms.push(1, "B0")
    # Stack 2
    ms.push(2, "C0")
    ms.push(2, "C1")
    ms.push(2, "C2")
    assert ms.is_full(2)
    with pytest.raises(IndexError):
        ms.push(2, "C_overflow")
    assert ms.pop(0) == "A1"
    assert ms.pop(1) == "B0"
    assert ms.pop(2) == "C2"

def test_navigation_stack_manager():
    nav = NavigationStackManager("/")
    nav.visit("/shop")
    nav.visit("/product/1")
    assert nav.current_page == "/product/1"
    assert nav.go_back() == "/shop"
    assert nav.go_back() == "/"
    assert nav.go_forward() == "/shop"
    # Filter undo
    nav.push_filter_state({"category": "Electronics"})
    nav.push_filter_state({"category": "Audio"})
    assert nav.undo_filter() == {"category": "Audio"}
    assert nav.undo_filter() == {"category": "Electronics"}

def test_simulated_category_traversal():
    tree = {
        "Electronics": ["Audio", "Wearables"],
        "Home": ["Decor", "Kitchen"]
    }
    result = simulated_category_traversal(tree)
    assert len(result) == 6
    assert any("Audio" in line for line in result)


# ==========================================
# UNIT I: Queues & Deque
# ==========================================
def test_queue_fifo_order():
    q = Queue(5)
    assert q.is_empty()
    q.enqueue("first")
    q.enqueue("second")
    assert q.dequeue() == "first"
    assert q.peek() == "second"
    assert q.dequeue() == "second"
    assert q.is_empty()

def test_circular_queue_recent_searches_drop_oldest():
    cq = CircularQueue(capacity=3)
    cq.enqueue("kurta")
    cq.enqueue("earbuds")
    cq.enqueue("copper bottle")
    assert cq.to_list() == ["kurta", "earbuds", "copper bottle"]
    # 4th search drops oldest ("kurta")
    cq.enqueue("chai kulhad")
    assert cq.to_list() == ["earbuds", "copper bottle", "chai kulhad"]
    # Re-searching existing item moves to latest
    cq.enqueue("earbuds")
    assert cq.to_list() == ["copper bottle", "chai kulhad", "earbuds"]

def test_deque_both_ends():
    dq = Deque(5)
    dq.add_front(10)
    dq.add_rear(20)
    dq.add_front(5)
    assert dq.to_list() == [5, 10, 20]
    assert dq.remove_front() == 5
    assert dq.remove_rear() == 20
    assert dq.to_list() == [10]

def test_restricted_deques():
    ird = InputRestrictedDeque(4)
    ird.insert("A")
    ird.insert("B")
    assert ird.delete_front() == "A"
    assert ird.delete_rear() == "B"

    ord_q = OutputRestrictedDeque(4)
    ord_q.insert_front("A")
    ord_q.insert_rear("B")
    assert ord_q.delete() == "A"
    assert ord_q.delete() == "B"


# ==========================================
# UNIT I: Priority Queue & Binary Heap
# ==========================================
def test_binary_max_heap():
    heap = BinaryHeap(is_max_heap=True)
    heap.insert("item1", 10.0)
    heap.insert("item2", 50.0)
    heap.insert("item3", 30.0)
    assert heap.peek()[1] == 50.0
    item, p = heap.extract()
    assert item == "item2" and p == 50.0
    item, p = heap.extract()
    assert item == "item3" and p == 30.0

def test_binary_heap_build_heap():
    items = [("A", 12.0), ("B", 45.0), ("C", 2.0), ("D", 88.0), ("E", 23.0)]
    heap = BinaryHeap(is_max_heap=True)
    heap.build_heap(items)
    assert heap.peek()[1] == 88.0
    extracted = []
    while not heap.is_empty():
        extracted.append(heap.extract()[1])
    assert extracted == [88.0, 45.0, 23.0, 12.0, 2.0]

def test_linked_list_priority_queue():
    pq = LinkedListPriorityQueue(is_max=True)
    pq.insert("low", 1.0)
    pq.insert("high", 10.0)
    pq.insert("mid", 5.0)
    assert pq.extract()[0] == "high"
    assert pq.extract()[0] == "mid"
    assert pq.extract()[0] == "low"


# ==========================================
# UNIT I: Linked Lists & Applications
# ==========================================
def test_header_linked_list_cart():
    cart = HeaderLinkedList()
    cart.add_item(1, "Earbuds", 1999.0, quantity=2)
    cart.add_item(2, "Copper Bottle", 899.0, quantity=1)
    summary = cart.get_summary()
    assert summary["total_items"] == 3
    assert summary["grand_total"] == round(1999.0 * 2 + 899.0, 2)
    # Update quantity
    cart.update_quantity(1, 1)
    summary2 = cart.get_summary()
    assert summary2["total_items"] == 2
    assert summary2["grand_total"] == 1999.0 + 899.0
    # Remove item
    cart.remove_item(2)
    assert cart.get_summary()["total_items"] == 1

def test_circular_linked_list_carousel():
    cll = CircularLinkedList()
    cll.insert("Slide 1")
    cll.insert("Slide 2")
    cll.insert("Slide 3")
    assert cll.get_current() == "Slide 1"
    assert cll.rotate_forward() == "Slide 2"
    assert cll.rotate_forward() == "Slide 3"
    assert cll.rotate_forward() == "Slide 1"  # loops forever
    assert cll.rotate_backward() == "Slide 3"

def test_polynomial_addition_and_multiplication():
    # P1: 3x^2 + 5x + 2
    p1 = Polynomial()
    p1.add_term(3, 2)
    p1.add_term(5, 1)
    p1.add_term(2, 0)
    # P2: 4x^1 + 1
    p2 = Polynomial()
    p2.add_term(4, 1)
    p2.add_term(1, 0)

    # Addition: 3x^2 + 9x + 3
    p_add = p1.add(p2)
    assert p_add.evaluate(1) == 15.0  # 3 + 9 + 3

    # Multiplication: (3x^2 + 5x + 2)(4x + 1) = 12x^3 + 3x^2 + 20x^2 + 5x + 8x + 2 = 12x^3 + 23x^2 + 13x + 2
    p_mul = p1.multiply(p2)
    assert p_mul.evaluate(2) == 12 * 8 + 23 * 4 + 13 * 2 + 2  # 96 + 92 + 26 + 2 = 216

def test_sparse_matrix():
    sm = SparseMatrix(4, 4)
    sm.set_value(0, 1, 4.5)
    sm.set_value(2, 3, 5.0)
    assert sm.get_value(0, 1) == 4.5
    assert sm.get_value(0, 0) == 0.0
    assert sm.non_zero_count == 2
    trans = sm.transpose()
    assert trans.get_value(1, 0) == 4.5
    assert trans.get_value(3, 2) == 5.0


# ==========================================
# UNIT II: BST & Threaded BST
# ==========================================
def test_bst_insert_search_delete():
    bst = BST()
    for val in [50, 30, 70, 20, 40, 60, 80]:
        bst.insert(val, f"val_{val}")
    assert bst.search(40) == "val_40"
    assert bst.search(99) is None
    # Range query (price filter)
    in_range = bst.range_query(25, 65)
    assert len(in_range) == 4  # 30, 40, 50, 60
    # Delete
    assert bst.delete(30) is True
    assert bst.search(30) is None

def test_bst_recursive_and_iterative_traversals():
    bst = BST()
    for val in [40, 20, 60, 10, 30]:
        bst.insert(val)
    # Inorder
    assert bst.inorder_recursive() == [10, 20, 30, 40, 60]
    assert bst.inorder_iterative() == [10, 20, 30, 40, 60]
    # Preorder
    assert bst.preorder_recursive() == [40, 20, 10, 30, 60]
    assert bst.preorder_iterative() == [40, 20, 10, 30, 60]
    # Postorder
    assert bst.postorder_recursive() == [10, 30, 20, 60, 40]
    assert bst.postorder_iterative() == [10, 30, 20, 60, 40]

def test_threaded_bst():
    tbst = ThreadedBST()
    for k in [40, 20, 60, 10, 30, 50, 70]:
        tbst.insert(k)
    # Inorder traversal without recursion or stack
    assert tbst.inorder_traversal() == [10, 20, 30, 40, 50, 60, 70]


# ==========================================
# UNIT II: AVL Tree
# ==========================================
def test_avl_rotations():
    # LL Rotation test
    avl = AVLTree()
    avl.insert(30)
    avl.insert(20)
    avl.insert(10)  # triggers LL rotation
    assert avl.rotations["LL"] == 1
    assert avl.root.key == 20

    # RR Rotation test
    avl2 = AVLTree()
    avl2.insert(10)
    avl2.insert(20)
    avl2.insert(30)  # triggers RR rotation
    assert avl2.rotations["RR"] == 1
    assert avl2.root.key == 20

    # LR Rotation test
    avl3 = AVLTree()
    avl3.insert(30)
    avl3.insert(10)
    avl3.insert(20)  # triggers LR rotation
    assert avl3.rotations["LR"] == 1
    assert avl3.root.key == 20

def test_avl_lookup_and_delete():
    avl = AVLTree()
    for i in range(1, 16):
        avl.insert(i, f"Product #{i}")
    assert avl._height(avl.root) <= 4  # log2(15) is ~4
    assert avl.search(7) == "Product #7"
    assert avl.delete(7) is True
    assert avl.search(7) is None


# ==========================================
# UNIT II: B-Tree & B+ Tree
# ==========================================
def test_btree_multiway_search():
    bt = BTree(t=2)
    keys = [10, 20, 5, 6, 12, 30, 7, 17]
    for k in keys:
        bt.insert(k, f"Val_{k}")
    for k in keys:
        assert bt.search(k) == f"Val_{k}"
    assert bt.search(999) is None

def test_bplus_tree_range_scan():
    bplus = BPlusTree(order=3)
    prices = [199, 449, 699, 899, 1199, 1499, 1999, 2499, 3999]
    for p in prices:
        bplus.insert(p, f"Prod_₹{p}")
    assert bplus.search(899) == "Prod_₹899"
    # Range query
    range_res = bplus.range_query(500, 2000)
    assert range_res == ["Prod_₹699", "Prod_₹899", "Prod_₹1199", "Prod_₹1499", "Prod_₹1999"]


# ==========================================
# UNIT III: Graphs & Networks
# ==========================================
def test_graph_bfs_and_dfs():
    g = Graph()
    g.add_edge("P1", "P2")
    g.add_edge("P2", "P3")
    g.add_edge("P1", "P4")
    g.add_edge("P4", "P5")

    # BFS from P1
    bfs_res = g.bfs("P1", max_depth=2)
    vertices_found = [v for v, depth in bfs_res]
    assert "P2" in vertices_found and "P4" in vertices_found
    assert "P3" in vertices_found and "P5" in vertices_found

    # DFS from P1
    dfs_res = g.dfs("P1")
    assert len(dfs_res) == 5

def test_graph_shortest_hop_and_components():
    g = Graph()
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(1, 4)  # direct shortcut
    # Disconnected island
    g.add_edge(5, 6)

    path = g.shortest_path(1, 4)
    assert path == [1, 4]  # 1 hop
    comps = g.connected_components()
    assert len(comps) == 2

def test_graph_mst_prim_and_kruskal():
    g = Graph()
    # Triangle network
    g.add_edge("BLR", "BOM", 980)
    g.add_edge("BOM", "DEL", 1400)
    g.add_edge("BLR", "DEL", 2100)

    prim_res = g.prim_mst()
    kruskal_res = g.kruskal_mst()
    assert prim_res["total_cost"] == 980 + 1400  # 2380
    assert kruskal_res["total_cost"] == 2380


# ==========================================
# UNIT IV: Sorting & Searching
# ==========================================
def test_all_sorting_algorithms():
    data = [45, 12, 85, 32, 89, 39, 69, 44, 42, 1, 100]
    expected = [1, 12, 32, 39, 42, 44, 45, 69, 85, 89, 100]

    assert shell_sort(data).sorted_items == expected
    assert quick_sort(data).sorted_items == expected
    assert merge_sort(data).sorted_items == expected
    assert heap_sort(data).sorted_items == expected
    assert counting_sort(data).sorted_items == expected

def test_stable_sort_demo():
    items = [
        {"name": "A", "price": 100, "rating": 4.5},
        {"name": "B", "price": 200, "rating": 4.5},
        {"name": "C", "price": 150, "rating": 4.0}
    ]
    res = demonstrate_stability(items)
    assert res["merge_sort_stable"]["is_stable"] is True

def test_linear_and_binary_search():
    sorted_items = [{"sku": f"SKU-{i:03d}", "id": i} for i in range(1, 51)]
    lin = linear_search(sorted_items, "SKU-042", key=lambda x: x["sku"])
    bin_s = binary_search(sorted_items, "SKU-042", key=lambda x: x["sku"])
    assert lin["found"] is True
    assert bin_s["found"] is True
    assert bin_s["comparisons"] <= 6  # log2(50) is ~6
    assert lin["comparisons"] == 42


# ==========================================
# UNIT IV: Hashing
# ==========================================
def test_hash_table_functions_and_collision_modes():
    # Chaining with Division
    ht1 = HashTable(capacity=7, hash_fn="division", collision_strategy="chaining")
    ht1.insert("SKU-1", "Product 1")
    ht1.insert("SKU-8", "Product 8")  # likely collision
    assert ht1.get("SKU-1") == "Product 1"
    assert ht1.get("SKU-8") == "Product 8"

    # Linear Probing with Mid-Square
    ht2 = HashTable(capacity=11, hash_fn="mid_square", collision_strategy="linear")
    ht2.insert("ITEM_A", 100)
    ht2.insert("ITEM_B", 200)
    assert ht2.get("ITEM_A") == 100
    assert ht2.get("ITEM_B") == 200

    # Quadratic Probing with Folding
    ht3 = HashTable(capacity=11, hash_fn="folding", collision_strategy="quadratic")
    ht3.insert(10, "Ten")
    ht3.insert(21, "Twenty-One")
    assert ht3.get(10) == "Ten"
    assert ht3.get(21) == "Twenty-One"
    ht3.delete(10)
    assert ht3.get(10) is None

def test_symbol_table_and_product_dictionary():
    st = SymbolTable(capacity=23)
    st.put("KS-ELEC-001", {"name": "Earbuds"})
    assert st.contains("KS-ELEC-001")
    assert st.get("KS-ELEC-001")["name"] == "Earbuds"

    inv = ProductDictionary(capacity=23)
    inv.set_stock("KS-ELEC-001", 10)
    assert inv.decrement_stock("KS-ELEC-001", 3) is True
    assert inv.get_stock("KS-ELEC-001") == 7


# ==========================================
# UNIT V: Trie
# ==========================================
def test_trie_insert_search_autocomplete():
    trie = Trie()
    trie.insert("airdopes", {"id": 1})
    trie.insert("airpods", {"id": 2})
    trie.insert("ajrakh", {"id": 3})

    assert trie.search("airdopes") is True
    assert trie.search("air") is False

    # Autocomplete
    matches = trie.autocomplete("air")
    words = [m["full_word"] for m in matches]
    assert "airdopes" in words
    assert "airpods" in words
    assert "ajrakh" not in words

    # Delete
    assert trie.delete("airpods") is True
    assert trie.search("airpods") is False
    assert trie.search("airdopes") is True


# ==========================================
# UNIT V: Disjoint Set
# ==========================================
def test_disjoint_set_union_and_find():
    ds = DisjointSet()
    for i in range(1, 7):
        ds.make_set(i)

    # Union (1, 2) and (2, 3) -> Family {1, 2, 3}
    ds.union(1, 2)
    ds.union(2, 3)
    # Union (4, 5) -> Family {4, 5}
    ds.union(4, 5)

    assert ds.connected(1, 3) is True
    assert ds.connected(1, 4) is False
    comps = ds.get_components()
    assert len(comps) == 3  # {1,2,3}, {4,5}, {6}


# ==========================================
# UNIT V: Backtracking Budget Bundle Builder
# ==========================================
def test_budget_bundle_builder():
    catalog = [
        {"id": 1, "name": "Item 1", "price": 500, "rating": 4.5},
        {"id": 2, "name": "Item 2", "price": 800, "rating": 4.8},
        {"id": 3, "name": "Item 3", "price": 1200, "rating": 4.6},
        {"id": 4, "name": "Item 4", "price": 400, "rating": 4.0},
        {"id": 5, "name": "Item 5", "price": 600, "rating": 4.2},
        {"id": 6, "name": "Item 6", "price": 3000, "rating": 5.0},
    ]
    builder = BudgetBundleBuilder(catalog)
    res = builder.build_bundle(budget=2500, min_items=3, max_items=4)
    assert res["found"] is True
    assert res["total_price"] <= 2500
    assert 3 <= res["item_count"] <= 4
    assert res["states_explored"] > 0
