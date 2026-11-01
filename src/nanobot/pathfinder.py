"""A* search for the shortest path from the injection site to the tumor."""

import heapq
import math

from .tissue import Cell, TissueMap

# 8 directions: straight steps cost 1, diagonal steps cost sqrt(2)
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]


def octile_distance(a: Cell, b: Cell) -> float:
    """Shortest possible length between two cells on an open 8-direction grid."""
    dr, dc = abs(a[0] - b[0]), abs(a[1] - b[1])
    return max(dr, dc) + (math.sqrt(2) - 1) * min(dr, dc)


def shortest_path(tissue: TissueMap) -> tuple[list[Cell], float] | None:
    """Return (path, length) of the shortest route from start to target, or None if unreachable."""
    start, goal = tissue.start, tissue.target
    best = {start: 0.0}
    came_from: dict[Cell, Cell] = {}
    frontier = [(octile_distance(start, goal), 0.0, start)]

    while frontier:
        _, cost, cell = heapq.heappop(frontier)
        if cell == goal:
            return _rebuild(came_from, cell), cost
        if cost > best[cell]:
            continue  # stale entry, a shorter route to this cell was already found

        r, c = cell
        for dr, dc in MOVES:
            nxt = (r + dr, c + dc)
            if not tissue.is_open(nxt):
                continue
            diagonal = dr != 0 and dc != 0
            if diagonal and not (tissue.is_open((r + dr, c)) and tissue.is_open((r, c + dc))):
                continue  # no cutting corners past a blocked cell
            new_cost = cost + (math.sqrt(2) if diagonal else 1.0)
            if new_cost < best.get(nxt, math.inf):
                best[nxt] = new_cost
                came_from[nxt] = cell
                heapq.heappush(frontier, (new_cost + octile_distance(nxt, goal), new_cost, nxt))
    return None


def _rebuild(came_from: dict[Cell, Cell], cell: Cell) -> list[Cell]:
    path = [cell]
    while cell in came_from:
        cell = came_from[cell]
        path.append(cell)
    return path[::-1]
