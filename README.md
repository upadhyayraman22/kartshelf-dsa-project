# KartShelf &bull; E-Commerce Product Search &amp; DSA Laboratory Engine

A full-stack, editorial E-Commerce web application built as a term-assignment project for a **B.Tech ECE (Electronics & Communication Engineering) Data Structures & Applications (DSA)** course.

Every core e-commerce feature—from search autocomplete and multi-way database indexing to cart management, sorting engine comparisons, recommendation graphs, and budget bundle generation—is driven by **custom data structures and algorithms written completely from scratch in pure Python**.

> **Academic Rigor Guarantee:**  
> Zero built-in shortcut libraries are used inside the `dsa/` engine modules:  
> **NO** `heapq`, **NO** `bisect`, **NO** `sorted()`, **NO** `list.sort()`, **NO** `collections.deque`, and **NO** dictionary/set shortcuts for trees or hash tables. Python's built-in lists are used strictly as underlying memory buffers.

---

## 🏛️ Syllabus-to-Feature Mapping Table

This mapping links every syllabus concept to its implementation in the app and the interactive DSA Workbench.

| Course Unit | Syllabus Topic | Python Source Module | KartShelf Application Feature | Theoretical Time & Space Complexity |
| :--- | :--- | :--- | :--- | :--- |
| **UNIT I** | Stack (Array / LIFO) | `dsa/stack.py: Stack` | Back / Forward navigation & Undo last filter state | Push: $O(1)$, Pop: $O(1)$, Space: $O(N)$ |
| **UNIT I** | Dynamic Stack | `dsa/stack.py: DynamicStack` | Auto-resizing buffer (doubles at 100%, halves at 25%) | Amortized $O(1)$, Space: $O(N)$ |
| **UNIT I** | MultiStack | `dsa/stack.py: MultiStack` | 3 independent stacks partitioned in 1 contiguous array | Push/Pop: $O(1)$, Space: $O(N)$ shared |
| **UNIT I** | Simulated Recursion | `dsa/stack.py: simulated_category_traversal` | Category hierarchy depth-first traversal without recursion | Time: $O(V + E)$, Space: $O(H)$ |
| **UNIT I** | Queue & Circular Queue | `dsa/queue_ds.py: CircularQueue` | Recent searches ring buffer (last 6 items, drop oldest) | Enqueue: $O(1)$, Dequeue: $O(1)$, Space: $O(1)$ bounded |
| **UNIT I** | Deque (Input/Output Restricted) | `dsa/queue_ds.py: Deque` | Recently viewed products (add front, drop rear, remove any) | Add/Remove: $O(1)$, Space: $O(N)$ |
| **UNIT I** | Header Linked List | `dsa/linked_list.py: HeaderLinkedList` | Shopping Cart with $O(1)$ header metadata (items & grand total) | Add/Remove: $O(N)$, Totals: $O(1)$, Space: $O(N)$ |
| **UNIT I** | Circular Linked List | `dsa/linked_list.py: CircularLinkedList` | Featured boutique product infinite looping carousel | Rotate: $O(1)$, Insert: $O(1)$, Space: $O(N)$ |
| **UNIT I** | Polynomial (Linked List) | `dsa/linked_list.py: Polynomial` | Single-variable polynomial addition & multiplication in Lab | Add: $O(N+M)$, Mul: $O(N \times M)$, Space: $O(N)$ |
| **UNIT I** | Sparse Matrix (Triplet LL) | `dsa/linked_list.py: SparseMatrix` | User $\times$ Product rating matrix (>95% sparsity) & recommendations | Set/Get: $O(K)$, Transpose: $O(K)$, Space: $O(K)$ |
| **UNIT I** | Binary Heap (Max-Heap) | `dsa/priority_queue.py: BinaryHeap` | "Top Deals" (discount %) and "Best Rated" (rating) ranking | Insert: $O(\log N)$, Extract: $O(\log N)$, Build: $O(N)$ |
| **UNIT I** | Linked List Priority Queue | `dsa/priority_queue.py: LinkedListPriorityQueue` | Head-to-head complexity comparison with Binary Heap in Lab | Insert: $O(N)$, Extract: $O(1)$, Space: $O(N)$ |
| **UNIT I** | Backtracking Search | `dsa/backtracking.py: BudgetBundleBuilder` | Budget Bundle Builder (pick 3-5 items maximizing rating) | Branch & Bound with 3 pruning rules |
| **UNIT II** | Binary Search Tree (BST) | `dsa/bst.py: BST` | Price-range filter range query & 3 traversals (iterative + recursive) | Search/Insert: $O(H)$, Inorder: $O(N)$ |
| **UNIT II** | Threaded BST | `dsa/bst.py: ThreadedBST` | Stackless, non-recursive inorder traversal via threaded links | Traversal: $O(N)$ time, $O(1)$ extra space |
| **UNIT II** | AVL Tree | `dsa/avl.py: AVLTree` | Guaranteed $O(\log N)$ Product lookup by ID with LL/RR/LR/RL rotations | Search/Insert/Delete: $O(\log N)$ guaranteed |
| **UNIT II** | B-Tree | `dsa/btree.py: BTree` | Multi-way index for Brand & Name database-style lookups | Search/Insert: $O(t \log_t N)$, Space: $O(N)$ |
| **UNIT II** | B+ Tree | `dsa/btree.py: BPlusTree` | Price-range scan using sequential linked leaf nodes | Range Query: $O(\log_M N + K)$, Space: $O(N)$ |
| **UNIT III** | Graph (Adj List & Matrix) | `dsa/graph.py: Graph` | Dual representation: product relation graph & delivery network | $V$ vertices, $E$ edges representations |
| **UNIT III** | Breadth-First Search (BFS) | `dsa/graph.py: bfs` | "Customers Also Bought" related products up to depth 2 | Time: $O(V + E)$, Space: $O(V)$ |
| **UNIT III** | Depth-First Search (DFS) | `dsa/graph.py: dfs` | Browsing trail simulation using explicit Stack | Time: $O(V + E)$, Space: $O(V)$ |
| **UNIT III** | Connected Components | `dsa/graph.py: connected_components` | Product market clusters and categories | Time: $O(V + E)$, Space: $O(V)$ |
| **UNIT III** | Shortest Hop Path | `dsa/graph.py: shortest_path` | Fewest-hop connection path between any two products | Time: $O(V + E)$ using BFS predecessor tracking |
| **UNIT III** | Minimum Spanning Tree (MST) | `dsa/graph.py: prim_mst / kruskal_mst` | Warehouse-to-city distribution network route optimization | Prim: $O(V^2)$, Kruskal: $O(E \log E)$ |
| **UNIT IV** | Sorting Algorithms | `dsa/sorting.py` | Catalog sorting engine selector: Quick, Merge, Heap, Shell, Counting | Quick/Merge/Heap: $O(N \log N)$, Counting: $O(N+K)$ |
| **UNIT IV** | Sort Stability Demonstrator | `dsa/sorting.py: demonstrate_stability` | Visual proof: Merge Sort preserves price ties vs Quick Sort | Merge: Stable, Quick: Unstable |
| **UNIT IV** | Linear vs Binary Search | `dsa/searching.py` | SKU lookup comparison counter ($O(N)$ vs $O(\log N)$) | Linear: $\approx 40$ comps, Binary: $\le 7$ comps |
| **UNIT IV** | Hash Table & Collisions | `dsa/hashing.py: HashTable` | Division/Mid-Square/Folding + Chaining/Linear/Quadratic probing | Average $O(1)$, Worst $O(N)$ |
| **UNIT IV** | Symbol Table & Dictionary | `dsa/hashing.py: SymbolTable` | SKU $\to$ Product details & Real-time stock dictionary | Average $O(1)$ |
| **UNIT V** | Prefix Trie | `dsa/trie.py: Trie` | Search box as-you-type autocomplete with highlighted prefixes | Search/Insert: $O(L)$, Autocomplete: $O(L+K)$ |
| **UNIT V** | Disjoint Set (Union-Find) | `dsa/disjoint_set.py: DisjointSet` | Product variants & same-family clustering (Union by Rank + Path Compression) | Find/Union: $O(\alpha(N)) \approx O(1)$ |

