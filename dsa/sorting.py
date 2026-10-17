"""
dsa/sorting.py - Sorting Algorithms & Stability Demonstrator
Implemented strictly from scratch without Python's list.sort() or sorted().

Algorithms:
1. Shell Sort (Diminishing increment sort)
2. Quick Sort (Divide and conquer with partition)
3. Merge Sort (Divide, conquer and stable merge)
4. Heap Sort (Heapify and extract max)
5. Counting Sort (Non-comparison based integer distribution sort)
6. Stability Demonstrator: Compares Merge Sort (stable) vs Quick Sort (unstable).
"""

import time
from typing import Any, List, Callable, Optional, Dict, Tuple


class SortResult:
    def __init__(self, sorted_items: List[Any], comparisons: int, moves: int, time_ms: float, algorithm: str, is_stable: bool):
        self.sorted_items = sorted_items
        self.comparisons = comparisons
        self.moves = moves
        self.time_ms = time_ms
        self.algorithm = algorithm
        self.is_stable = is_stable

    def to_dict(self) -> Dict[str, Any]:
        return {
            "algorithm": self.algorithm,
            "comparisons": self.comparisons,
            "moves": self.moves,
            "time_ms": round(self.time_ms, 3),
            "is_stable": self.is_stable,
            "item_count": len(self.sorted_items)
        }


def _default_key(x: Any) -> Any:
    return x


def shell_sort(arr: List[Any], key: Optional[Callable[[Any], Any]] = None, reverse: bool = False) -> SortResult:
    """
    Shell Sort: Generalization of insertion sort using diminishing gap sequences (Knuth sequence).
    
    Time: O(N log^2 N) or O(N^(3/2)) depending on gaps.
    Space: O(1) auxiliary (in-place).
    Stability: Unstable.
    """
    t0 = time.perf_counter()
    k_fn = key if key is not None else _default_key
    items = [x for x in arr]
    n = len(items)
    comparisons = 0
    moves = 0

    # Knuth gap sequence: 1, 4, 13, 40, 121...
    gap = 1
    while gap < n // 3:
        gap = 3 * gap + 1

    while gap > 0:
        for i in range(gap, n):
            temp = items[i]
            temp_key = k_fn(temp)
            j = i
            while j >= gap:
                comparisons += 1
                curr_key = k_fn(items[j - gap])
                should_move = (curr_key < temp_key) if reverse else (curr_key > temp_key)
                if should_move:
                    items[j] = items[j - gap]
                    moves += 1
                    j -= gap
                else:
                    break
            items[j] = temp
            moves += 1
        gap //= 3

    t1 = time.perf_counter()
    return SortResult(items, comparisons, moves, (t1 - t0) * 1000, "Shell Sort", False)


def quick_sort(arr: List[Any], key: Optional[Callable[[Any], Any]] = None, reverse: bool = False) -> SortResult:
    """
    Quick Sort: Divide-and-conquer using Lomuto / Median-of-three partitioning.
    
    Time: O(N log N) average, O(N^2) worst case.
    Space: O(log N) stack frames.
    Stability: Unstable.
    """
    t0 = time.perf_counter()
    k_fn = key if key is not None else _default_key
    items = [x for x in arr]
    comparisons = 0
    moves = 0

    def _partition(low: int, high: int) -> int:
        nonlocal comparisons, moves
        # Median of three pivot choice
        mid = (low + high) // 2
        # Pivot choice at high
        pivot_val = k_fn(items[high])
        i = low - 1
        for j in range(low, high):
            comparisons += 1
            item_val = k_fn(items[j])
            condition = (item_val > pivot_val) if reverse else (item_val < pivot_val)
            if condition:
                i += 1
                items[i], items[j] = items[j], items[i]
                moves += 2
        items[i + 1], items[high] = items[high], items[i + 1]
        moves += 2
        return i + 1

    def _qs(low: int, high: int):
        if low < high:
            pi = _partition(low, high)
            _qs(low, pi - 1)
            _qs(pi + 1, high)

    if len(items) > 1:
        _qs(0, len(items) - 1)

    t1 = time.perf_counter()
    return SortResult(items, comparisons, moves, (t1 - t0) * 1000, "Quick Sort", False)


def merge_sort(arr: List[Any], key: Optional[Callable[[Any], Any]] = None, reverse: bool = False) -> SortResult:
    """
    Merge Sort: Stable divide-and-conquer sorting.
    
    Time: O(N log N) worst-case and average.
    Space: O(N) auxiliary array.
    Stability: Stable (preserves order of duplicates).
    """
    t0 = time.perf_counter()
    k_fn = key if key is not None else _default_key
    items = [x for x in arr]
    comparisons = 0
    moves = 0

    def _ms(lst: List[Any]) -> List[Any]:
        nonlocal comparisons, moves
        if len(lst) <= 1:
            return lst

        mid = len(lst) // 2
        left = _ms(lst[:mid])
        right = _ms(lst[mid:])

        # Merge step
        merged = []
        i = 0
        j = 0
        while i < len(left) and j < len(right):
            comparisons += 1
            lk = k_fn(left[i])
            rk = k_fn(right[j])
            # Strict inequality for stability
            condition = (lk >= rk) if reverse else (lk <= rk)
            if condition:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
            moves += 1

        while i < len(left):
            merged.append(left[i])
            i += 1
            moves += 1
        while j < len(right):
            merged.append(right[j])
            j += 1
            moves += 1

        return merged

    sorted_res = _ms(items)
    t1 = time.perf_counter()
    return SortResult(sorted_res, comparisons, moves, (t1 - t0) * 1000, "Merge Sort", True)


