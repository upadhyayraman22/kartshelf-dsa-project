"""
app.py - KartShelf E-Commerce Product Search & DSA Engine
Flask Application powering the Shop and the DSA Interactive Laboratory.
All core features powered by scratch-implemented data structures.
"""

import os
import json
import time
from flask import Flask, render_template, request, jsonify

# Import custom DSA implementations from scratch
from dsa.stack import Stack, DynamicStack, MultiStack, NavigationStackManager, simulated_category_traversal
from dsa.queue_ds import Queue, CircularQueue, Deque, InputRestrictedDeque, OutputRestrictedDeque
from dsa.priority_queue import BinaryHeap, LinkedListPriorityQueue
from dsa.linked_list import HeaderLinkedList, CircularLinkedList, Polynomial, SparseMatrix
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

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "kartshelf-secret-ece-dsa-2026"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCTS_FILE = os.path.join(BASE_DIR, "data", "products.json")

# Load dataset
with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
    ALL_PRODUCTS = json.load(f)

# Global in-memory DSA instances
avl_index = AVLTree()
bst_price_index = BST()
bplus_price_index = BPlusTree(order=4)
btree_brand_index = BTree(t=3)
trie_search = Trie()
sku_symbol_table = SymbolTable(capacity=127)
inventory_dict = ProductDictionary(capacity=127)
product_graph = Graph(directed=False)
city_graph = Graph(directed=False)
variant_disjoint_set = DisjointSet()
recent_searches_queue = CircularQueue(capacity=6)
recently_viewed_deque = Deque(capacity=10)
cart_header_ll = HeaderLinkedList()
carousel_cll = CircularLinkedList()
sparse_ratings_matrix = SparseMatrix(num_rows=10, num_cols=80)
bundle_builder = BudgetBundleBuilder(ALL_PRODUCTS)

# Interactive Lab demo instances
lab_stack = Stack(10)
lab_dyn_stack = DynamicStack(4)
lab_multi_stack = MultiStack(3, 12)
lab_cq = CircularQueue(6)
lab_deque = Deque(8)
lab_heap = BinaryHeap(is_max_heap=True)
lab_avl = AVLTree()
lab_bst = BST()
lab_threaded_bst = ThreadedBST()
lab_btree = BTree(t=2)
lab_disjoint_set = DisjointSet()
lab_hash_table = HashTable(13, hash_fn="division", collision_strategy="chaining")