---

## 🛠️ Tech Stack & Constraints

- **Backend**: Python 3.10+, Flask 3.1+ (serves HTML templates and JSON API endpoints).
- **Frontend**: Plain HTML5, Modern CSS3 with Neo-Editorial design tokens, Vanilla JavaScript ES6+ (Zero React, Zero Bootstrap, Zero Tailwind, Zero jQuery).
- **Dataset**: `data/products.json` containing 80 authentic Indian marketplace products (Brass Davarah coffee sets, Chanderi sarees, Bastar iron craft, bamboo laptop stands, Ayurvedic oils, etc.).
- **Typography**: *Fraunces* (editorial serif headings), *DM Sans* (body), and *JetBrains Mono* (DSA telemetry badges).
- **Design Palette**: Paper `#FAF5EC`, Ink `#1D1B19`, Terracotta `#E4572E`, Deep Teal `#14565F`, Mustard `#F2B134`, Sage `#A8C3A0`.

---

## 🚀 Quickstart & How to Run

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Generate Dataset (Optional - already pre-generated)
```bash
python generate_data.py
```

### 3. Run the Comprehensive Pytest Suite
```bash
python -m pytest tests/test_dsa.py -v
```
All **35 unit tests** verify every single data structure and algorithm implementation.

### 4. Launch the Web Application
```bash
python app.py
```
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in any modern web browser.

