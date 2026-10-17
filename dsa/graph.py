"""
dsa/graph.py - Graph Data Structures & Algorithms
Implemented from scratch with Adjacency List, Adjacency Matrix, BFS, DFS,
Shortest Hop Path, Connected Components, Prim's MST, and Kruskal's MST.

Classes:
1. Graph: Dual representation (Adjacency List + Adjacency Matrix).
"""

from typing import Any, List, Dict, Optional, Tuple, Set
from dsa.queue_ds import Queue
from dsa.stack import Stack
from dsa.disjoint_set import DisjointSet


class Edge:
    def __init__(self, u: Any, v: Any, weight: float = 1.0):
        self.u = u
        self.v = v
        self.weight = weight

    def to_dict(self) -> Dict[str, Any]:
        return {"from": self.u, "to": self.v, "weight": self.weight}


class Graph:
    """
    Graph supporting both Adjacency List and Adjacency Matrix representations.
    
    Purpose:
        1. 'Customers also bought' recommendation graph (BFS up to depth 2).
        2. 'Browsing trail' exploration (DFS with explicit Stack).
        3. Shortest hop path between two products (BFS shortest path).
        4. Connected components (product clusters / market categories).
        5. Warehouse delivery network MST (Prim & Kruskal).
    """

    def __init__(self, directed: bool = False):
        self.directed = directed
        self.vertices: List[Any] = []
        self.vertex_indices: Dict[Any, int] = {}
        self.adj_list: Dict[Any, List[Tuple[Any, float]]] = {}
        self.edges: List[Edge] = []
        self.adj_matrix: List[List[float]] = []

    def add_vertex(self, v: Any) -> None:
        if v not in self.vertex_indices:
            idx = len(self.vertices)
            self.vertex_indices[v] = idx
            self.vertices.append(v)
            self.adj_list[v] = []

            # Expand adjacency matrix
            for row in self.adj_matrix:
                row.append(0.0)
            self.adj_matrix.append([0.0] * len(self.vertices))

    def add_edge(self, u: Any, v: Any, weight: float = 1.0) -> None:
        self.add_vertex(u)
        self.add_vertex(v)

        # Adjacency List
        self.adj_list[u].append((v, weight))
        if not self.directed:
            self.adj_list[v].append((u, weight))

        # Adjacency Matrix
        u_idx = self.vertex_indices[u]
        v_idx = self.vertex_indices[v]
        self.adj_matrix[u_idx][v_idx] = weight
        if not self.directed:
            self.adj_matrix[v_idx][u_idx] = weight

        self.edges.append(Edge(u, v, weight))

    def get_neighbors(self, u: Any) -> List[Tuple[Any, float]]:
        return self.adj_list.get(u, [])

    def bfs(self, start_vertex: Any, max_depth: Optional[int] = None) -> List[Tuple[Any, int]]:
        """
        Breadth-First Search using custom Queue.
        Returns list of (vertex, depth).
        Used for 'Customers also bought' at depth 1 and depth 2.
        """
        if start_vertex not in self.vertex_indices:
            return []

        visited = set()
        queue = Queue(500)
        traversal = []

        visited.add(start_vertex)
        queue.enqueue((start_vertex, 0))

        while not queue.is_empty():
            curr, depth = queue.dequeue()
            if curr != start_vertex:
                traversal.append((curr, depth))

            if max_depth is not None and depth >= max_depth:
                continue

            for neighbor, _ in self.adj_list.get(curr, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.enqueue((neighbor, depth + 1))

        return traversal

    def dfs(self, start_vertex: Any) -> List[Any]:
        """
        Depth-First Search using custom explicit Stack.
        Simulates browsing trail through product connections.
        """
        if start_vertex not in self.vertex_indices:
            return []

        visited = set()
        stack = Stack(500)
        traversal = []

        stack.push(start_vertex)

        while not stack.is_empty():
            curr = stack.pop()
            if curr not in visited:
                visited.add(curr)
                traversal.append(curr)

                # Push neighbors in reverse order
                nbrs = self.adj_list.get(curr, [])
                for i in range(len(nbrs) - 1, -1, -1):
                    neighbor, _ = nbrs[i]
                    if neighbor not in visited:
                        stack.push(neighbor)

        return traversal

    def shortest_path(self, start: Any, target: Any) -> Optional[List[Any]]:
        """
        Finds shortest unweighted hop path using BFS with predecessor tracking.
        """
        if start not in self.vertex_indices or target not in self.vertex_indices:
            return None
        if start == target:
            return [start]

        visited = set()
        parent = {}
        queue = Queue(500)

        visited.add(start)
        queue.enqueue(start)

        found = False
        while not queue.is_empty():
            curr = queue.dequeue()
            if curr == target:
                found = True
                break

            for neighbor, _ in self.adj_list.get(curr, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = curr
                    queue.enqueue(neighbor)

        if not found:
            return None

        # Reconstruct path
        path = []
        curr = target
        while curr is not None:
            path.append(curr)
            curr = parent.get(curr, None)

        # Reverse path
        reversed_path = []
        for i in range(len(path) - 1, -1, -1):
            reversed_path.append(path[i])
        return reversed_path

    def connected_components(self) -> List[List[Any]]:
        """
        Finds all connected components (product clusters / market sub-graphs).
        """
        visited = set()
        components = []

        for v in self.vertices:
            if v not in visited:
                comp = []
                queue = Queue(500)
                visited.add(v)
                queue.enqueue(v)

                while not queue.is_empty():
                    curr = queue.dequeue()
                    comp.append(curr)
                    for nbr, _ in self.adj_list.get(curr, []):
                        if nbr not in visited:
                            visited.add(nbr)
                            queue.enqueue(nbr)

                components.append(comp)

        return components

    def prim_mst(self) -> Dict[str, Any]:
        """
        Prim's Algorithm for Minimum Spanning Tree without heapq.
        Time Complexity: O(V^2) or O(E log V).
        """
        if not self.vertices:
            return {"total_cost": 0, "edges": []}

        n = len(self.vertices)
        in_mst = [False] * n
        key = [float('inf')] * n
        parent: List[Optional[int]] = [None] * n

        key[0] = 0.0

        for _ in range(n):
            # Pick min key vertex not in MST
            min_val = float('inf')
            min_u = -1
            for v_idx in range(n):
                if not in_mst[v_idx] and key[v_idx] < min_val:
                    min_val = key[v_idx]
                    min_u = v_idx

            if min_u == -1:
                break

            in_mst[min_u] = True
            u_vertex = self.vertices[min_u]

            for neighbor, weight in self.adj_list.get(u_vertex, []):
                v_idx = self.vertex_indices[neighbor]
                if not in_mst[v_idx] and weight < key[v_idx]:
                    key[v_idx] = weight
                    parent[v_idx] = min_u

        mst_edges = []
        total_cost = 0.0
        for i in range(1, n):
            if parent[i] is not None:
                u_name = self.vertices[parent[i]]
                v_name = self.vertices[i]
                cost = self.adj_matrix[parent[i]][i]
                mst_edges.append({"from": u_name, "to": v_name, "cost": cost})
                total_cost += cost

        return {"algorithm": "Prim", "total_cost": round(total_cost, 2), "edges": mst_edges}

    def kruskal_mst(self) -> Dict[str, Any]:
        """
        Kruskal's Algorithm for MST using DisjointSet.
        Time Complexity: O(E log E) sorting edges + O(E alpha(V)) set operations.
        """
        # Sort edges by weight manually using simple bubble/insertion sort
        sorted_edges = [Edge(e.u, e.v, e.weight) for e in self.edges]
        # Manual insertion sort on edges
        for i in range(1, len(sorted_edges)):
            curr = sorted_edges[i]
            j = i - 1
            while j >= 0 and sorted_edges[j].weight > curr.weight:
                sorted_edges[j + 1] = sorted_edges[j]
                j -= 1
            sorted_edges[j + 1] = curr

        ds = DisjointSet()
        for v in self.vertices:
            ds.make_set(v)

        mst_edges = []
        total_cost = 0.0

        for edge in sorted_edges:
            if ds.union(edge.u, edge.v):
                mst_edges.append({"from": edge.u, "to": edge.v, "cost": edge.weight})
                total_cost += edge.weight

        return {"algorithm": "Kruskal", "total_cost": round(total_cost, 2), "edges": mst_edges}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "Graph",
            "vertex_count": len(self.vertices),
            "edge_count": len(self.edges),
            "vertices": self.vertices[:30],  # sample for visualization
            "adjacency_list": {str(k): [{"to": v, "weight": w} for v, w in nbrs] for k, nbrs in list(self.adj_list.items())[:20]},
            "connected_components_count": len(self.connected_components())
        }