def init_dsa_structures():
    """Initializes and seeds all data structures from ALL_PRODUCTS."""
    for p in ALL_PRODUCTS:
        p_id = p["id"]
        # AVL index by ID
        avl_index.insert(p_id, p)
        lab_avl.insert(p_id, p["name"])

        # BST index by Price
        bst_price_index.insert(p["price"], p)
        lab_bst.insert(p["price"], p["name"])
        lab_threaded_bst.insert(p["price"], p["name"])

        # B+ Tree by Price
        bplus_price_index.insert(p["price"], p)

        # B-Tree by Brand
        btree_brand_index.insert(p["brand"] + " - " + p["sku"], p)

        # Symbol Table by SKU
        sku_symbol_table.put(p["sku"], p)

        # Inventory Dictionary by SKU
        inventory_dict.set_stock(p["sku"], p["stock"])

        # Trie: index name, category, brand tokens
        for token in p["name"].split():
            trie_search.insert(token, p)
        trie_search.insert(p["name"], p)
        trie_search.insert(p["category"], p)
        trie_search.insert(p["brand"], p)
        trie_search.insert(p["subcategory"], p)

        # Disjoint set for variant family
        variant_disjoint_set.make_set(p_id)
        lab_disjoint_set.make_set(p_id)

        # Product recommendation Graph
        product_graph.add_vertex(p_id)
        for rel_id in p.get("related_ids", []):
            product_graph.add_edge(p_id, rel_id, weight=1.0)

    # Disjoint Set: merge products in same variant group
    groups = {}
    for p in ALL_PRODUCTS:
        grp = p.get("variant_group_id", 1)
        if grp not in groups:
            groups[grp] = []
        groups[grp].append(p["id"])

    for grp_id, members in groups.items():
        for i in range(1, len(members)):
            variant_disjoint_set.union(members[0], members[i])
            lab_disjoint_set.union(members[0], members[i])

    # Circular Linked List Carousel: pick 8 top-deal items
    top_deals = sorted(ALL_PRODUCTS, key=lambda x: x["discount_pct"], reverse=True)[:8]
    for deal in top_deals:
        carousel_cll.insert(deal)

    # Initialize city delivery network graph for Prim & Kruskal MST demo
    cities = [
        ("Bengaluru", "Chennai", 350),
        ("Bengaluru", "Hyderabad", 570),
        ("Chennai", "Hyderabad", 630),
        ("Mumbai", "Pune", 150),
        ("Mumbai", "Bengaluru", 980),
        ("Mumbai", "Jaipur", 1150),
        ("Delhi", "Jaipur", 280),
        ("Delhi", "Mumbai", 1400),
        ("Delhi", "Kolkata", 1500),
        ("Kolkata", "Chennai", 1680),
        ("Hyderabad", "Kolkata", 1480),
        ("Pune", "Bengaluru", 840),
    ]
    for u, v, w in cities:
        city_graph.add_edge(u, v, float(w))

    # Initialize sparse ratings matrix (simulated 10 users x 80 products)
    import random
    rng = random.Random(99)
    for user_id in range(10):
        # each user rates 3-6 random products
        num_ratings = rng.randint(3, 6)
        rated_prods = rng.sample(range(1, 81), num_ratings)
        for pid in rated_prods:
            sparse_ratings_matrix.set_value(user_id, pid - 1, float(rng.choice([3.5, 4.0, 4.5, 5.0])))

    # Seed Lab Stack & Queues with initial educational items
    for val in ["CartState#1", "CartState#2", "FilterApplied#Elec"]:
        lab_stack.push(val)
        lab_dyn_stack.push(val)

    lab_multi_stack.push(0, "Nav_Home")
    lab_multi_stack.push(0, "Nav_Shop")
    lab_multi_stack.push(1, "Filter_Price<2000")
    lab_multi_stack.push(2, "Cache_Trie")

    for s in ["earbuds", "leather journal", "chai kulhad"]:
        lab_cq.enqueue(s)
        recent_searches_queue.enqueue(s)

    for p in ALL_PRODUCTS[:4]:
        lab_deque.add_rear(p["name"])
        recently_viewed_deque.add_front(p)

    for p in ALL_PRODUCTS[:7]:
        lab_heap.insert(p["name"], p["rating"])
        lab_btree.insert(p["price"], p["name"])
        lab_hash_table.insert(p["sku"], p["name"])

init_dsa_structures()


# =========================================================================
# WEB PAGES
# =========================================================================
@app.route("/")
def index_page():
    return render_template("index.html")

@app.route("/product/<int:product_id>")
def product_page(product_id: int):
    # Lookup via AVL tree
    product = avl_index.search(product_id)
    if not product:
        return "Product not found", 404
    # Track in recently viewed Deque
    recently_viewed_deque.add_front(product)
    return render_template("product.html", product=product, product_id=product_id)

@app.route("/cart")
def cart_page():
    return render_template("cart.html")

@app.route("/lab")
def lab_page():
    return render_template("lab.html")


