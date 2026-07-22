"""Find the lowest-cost route through a weighted graph."""

from __future__ import annotations

import heapq
from dataclasses import dataclass
from math import inf


@dataclass(frozen=True)
class RouteResult:
    """The completed path and its total cost."""

    path: list[str]
    total_cost: float


class WeightedGraph:
    """An adjacency-list implementation of a weighted directed graph."""

    def __init__(self) -> None:
        self._edges: dict[str, list[tuple[str, float]]] = {}

    def add_edge(
        self,
        start: str,
        destination: str,
        cost: float,
        *,
        bidirectional: bool = False,
    ) -> None:
        """Add a weighted edge between two nodes."""

        if not start or not destination:
            raise ValueError("Node names cannot be empty.")

        if cost < 0:
            raise ValueError("Dijkstra's algorithm requires nonnegative costs.")

        self._edges.setdefault(start, []).append((destination, cost))
        self._edges.setdefault(destination, [])

        if bidirectional:
            self._edges[destination].append((start, cost))

    def shortest_path(self, start: str, destination: str) -> RouteResult | None:
        """Find the least expensive route using Dijkstra's algorithm."""

        if start not in self._edges:
            raise KeyError(f"Unknown starting node: {start}")

        if destination not in self._edges:
            raise KeyError(f"Unknown destination node: {destination}")

        distances = {node: inf for node in self._edges}
        previous: dict[str, str | None] = {
            node: None for node in self._edges
        }

        distances[start] = 0.0

        # Each heap entry is stored as (distance, node).
        priority_queue: list[tuple[float, str]] = [(0.0, start)]

        while priority_queue:
            current_cost, current_node = heapq.heappop(priority_queue)

            # Ignore outdated heap entries created before a shorter path
            # to this node was discovered.
            if current_cost > distances[current_node]:
                continue

            if current_node == destination:
                break

            for neighbor, edge_cost in self._edges[current_node]:
                new_cost = current_cost + edge_cost

                if new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    previous[neighbor] = current_node
                    heapq.heappush(
                        priority_queue,
                        (new_cost, neighbor),
                    )

        if distances[destination] == inf:
            return None

        path = self._reconstruct_path(
            previous=previous,
            destination=destination,
        )

        return RouteResult(
            path=path,
            total_cost=distances[destination],
        )

    @staticmethod
    def _reconstruct_path(
        previous: dict[str, str | None],
        destination: str,
    ) -> list[str]:
        """Walk backward through the previous-node mapping."""

        path: list[str] = []
        current: str | None = destination

        while current is not None:
            path.append(current)
            current = previous[current]

        path.reverse()
        return path


def main() -> None:
    graph = WeightedGraph()

    graph.add_edge("Garage", "Fuel Station", 3.2, bidirectional=True)
    graph.add_edge("Garage", "Tire Area", 2.0, bidirectional=True)
    graph.add_edge("Tire Area", "Inspection", 2.3, bidirectional=True)
    graph.add_edge("Fuel Station", "Inspection", 1.4, bidirectional=True)
    graph.add_edge("Inspection", "Pit Lane", 1.8, bidirectional=True)
    graph.add_edge("Tire Area", "Pit Lane", 5.0, bidirectional=True)

    result = graph.shortest_path("Garage", "Pit Lane")

    if result is None:
        print("No available route.")
        return

    print("Route:", " -> ".join(result.path))
    print(f"Total cost: {result.total_cost:.1f}")


if __name__ == "__main__":
    main()