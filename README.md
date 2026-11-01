# nanobot

A small computational simulator for a therapeutic nanobot. The nanobot starts at an
injection site and finds the **shortest path** through tissue to a tumor, going
around anything it can't pass through. This is a starting point for work aligned
with the Dogra Lab (USC Mann School of Pharmacy).

## Layout

```
src/nanobot/
  tissue.py      # TissueMap: grid of open / blocked cells, start (S), tumor (T)
  pathfinder.py  # shortest_path(): A* search
examples/find_tumor.py
tests/test_pathfinder.py
```

## How it works

- The tissue is a 2D grid: `.` open, `#` blocked, `S` injection site, `T` tumor.
- The nanobot can move in 8 directions. A straight step costs 1 and a diagonal step costs √2.
  It can't cut diagonally past a blocked corner.
- A* search uses the octile distance as its heuristic, so the path it returns is
  guaranteed to be the shortest.

## Run

```bash
python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"
.venv/bin/python examples/find_tumor.py
.venv/bin/python -m pytest
```
