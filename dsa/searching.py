"""
dsa/searching.py - Linear and Binary Search Algorithms
Implemented from scratch with comparison counters and timing.

Algorithms:
1. Linear Search: Sequential comparison over unsorted or sorted array.
2. Binary Search: Divide-and-conquer logarithmic search over sorted array.
3. Search Comparator: Side-by-side performance analysis for SKU lookups.
"""

import time
from typing import Any, List, Callable, Optional, Dict


def _default_key(x: Any) -> Any:
    return x


def linear_search(arr: List[Any], target: Any, key: Optional[Callable[[Any], Any]] = None) -> Dict[str, Any]:
    """
    Linear Search: O(N) sequential scan.
    
    Time: O(1) best-case, O(N) worst and average case.
    Space: O(1) auxiliary.
    """
    t0 = time.perf_counter()
    k_fn = key if key is not None else _default_key
    comparisons = 0
    found_idx = -1
    found_item = None

    for i in range(len(arr)):
        comparisons += 1
        if k_fn(arr[i]) == target:
            found_idx = i
            found_item = arr[i]
            break

    t1 = time.perf_counter()
    return {
        "algorithm": "Linear Search",
        "found": found_idx != -1,
        "index": found_idx,
        "item": found_item,
        "comparisons": comparisons,
        "time_ms": round((t1 - t0) * 1000, 4)
    }


def binary_search(arr: List[Any], target: Any, key: Optional[Callable[[Any], Any]] = None) -> Dict[str, Any]:
    """
    Binary Search: O(log N) logarithmic halving on pre-sorted array.
    
    Time: O(1) best-case, O(log N) worst and average case.
    Space: O(1) iterative auxiliary.
    """
    t0 = time.perf_counter()
    k_fn = key if key is not None else _default_key
    comparisons = 0
    low = 0
    high = len(arr) - 1
    found_idx = -1
    found_item = None

    while low <= high:
        mid = (low + high) // 2
        mid_val = k_fn(arr[mid])
        comparisons += 1

        if mid_val == target:
            found_idx = mid
            found_item = arr[mid]
            break
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1

    t1 = time.perf_counter()
    return {
        "algorithm": "Binary Search",
        "found": found_idx != -1,
        "index": found_idx,
        "item": found_item,
        "comparisons": comparisons,
        "time_ms": round((t1 - t0) * 1000, 4)
    }


def compare_search_performance(arr_sorted: List[Any], target: Any, key: Optional[Callable[[Any], Any]] = None) -> Dict[str, Any]:
    """
    Direct head-to-head comparison between Linear and Binary search on SKU lookups.
    """
    lin_res = linear_search(arr_sorted, target, key)
    bin_res = binary_search(arr_sorted, target, key)

    return {
        "target": target,
        "array_size": len(arr_sorted),
        "linear_search": lin_res,
        "binary_search": bin_res,
        "comparison_ratio": f"{lin_res['comparisons']} vs {bin_res['comparisons']} (Binary is {round(lin_res['comparisons'] / max(1, bin_res['comparisons']), 1)}x fewer comparisons)"
    }
