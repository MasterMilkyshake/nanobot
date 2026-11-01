"""Tissue map: the 2D grid the nanobot moves through."""

from dataclasses import dataclass

Cell = tuple[int, int]  # (row, col)


@dataclass
class TissueMap:
    rows: int
    cols: int
    blocked: set[Cell]
    start: Cell   # injection site
    target: Cell  # tumor

    @classmethod
    def from_ascii(cls, text: str) -> "TissueMap":
        """Legend: '.' open, '#' blocked, 'S' injection site, 'T' tumor."""
        lines = [line.strip() for line in text.strip().splitlines()]
        if len({len(line) for line in lines}) != 1:
            raise ValueError("all map rows must be the same length")

        blocked, start, target = set(), None, None
        for r, line in enumerate(lines):
            for c, ch in enumerate(line):
                if ch == "#":
                    blocked.add((r, c))
                elif ch == "S":
                    start = (r, c)
                elif ch == "T":
                    target = (r, c)
                elif ch != ".":
                    raise ValueError(f"unknown map symbol {ch!r} at row {r}, col {c}")
        if start is None or target is None:
            raise ValueError("map needs one 'S' and one 'T'")
        return cls(len(lines), len(lines[0]), blocked, start, target)

    def is_open(self, cell: Cell) -> bool:
        r, c = cell
        return 0 <= r < self.rows and 0 <= c < self.cols and cell not in self.blocked

    def render(self, path: list[Cell] = ()) -> str:
        """Draw the map, marking the path with '*'."""
        on_path = set(path)
        rows = []
        for r in range(self.rows):
            row = ""
            for c in range(self.cols):
                cell = (r, c)
                if cell == self.start:
                    row += "S"
                elif cell == self.target:
                    row += "T"
                elif cell in self.blocked:
                    row += "#"
                elif cell in on_path:
                    row += "*"
                else:
                    row += "."
            rows.append(row)
        return "\n".join(rows)