def heap_sort(arr: List[Any], key: Optional[Callable[[Any], Any]] = None, reverse: bool = False) -> SortResult:
    """
    Heap Sort: In-place array-based heapification followed by extraction.
    
    Time: O(N log N) guaranteed in all cases.
    Space: O(1) in-place.
    Stability: Unstable.
    """
    t0 = time.perf_counter()
    k_fn = key if key is not None else _default_key
    items = [x for x in arr]
    n = len(items)
    comparisons = 0
    moves = 0

    def _sift(curr: int, size: int):
        nonlocal comparisons, moves
        while True:
            left = 2 * curr + 1
            right = 2 * curr + 2
            extreme = curr

            if left < size:
                comparisons += 1
                cond = (k_fn(items[left]) < k_fn(items[extreme])) if reverse else (k_fn(items[left]) > k_fn(items[extreme]))
                if cond:
                    extreme = left

            if right < size:
                comparisons += 1
                cond = (k_fn(items[right]) < k_fn(items[extreme])) if reverse else (k_fn(items[right]) > k_fn(items[extreme]))
                if cond:
                    extreme = right

            if extreme != curr:
                items[curr], items[extreme] = items[extreme], items[curr]
                moves += 2
                curr = extreme
            else:
                break

    # Build heap bottom-up
    for i in range(n // 2 - 1, -1, -1):
        _sift(i, n)

    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        items[0], items[i] = items[i], items[0]
        moves += 2
        _sift(0, i)

    t1 = time.perf_counter()
    return SortResult(items, comparisons, moves, (t1 - t0) * 1000, "Heap Sort", False)


def counting_sort(arr: List[Any], key: Optional[Callable[[Any], Any]] = None, reverse: bool = False) -> SortResult:
    """
    Counting Sort: Non-comparison stable sort for integer/scaled ratings (e.g. 1.0 to 5.0 scaled x2 -> 2 to 10).
    
    Time: O(N + K) where K is range of keys.
    Space: O(N + K).
    Stability: Stable (backwards accumulation into output).
    """
    t0 = time.perf_counter()
    k_fn = key if key is not None else _default_key
    if not arr:
        return SortResult([], 0, 0, 0.0, "Counting Sort", True)

    # Map keys to integers
    keys = [int(round(float(k_fn(x)) * 2)) for x in arr]  # scale ratings by 2 to make integers
    min_k = keys[0]
    max_k = keys[0]
    for k in keys:
        if k < min_k:
            min_k = k
        if k > max_k:
            max_k = k

    range_k = max_k - min_k + 1
    count = [0] * range_k
    output = [None] * len(arr)
    moves = 0

    # Count occurrences
    for k in keys:
        count[k - min_k] += 1

    # Prefix sums
    for i in range(1, range_k):
        count[i] += count[i - 1]

    # Build output in reverse for stability
    for i in range(len(arr) - 1, -1, -1):
        k = keys[i]
        idx = count[k - min_k] - 1
        output[idx] = arr[i]
        count[k - min_k] -= 1
        moves += 1

    if reverse:
        rev_output = [None] * len(output)
        for i in range(len(output)):
            rev_output[i] = output[len(output) - 1 - i]
        output = rev_output

    t1 = time.perf_counter()
    return SortResult(output, 0, moves, (t1 - time.perf_counter()) * 1000 if (t1 - t0) < 0 else (t1 - t0) * 1000, "Counting Sort", True)


def demonstrate_stability(products: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Demonstrates Stability:
    1. First sort products by price (ascending).
    2. Then sort by rating (e.g. 4.5, 4.0).
    Under Merge Sort (Stable): products with equal rating keep their price-sorted order.
    Under Quick Sort (Unstable): products with equal rating scramble their previous price order!
    """
    # Step 1: Pre-sort a small subset (e.g. 10 products) by price
    subset = products[:12]
    by_price = merge_sort(subset, key=lambda p: p["price"]).sorted_items

    # Step 2: Sort by rating using Merge Sort (stable)
    stable_res = merge_sort(by_price, key=lambda p: p["rating"], reverse=True)

    # Step 3: Sort by rating using Quick Sort (unstable)
    unstable_res = quick_sort(by_price, key=lambda p: p["rating"], reverse=True)

    return {
        "description": "Stability comparison: pre-sorted by price, then sorted by rating. Stable sort retains price ordering within ties.",
        "pre_sorted_by_price": [{"name": p["name"][:20], "price": p["price"], "rating": p["rating"]} for p in by_price],
        "merge_sort_stable": {
            "items": [{"name": p["name"][:20], "price": p["price"], "rating": p["rating"]} for p in stable_res.sorted_items],
            "is_stable": True,
            "comparisons": stable_res.comparisons
        },
        "quick_sort_unstable": {
            "items": [{"name": p["name"][:20], "price": p["price"], "rating": p["rating"]} for p in unstable_res.sorted_items],
            "is_stable": False,
            "comparisons": unstable_res.comparisons
        }
    }