---

## 📂 Project Directory Structure

```text
kartshelf/
├── app.py                     # Flask web server & all 24 DSA API endpoints
├── generate_data.py           # Dataset generator for 80 realistic marketplace products
├── requirements.txt           # Minimal runtime dependencies (Flask, pytest)
├── README.md                  # Comprehensive academic report & documentation
├── data/
│   └── products.json          # 80 products with graph edges and variant groups
├── dsa/                       # PURE SCRATCH DSA IMPLEMENTATIONS (NO LIBRARIES)
│   ├── __init__.py
│   ├── stack.py               # Stack, DynamicStack, MultiStack, NavManager
│   ├── queue_ds.py            # Queue, CircularQueue, Deque, Restricted Deques
│   ├── priority_queue.py      # BinaryHeap (Max/Min), LinkedListPriorityQueue
│   ├── linked_list.py         # SinglyLL, HeaderLinkedList, CircularLL, Poly, SparseMatrix
│   ├── bst.py                 # BST (iterative + recursive), ThreadedBST
│   ├── avl.py                 # AVLTree with LL, RR, LR, RL rotations
│   ├── btree.py               # BTree (multi-way), BPlusTree (linked leaves)
│   ├── graph.py               # Graph (AdjList + Matrix), BFS, DFS, MST (Prim, Kruskal)
│   ├── sorting.py             # Shell, Quick, Merge, Heap, Counting, Stability Demo
│   ├── searching.py           # Linear Search, Binary Search, Comparator
│   ├── hashing.py             # HashTable (Division, Mid-Square, Folding, Probing)
│   ├── trie.py                # Prefix Trie with prefix highlight autocomplete
│   ├── disjoint_set.py        # DisjointSet with Path Compression & Union by Rank
│   └── backtracking.py        # BudgetBundleBuilder via Branch & Bound Pruning
├── templates/
│   ├── index.html             # Boutique shop homepage with Trie search & filters
│   ├── product.html           # Product detail with AVL lookup & Graph BFS
│   ├── cart.html              # HeaderLL cart & Backtracking bundle builder
│   └── lab.html               # Interactive DSA workbench with dark-ink theme
├── static/
│   ├── css/
│   │   └── style.css          # Neo-editorial CSS system, palette, and animations
│   └── js/
│       ├── app.js             # Shop interactions, cart drawer, and autocomplete
│       └── lab.js             # Interactive DSA workbench visualizers
└── tests/
    └── test_dsa.py            # Comprehensive pytest test suite (35 tests)
```

---

## 🧪 DSA Laboratory Workbench Pages

The `/lab` route provides a specialized **dark-ink workbench** designed for instructor viva examination:

1. **Unit I Workbench**: Live push/pop into array stack, dynamic stack resize logs, 3-stack partitioned array visualizer, CircularQueue ring buffer with front/rear wrap-around, Deque, and Max-Heap array slot inspector.
2. **Unit II Workbench**: AVL Tree with real-time LL, RR, LR, RL rotation counters, balance factor telemetry, and B+ Tree leaf linked-chain inspector.
3. **Unit III Workbench**: Indian distribution center network with Minimum Spanning Tree (MST) comparison (Prim vs Kruskal) and graph adjacency matrix/list inspector.
4. **Unit IV Workbench**: Live sorting benchmark table showing comparisons, moves, and execution time in ms; stability comparison (Merge vs Quick sort); Linear vs Binary search telemetry; and interactive Hash Table bucket visualizer with switchable hash functions and collision resolutions.
5. **Unit V Workbench**: Prefix Trie dictionary with prefix search tester, Disjoint Set component clusters, and the complete "Which Data Structure Should I Use?" engineering decision matrix.
6. **Syllabus Mapping Tab**: Tabular viva cheat-sheet mapping each course unit to its code, feature, and Big-O analysis.

---

## 👥 Authors & Academic Context
- **Course**: Data Structures & Applications (DSA)
- **Degree**: Bachelor of Technology (B.Tech), Electronics & Communication Engineering (ECE)
- **Institution**: University Coursework Term Project
