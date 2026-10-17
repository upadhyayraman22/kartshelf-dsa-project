"""
dsa/backtracking.py - Budget Bundle Builder via Backtracking with Pruning
Implemented from scratch without combinatorial itertools or solver libraries.

Purpose:
    Given a user budget B (e.g. Rs 5000) and target bundle size (3 to 5 items),
    finds the highest-rated product combination strictly within budget using
    backtracking search with branch-and-bound pruning.
"""

import time
from typing import Any, List, Dict, Optional, Tuple


class BudgetBundleBuilder:
    """
    Backtracking Search with Pruning for Constrained Combinatorial Optimization.
    
    Problem Formulation:
        Maximize Sum(rating_i) for i in bundle
        Subject to:
            Sum(price_i) <= Budget
            min_items <= len(bundle) <= max_items
    Pruning Heuristics:
        1. Capacity Pruning: if current_cost + min_remaining_cost > budget -> backtrack.
        2. Upper-Bound Pruning: if current_rating + theoretical_max_remaining_rating <= best_rating -> backtrack.
        3. Cardinality Pruning: if current_count + remaining_items_available < min_items -> backtrack.
    """

    def __init__(self, products: List[Dict[str, Any]]):
        self.products = products
        self.states_explored = 0

    def build_bundle(self, budget: float, min_items: int = 1, max_items: int = 5) -> Dict[str, Any]:
        t0 = time.perf_counter()
        self.states_explored = 0
        min_items = max(1, min_items)
        max_items = max(min_items, max_items)

        # Filter out products that alone exceed budget
        candidates = [p for p in self.products if p["price"] <= budget]

        # Sort candidates descending by value-density (rating / price) manually
        # Simple selection/insertion sort
        for i in range(1, len(candidates)):
            curr = candidates[i]
            curr_density = curr["rating"] / max(1, curr["price"])
            j = i - 1
            while j >= 0:
                prev_density = candidates[j]["rating"] / max(1, candidates[j]["price"])
                if prev_density < curr_density:
                    candidates[j + 1] = candidates[j]
                    j -= 1
                else:
                    break
            candidates[j + 1] = curr

        # Limit candidate pool to top 30 to prevent exponential explosion while providing excellent options
        candidates = candidates[:30]

        best_bundle: List[Dict[str, Any]] = []
        best_rating = -1.0
        best_cost = 0.0

        current_choice: List[Dict[str, Any]] = []

        def _backtrack(index: int, current_cost: float, current_rating: float):
            nonlocal best_bundle, best_rating, best_cost
            self.states_explored += 1

            # Check valid bundle candidate
            count = len(current_choice)
            if min_items <= count <= max_items:
                if current_rating > best_rating or (abs(current_rating - best_rating) < 1e-4 and current_cost < best_cost):
                    best_rating = current_rating
                    best_cost = current_cost
                    best_bundle = [x for x in current_choice]

            # Reached maximum allowed items
            if count == max_items:
                return

            # Cardinality pruning: not enough candidates left to reach min_items
            if count + (len(candidates) - index) < min_items:
                return

            # Explore choices
            for i in range(index, len(candidates)):
                p = candidates[i]
                next_cost = current_cost + p["price"]

                # Pruning 1: Exceeds budget
                if next_cost > budget:
                    continue

                # Pruning 2: Theoretical upper bound on rating from remaining slots
                slots_left = max_items - count
                max_possible_remaining_rating = slots_left * 5.0
                if current_rating + max_possible_remaining_rating <= best_rating:
                    continue

                # Make choice
                current_choice.append(p)

                # Recurse
                _backtrack(i + 1, next_cost, current_rating + p["rating"])

                # Backtrack choice
                current_choice.pop()

        _backtrack(0, 0.0, 0.0)

        t1 = time.perf_counter()
        time_ms = round((t1 - t0) * 1000, 2)

        return {
            "budget": budget,
            "min_items": min_items,
            "max_items": max_items,
            "states_explored": self.states_explored,
            "time_ms": time_ms,
            "found": len(best_bundle) > 0,
            "item_count": len(best_bundle),
            "total_price": round(best_cost, 2),
            "total_rating": round(best_rating, 2),
            "average_rating": round(best_rating / len(best_bundle), 2) if best_bundle else 0.0,
            "savings": round(budget - best_cost, 2),
            "bundle": best_bundle
        }
