"""Find the shortest route from the injection site (S) to the tumor (T)."""

from nanobot import TissueMap, shortest_path

TISSUE = """
S.......#...........
.######.#.#########.
......#.#.#.......#.
.####.#...#.#####.#.
....#.#####.#.T.#.#.
.##.#.......#...#.#.
..#.#########.###.#.
..#...............#.
"""

tissue = TissueMap.from_ascii(TISSUE)
result = shortest_path(tissue)

if result is None:
    print("No path: the tumor is unreachable.")
else:
    path, length = result
    print(tissue.render(path))
    print(f"\nShortest path length: {length:.2f} cells ({len(path) - 1} moves)")