# =========================================================================
# SHOPPING & CATALOG APIs
# =========================================================================
@app.route("/api/products")
def api_products():
    """
    Search & filter products with selectable sorting algorithm engine.
    Demonstrates:
    - Trie for keyword search
    - BST / B+ Tree for price range scan
    - Custom sort algorithms: quick, merge, heap, shell, counting
    - Real-time comparison count and execution timing badge!
    """
    q = request.args.get("q", "").strip().lower()
    cat = request.args.get("category", "").strip()
    min_price = float(request.args.get("min", 0))
    max_price = float(request.args.get("max", 100000))
    min_rating = float(request.args.get("rating", 0))
    sort_by = request.args.get("sort", "price_asc")
    algo = request.args.get("algo", "merge").lower()

    # Step 1: Candidate retrieval
    if q:
        # Autocomplete search using Trie
        matches = trie_search.autocomplete(q, limit=20)
        seen_ids = set()
        candidates = []
        for match in matches:
            for p in match.get("products", []):
                if p["id"] not in seen_ids:
                    seen_ids.add(p["id"])
                    candidates.append(p)
        # If trie had direct words or fallback to linear filter
        if not candidates:
            candidates = [p for p in ALL_PRODUCTS if q in p["name"].lower() or q in p["brand"].lower()]
    elif min_price > 0 or max_price < 100000:
        # Use B+ Tree range scan
        candidates = bplus_price_index.range_query(min_price, max_price)
    else:
        candidates = list(ALL_PRODUCTS)

    # Step 2: In-memory filtering (category & rating)
    filtered = []
    for p in candidates:
        if cat and p["category"].lower() != cat.lower():
            continue
        if p["price"] < min_price or p["price"] > max_price:
            continue
        if p["rating"] < min_rating:
            continue
        filtered.append(p)

    # Step 3: Sort using chosen custom DSA sorting engine
    reverse = False
    if sort_by == "price_asc":
        key_fn = lambda x: x["price"]
        reverse = False
    elif sort_by == "price_desc":
        key_fn = lambda x: x["price"]
        reverse = True
    elif sort_by == "rating_desc":
        key_fn = lambda x: x["rating"]
        reverse = True
    elif sort_by == "name_asc":
        key_fn = lambda x: x["name"].lower()
        reverse = False
    elif sort_by == "newest":
        key_fn = lambda x: x["id"]
        reverse = True
    else:
        key_fn = lambda x: x["price"]

    # Select sorting algorithm from scratch
    if algo == "quick":
        sort_result = quick_sort(filtered, key=key_fn, reverse=reverse)
    elif algo == "heap":
        sort_result = heap_sort(filtered, key=key_fn, reverse=reverse)
    elif algo == "shell":
        sort_result = shell_sort(filtered, key=key_fn, reverse=reverse)
    elif algo == "counting":
        # Counting sort works on rating or integer scaled keys
        if "rating" in sort_by:
            sort_result = counting_sort(filtered, key=lambda x: x["rating"], reverse=reverse)
        else:
            # Scaled price / 100
            sort_result = counting_sort(filtered, key=lambda x: x["price"] // 100, reverse=reverse)
    else:
        sort_result = merge_sort(filtered, key=key_fn, reverse=reverse)

    return jsonify({
        "count": len(sort_result.sorted_items),
        "products": sort_result.sorted_items,
        "dsa_telemetry": {
            "algorithm": sort_result.algorithm,
            "comparisons": sort_result.comparisons,
            "moves": sort_result.moves,
            "time_ms": round(sort_result.time_ms, 3),
            "is_stable": sort_result.is_stable,
            "powered_by": f"Sorting ({sort_result.algorithm}) + Tree Filter (B+ Tree)"
        }
    })

@app.route("/api/autocomplete")
def api_autocomplete():
    """Prefix autocomplete powered by Trie with prefix highlight segments."""
    prefix = request.args.get("prefix", "").strip()
    if not prefix:
        return jsonify({"completions": [], "count": 0})
    completions = trie_search.autocomplete(prefix, limit=6)
    return jsonify({
        "prefix": prefix,
        "count": len(completions),
        "completions": completions,
        "powered_by": "Prefix Trie (O(L + K))"
    })

@app.route("/api/product/<int:product_id>")
def api_product(product_id: int):
    """Product lookup by ID powered by AVL Tree."""
    p = avl_index.search(product_id)
    if not p:
        return jsonify({"error": "Not found"}), 404
    return jsonify({
        "product": p,
        "dsa_telemetry": {
            "powered_by": "AVL Tree",
            "lookup_complexity": "O(log N)",
            "tree_height": avl_index._height(avl_index.root),
            "rotations_logged": avl_index.rotations
        }
    })

@app.route("/api/related/<int:product_id>")
def api_related(product_id: int):
    """'Customers also bought' powered by Graph BFS (depth 1 & 2)."""
    bfs_nodes = product_graph.bfs(product_id, max_depth=2)
    related_products = []
    seen = {product_id}
    for n_id, depth in bfs_nodes:
        if n_id not in seen:
            seen.add(n_id)
            prod = avl_index.search(n_id)
            if prod:
                related_products.append({**prod, "graph_depth": depth})
        if len(related_products) >= 6:
            break
    return jsonify({
        "product_id": product_id,
        "related": related_products,
        "powered_by": "Graph BFS (Depth 1 & 2)"
    })

@app.route("/api/family/<int:product_id>")
def api_family(product_id: int):
    """Product variant family grouping powered by Disjoint Set (Union-Find)."""
    root_rep = variant_disjoint_set.find(product_id)
    all_comps = variant_disjoint_set.get_components()
    family_ids = all_comps.get(root_rep, [product_id])
    family_members = [avl_index.search(i) for i in family_ids if avl_index.search(i)]
    return jsonify({
        "product_id": product_id,
        "representative": root_rep,
        "family_size": len(family_members),
        "variants": family_members,
        "powered_by": "Disjoint Set (Union by Rank + Path Compression)"
    })

@app.route("/api/path")
def api_path():
    """Shortest hop path between two products in the relation graph."""
    from_id = int(request.args.get("from", 1))
    to_id = int(request.args.get("to", 10))
    path_ids = product_graph.shortest_path(from_id, to_id)
    path_products = [avl_index.search(pid) for pid in (path_ids or []) if avl_index.search(pid)]
    return jsonify({
        "from_id": from_id,
        "to_id": to_id,
        "hops": len(path_ids) - 1 if path_ids else -1,
        "path_ids": path_ids,
        "path_products": path_products,
        "powered_by": "Graph Shortest Path (BFS)"
    })

@app.route("/api/cart", methods=["GET", "POST", "PUT", "DELETE"])
def api_cart():
    """Shopping Cart powered by Header Linked List with aggregate metadata."""
    if request.method == "GET":
        summary = cart_header_ll.get_summary()
        summary["powered_by"] = "Header Linked List (O(1) totals access)"
        return jsonify(summary)

    data = request.get_json(silent=True) or {}
    product_id = data.get("product_id")

    if request.method == "POST":
        qty = data.get("quantity", 1)
        p = avl_index.search(product_id)
        if not p:
            return jsonify({"error": "Product not found"}), 404
        cart_header_ll.add_item(
            product_id=p["id"],
            name=p["name"],
            price=p["price"],
            quantity=qty,
            image_seed=p.get("image_seed", ""),
            sku=p.get("sku", ""),
            image_url=p.get("image_url", "")
        )
        return jsonify(cart_header_ll.get_summary())

    elif request.method == "PUT":
        qty = data.get("quantity", 1)
        cart_header_ll.update_quantity(product_id, qty)
        return jsonify(cart_header_ll.get_summary())

    elif request.method == "DELETE":
        if product_id:
            cart_header_ll.remove_item(product_id)
        else:
            cart_header_ll.clear()
        return jsonify(cart_header_ll.get_summary())

@app.route("/api/bundle")
def api_bundle():
    """Budget Bundle Builder powered by Backtracking with branch-and-bound pruning."""
    budget = float(request.args.get("budget", 5000))
    min_items = int(request.args.get("min_items", 1))
    max_items = int(request.args.get("max_items", 5))
    if min_items < 1:
        min_items = 1
    if max_items < min_items:
        max_items = min_items
    res = bundle_builder.build_bundle(budget, min_items, max_items)
    res["powered_by"] = "Backtracking with Branch & Bound Pruning"
    return jsonify(res)

@app.route("/api/recent-searches", methods=["GET", "POST"])
def api_recent_searches():
    """Recent searches powered by CircularQueue (Ring Buffer, capacity 6)."""
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        query = data.get("query", "").strip()
        if query:
            recent_searches_queue.enqueue(query, overwrite=True)
    return jsonify({
        "searches": recent_searches_queue.to_list(),
        "capacity": recent_searches_queue.capacity,
        "count": recent_searches_queue.size(),
        "powered_by": "CircularQueue (Ring Buffer)"
    })

@app.route("/api/recently-viewed", methods=["GET", "POST"])
def api_recently_viewed():
    """Recently viewed products powered by Deque."""
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        pid = data.get("product_id")
        p = avl_index.search(pid)
        if p:
            # Remove if exists to prevent duplicates and move to front
            recently_viewed_deque.remove_item(p)
            recently_viewed_deque.add_front(p)
    return jsonify({
        "items": recently_viewed_deque.to_list(),
        "count": recently_viewed_deque.size(),
        "powered_by": "Deque (Double-Ended Queue)"
    })

@app.route("/api/top-deals")
def api_top_deals():
    """Top Deals powered by BinaryHeap (Max-Heap on discount%)."""
    heap = BinaryHeap(is_max_heap=True)
    for p in ALL_PRODUCTS:
        heap.insert(p, p["discount_pct"])
    top = []
    for _ in range(min(8, heap.size())):
        item, disc = heap.extract()
        top.append(item)
    return jsonify({
        "deals": top,
        "powered_by": "Binary Heap (Max-Heap on discount_pct)"
    })

@app.route("/api/best-rated")
def api_best_rated():
    """Best Rated products powered by BinaryHeap (Max-Heap on rating)."""
    heap = BinaryHeap(is_max_heap=True)
    for p in ALL_PRODUCTS:
        heap.insert(p, p["rating"])
    top = []
    for _ in range(min(8, heap.size())):
        item, r = heap.extract()
        top.append(item)
    return jsonify({
        "best_rated": top,
        "powered_by": "Binary Heap (Max-Heap on rating)"
    })

@app.route("/api/carousel")
def api_carousel():
    """Infinite carousel powered by CircularLinkedList."""
    items = carousel_cll.to_list()
    return jsonify({
        "current": carousel_cll.get_current(),
        "items": items,
        "powered_by": "Circular Linked List"
    })

@app.route("/api/categories")
def api_categories():
    """Category tree simulated DFS traversal powered by Stack."""
    tree = {}
    for p in ALL_PRODUCTS:
        cat = p["category"]
        sub = p["subcategory"]
        if cat not in tree:
            tree[cat] = set()
        tree[cat].add(sub)
    formatted_tree = {k: sorted(list(v)) for k, v in tree.items()}
    traversal = simulated_category_traversal(formatted_tree)
    return jsonify({
        "categories": formatted_tree,
        "stack_traversal": traversal,
        "powered_by": "Simulated Recursion via Explicit Stack"
    })


# =========================================================================
# INTERACTIVE DSA LAB APIs (Workbench for viva presentation)
# =========================================================================
@app.route("/api/lab/stack", methods=["GET", "POST"])
def api_lab_stack():
    """Stack, DynamicStack, and MultiStack live states."""
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        op = data.get("op", "push")
        target = data.get("target", "stack")
        val = data.get("value", "SampleData")

        if target == "stack":
            if op == "push":
                try:
                    lab_stack.push(val)
                except IndexError as e:
                    return jsonify({"error": str(e)}), 400
            elif op == "pop":
                try:
                    lab_stack.pop()
                except IndexError as e:
                    return jsonify({"error": str(e)}), 400

        elif target == "dynamic_stack":
            if op == "push":
                lab_dyn_stack.push(val)
            elif op == "pop":
                try:
                    lab_dyn_stack.pop()
                except IndexError as e:
                    return jsonify({"error": str(e)}), 400

        elif target == "multistack":
            s_idx = int(data.get("stack_idx", 0))
            if op == "push":
                try:
                    lab_multi_stack.push(s_idx, val)
                except IndexError as e:
                    return jsonify({"error": str(e)}), 400
            elif op == "pop":
                try:
                    lab_multi_stack.pop(s_idx)
                except IndexError as e:
                    return jsonify({"error": str(e)}), 400

    return jsonify({
        "stack": lab_stack.to_dict(),
        "dynamic_stack": lab_dyn_stack.to_dict(),
        "multistack": lab_multi_stack.to_dict()
    })

@app.route("/api/lab/queue", methods=["GET", "POST"])
def api_lab_queue():
    """Queue, CircularQueue, and Deque live states."""
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        target = data.get("target", "circular_queue")
        op = data.get("op", "enqueue")
        val = data.get("value", "SearchQuery")

        if target == "circular_queue":
            if op == "enqueue":
                lab_cq.enqueue(val, overwrite=True)
            elif op == "dequeue":
                try:
                    lab_cq.dequeue()
                except IndexError as e:
                    return jsonify({"error": str(e)}), 400

        elif target == "deque":
            if op == "add_front":
                lab_deque.add_front(val)
            elif op == "add_rear":
                lab_deque.add_rear(val)
            elif op == "remove_front":
                try:
                    lab_deque.remove_front()
                except IndexError as e:
                    return jsonify({"error": str(e)}), 400
            elif op == "remove_rear":
                try:
                    lab_deque.remove_rear()
                except IndexError as e:
                    return jsonify({"error": str(e)}), 400

    return jsonify({
        "circular_queue": lab_cq.to_dict(),
        "deque": lab_deque.to_dict(),
        "input_restricted": InputRestrictedDeque(6).to_dict(),
        "output_restricted": OutputRestrictedDeque(6).to_dict()
    })

@app.route("/api/lab/priority-queue", methods=["GET", "POST"])
def api_lab_pq():
    """BinaryHeap and LinkedListPriorityQueue demonstration."""
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        op = data.get("op", "insert")
        item = data.get("item", "ProdItem")
        priority = float(data.get("priority", 4.5))

        if op == "insert":
            lab_heap.insert(item, priority)
        elif op == "extract":
            lab_heap.extract()

    return jsonify({
        "binary_heap": lab_heap.to_dict(),
        "complexity_note": {
            "binary_heap": {"insert": "O(log N)", "extract": "O(log N)", "space": "O(N) contiguous array"},
            "linked_list_pq": {"insert": "O(N) linear search", "extract": "O(1) head removal", "space": "O(N) pointer overhead"}
        }
    })

@app.route("/api/lab/linked-list")
def api_lab_linked_list():
    """Polynomial & Sparse Matrix demonstration."""
    # Polynomial demo: P1 = 4x^3 + 3x^2 + 5, P2 = 2x^2 + 7x + 1
    p1 = Polynomial()
    p1.add_term(4, 3)
    p1.add_term(3, 2)
    p1.add_term(5, 0)

    p2 = Polynomial()
    p2.add_term(2, 2)
    p2.add_term(7, 1)
    p2.add_term(1, 0)

    p_sum = p1.add(p2)
    p_prod = p1.multiply(p2)

    return jsonify({
        "polynomial": {
            "p1": p1.to_dict(),
            "p2": p2.to_dict(),
            "sum": p_sum.to_dict(),
            "product": p_prod.to_dict(),
            "p1_eval_at_2": p1.evaluate(2.0)
        },
        "sparse_matrix": sparse_ratings_matrix.to_dict()
    })

@app.route("/api/lab/trees", methods=["GET", "POST"])
def api_lab_trees():
    """BST, Threaded BST, and AVL Tree state & traversals."""
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        tree_type = data.get("tree", "avl")
        op = data.get("op", "insert")
        key = float(data.get("key", 999))
        val = data.get("value", f"Item_{key}")

        if tree_type == "avl":
            if op == "insert":
                lab_avl.insert(key, val)
            elif op == "delete":
                lab_avl.delete(key)
        elif tree_type == "bst":
            if op == "insert":
                lab_bst.insert(key, val)
            elif op == "delete":
                lab_bst.delete(key)

    return jsonify({
        "avl": lab_avl.to_dict(),
        "bst": lab_bst.to_dict(),
        "threaded_bst": lab_threaded_bst.to_dict()
    })

@app.route("/api/lab/btree")
def api_lab_btree():
    """B-Tree and B+ Tree multi-way indexing."""
    return jsonify({
        "b_tree": lab_btree.to_dict(),
        "b_plus_tree": bplus_price_index.to_dict()
    })

@app.route("/api/lab/graph")
def api_lab_graph():
    """Graph algorithms: BFS, DFS, Shortest path, and MST on city network."""
    prim_mst = city_graph.prim_mst()
    kruskal_mst = city_graph.kruskal_mst()
    return jsonify({
        "delivery_network": {
            "vertices": city_graph.vertices,
            "edges": [e.to_dict() for e in city_graph.edges],
            "prim_mst": prim_mst,
            "kruskal_mst": kruskal_mst
        },
        "product_graph_sample": product_graph.to_dict()
    })

@app.route("/api/lab/sorting")
def api_lab_sorting():
    """Head-to-head comparison of all 5 sorting algorithms and stability demo."""
    sample = ALL_PRODUCTS[:40]

    # Benchmark on price
    shell_res = shell_sort(sample, key=lambda x: x["price"])
    quick_res = quick_sort(sample, key=lambda x: x["price"])
    merge_res = merge_sort(sample, key=lambda x: x["price"])
    heap_res = heap_sort(sample, key=lambda x: x["price"])
    counting_res = counting_sort(sample, key=lambda x: x["price"] // 100)

    stability = demonstrate_stability(ALL_PRODUCTS)

    return jsonify({
        "benchmarks": [
            shell_res.to_dict(),
            quick_res.to_dict(),
            merge_res.to_dict(),
            heap_res.to_dict(),
            counting_res.to_dict()
        ],
        "stability_demo": stability
    })

@app.route("/api/lab/searching")
def api_lab_searching():
    """Linear vs Binary search performance comparison."""
    sku_list = sorted([p for p in ALL_PRODUCTS], key=lambda x: x["sku"])
    target_sku = request.args.get("sku", sku_list[len(sku_list) // 2]["sku"])
    res = compare_search_performance(sku_list, target_sku, key=lambda x: x["sku"])
    return jsonify(res)

@app.route("/api/lab/hashing", methods=["GET", "POST"])
def api_lab_hashing():
    """Interactive Hash Table with switchable hash functions and collision strategies."""
    global lab_hash_table
    fn = request.args.get("fn", lab_hash_table.hash_fn_name)
    strategy = request.args.get("strategy", lab_hash_table.collision_strategy)

    # Re-initialize if parameters changed
    if fn != lab_hash_table.hash_fn_name or strategy != lab_hash_table.collision_strategy:
        lab_hash_table = HashTable(13, hash_fn=fn, collision_strategy=strategy)
        for p in ALL_PRODUCTS[:7]:
            try:
                lab_hash_table.insert(p["sku"], p["name"])
            except OverflowError:
                break

    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        k = data.get("key", "NEW-SKU-99")
        v = data.get("value", "Sample Product")
        try:
            lab_hash_table.insert(k, v)
        except OverflowError as e:
            return jsonify({"error": str(e)}), 400

    return jsonify(lab_hash_table.to_dict())

@app.route("/api/lab/trie")
def api_lab_trie():
    """Trie structure and autocomplete inspector."""
    prefix = request.args.get("prefix", "air")
    completions = trie_search.autocomplete(prefix, limit=6)
    return jsonify({
        "trie_sample": trie_search.to_tree_dict(depth=0),
        "total_words": trie_search.word_count,
        "query_prefix": prefix,
        "completions": completions
    })

@app.route("/api/lab/disjoint-set", methods=["GET", "POST"])
def api_lab_disjoint_set():
    """Disjoint Set component partitions inspector."""
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        p1 = int(data.get("id1", 1))
        p2 = int(data.get("id2", 2))
        lab_disjoint_set.union(p1, p2)
    return jsonify(lab_disjoint_set.to_dict())

@app.route("/api/lab/syllabus")
def api_lab_syllabus():
    """Comprehensive syllabus mapping table for the instructor viva."""
    syllabus = [
        {"unit": "Unit I", "topic": "Stack (Array / LIFO)", "impl": "dsa/stack.py: Stack", "feature": "Back / Forward navigation & Undo last filter", "complexity": "Push: O(1), Pop: O(1), Space: O(N)"},
        {"unit": "Unit I", "topic": "Dynamic Stack", "impl": "dsa/stack.py: DynamicStack", "feature": "Auto-resizing memory buffer (doubles/halves)", "complexity": "Amortized O(1), Space: O(N)"},
        {"unit": "Unit I", "topic": "Multiple Stacks in One Array", "impl": "dsa/stack.py: MultiStack", "feature": "3 partitioned stacks in single contiguous array", "complexity": "Push/Pop: O(1), Space: O(N)"},
        {"unit": "Unit I", "topic": "Simulated Recursion", "impl": "dsa/stack.py: simulated_category_traversal", "feature": "Category hierarchy tree traversal without recursion", "complexity": "Time: O(V + E), Space: O(H)"},
        {"unit": "Unit I", "topic": "Queue & Circular Queue", "impl": "dsa/queue_ds.py: CircularQueue", "feature": "Recent searches ring buffer (last 6, drop oldest)", "complexity": "Enqueue: O(1), Dequeue: O(1), Space: O(1)"},
        {"unit": "Unit I", "topic": "Deque (Input/Output Restricted)", "impl": "dsa/queue_ds.py: Deque", "feature": "Recently viewed products (front add, rear drop)", "complexity": "Add/Remove: O(1), Space: O(N)"},
        {"unit": "Unit I", "topic": "Header Linked List", "impl": "dsa/linked_list.py: HeaderLinkedList", "feature": "Shopping Cart with O(1) metadata (items & grand total)", "complexity": "Add/Remove: O(N), Totals: O(1), Space: O(N)"},
        {"unit": "Unit I", "topic": "Circular Linked List", "impl": "dsa/linked_list.py: CircularLinkedList", "feature": "Featured boutique product infinite looping carousel", "complexity": "Rotate: O(1), Insert: O(1), Space: O(N)"},
        {"unit": "Unit I", "topic": "Polynomial (Linked List)", "impl": "dsa/linked_list.py: Polynomial", "feature": "Single-variable polynomial addition & multiplication", "complexity": "Add: O(N + M), Mul: O(N * M), Space: O(N)"},
        {"unit": "Unit I", "topic": "Sparse Matrix (Triplet LL)", "impl": "dsa/linked_list.py: SparseMatrix", "feature": "User x Product rating matrix & 'You may also like'", "complexity": "Lookup/Set: O(K), Transpose: O(K), Space: O(K)"},
        {"unit": "Unit I", "topic": "Binary Heap & Linked List PQ", "impl": "dsa/priority_queue.py", "feature": "Top Deals (discount) and Best Rated (rating) ranking", "complexity": "Insert: O(log N), Extract: O(log N), Build: O(N)"},
        {"unit": "Unit I", "topic": "Backtracking Search", "impl": "dsa/backtracking.py: BudgetBundleBuilder", "feature": "Budget bundle builder (3-5 items within budget)", "complexity": "Branch & Bound with 3 pruning rules"},
        {"unit": "Unit II", "topic": "Binary Search Tree (BST)", "impl": "dsa/bst.py: BST", "feature": "Price-range filter query & 3 traversals (iter + recur)", "complexity": "Search/Insert: O(H), Inorder: O(N)"},
        {"unit": "Unit II", "topic": "Threaded BST", "impl": "dsa/bst.py: ThreadedBST", "feature": "Stackless, non-recursive inorder traversal via threads", "complexity": "Traversal: O(N) time, O(1) extra space"},
        {"unit": "Unit II", "topic": "AVL Tree", "impl": "dsa/avl.py: AVLTree", "feature": "Guaranteed O(log N) Product lookup by ID with LL/RR/LR/RL", "complexity": "Search/Insert/Delete: O(log N) guaranteed"},
        {"unit": "Unit II", "topic": "B-Tree (Multi-way Index)", "impl": "dsa/btree.py: BTree", "feature": "Database-style Name and Brand multi-way index", "complexity": "Search/Insert: O(t * log_t N), Space: O(N)"},
        {"unit": "Unit II", "topic": "B+ Tree (Linked Leaves)", "impl": "dsa/btree.py: BPlusTree", "feature": "High-speed price range queries via leaf linked list", "complexity": "Range: O(log_M N + K), Space: O(N)"},
        {"unit": "Unit III", "topic": "Graph (Adj List & Matrix)", "impl": "dsa/graph.py: Graph", "feature": "'Customers also bought' relation network & delivery graph", "complexity": "V vertices, E edges representations"},
        {"unit": "Unit III", "topic": "Breadth-First Search (BFS)", "impl": "dsa/graph.py: bfs", "feature": "Related product discovery up to depth 2 & shortest hop", "complexity": "Time: O(V + E), Space: O(V)"},
        {"unit": "Unit III", "topic": "Depth-First Search (DFS)", "impl": "dsa/graph.py: dfs", "feature": "Browsing trail exploration using explicit Stack", "complexity": "Time: O(V + E), Space: O(V)"},
        {"unit": "Unit III", "topic": "Connected Components", "impl": "dsa/graph.py: connected_components", "feature": "Product category cluster identification", "complexity": "Time: O(V + E), Space: O(V)"},
        {"unit": "Unit III", "topic": "Minimum Spanning Tree (MST)", "impl": "dsa/graph.py: prim_mst / kruskal_mst", "feature": "Warehouse-to-city delivery route optimization", "complexity": "Prim: O(V^2), Kruskal: O(E log E)"},
        {"unit": "Unit IV", "topic": "Sorting Algorithms", "impl": "dsa/sorting.py", "feature": "Engine selector: Quick, Merge, Heap, Shell, Counting", "complexity": "Quick/Merge/Heap: O(N log N), Counting: O(N+K)"},
        {"unit": "Unit IV", "topic": "Sort Stability Demonstrator", "impl": "dsa/sorting.py: demonstrate_stability", "feature": "Visual proof that Merge Sort preserves price ties vs Quick", "complexity": "Merge: Stable, Quick: Unstable"},
        {"unit": "Unit IV", "topic": "Linear vs Binary Search", "impl": "dsa/searching.py", "feature": "SKU lookup comparison counter (O(N) vs O(log N))", "complexity": "Linear: O(N) ~40 comps, Binary: O(log N) <=7 comps"},
        {"unit": "Unit IV", "topic": "Hash Table & Collisions", "impl": "dsa/hashing.py: HashTable", "feature": "Division/Mid-Square/Folding + Chaining/Linear/Quadratic", "complexity": "Average O(1), Worst O(N)"},
        {"unit": "Unit IV", "topic": "Symbol Table & Dictionary", "impl": "dsa/hashing.py: SymbolTable", "feature": "SKU -> Product details & Real-time stock dictionary", "complexity": "Average O(1)"},
        {"unit": "Unit V", "topic": "Prefix Trie", "impl": "dsa/trie.py: Trie", "feature": "As-you-type search autocomplete with prefix highlighting", "complexity": "Search/Insert: O(L), Autocomplete: O(L + K)"},
        {"unit": "Unit V", "topic": "Disjoint Set (Union-Find)", "impl": "dsa/disjoint_set.py: DisjointSet", "feature": "Product variants / same-family grouping (color/size)", "complexity": "Find/Union: O(alpha(N)) with rank & compression"}
    ]
    return jsonify({"syllabus": syllabus, "total_topics": len(syllabus)})


if __name__ == "__main__":
    print("Starting KartShelf DSA E-Commerce Server on http://127.0.0.1:5000 ...")
    app.run(host="127.0.0.1", port=5000, debug=True)
