*This project has been created as part of the 42 curriculum by kdakovic, nkerstin.*

# A-Maze-ing

## Description

**A-Maze-ing** is a Python maze generator. From a plain-text configuration
file, it generates a maze on a rectangular grid, guarantees it is fully
connected, embeds a visible **"42"** pattern made of closed-off cells, and
writes the result to a file using a compact hexadecimal wall encoding.

The maze can be generated as a *perfect* maze (exactly one path between
entry and exit) or as an *imperfect* maze (extra walls removed to create
loops and alternative paths, while never creating an open area wider than
2 cells). The result is displayed as colored ASCII art directly in the
terminal, together with a small interactive menu to regenerate the maze,
show/hide the shortest solution path, and cycle through wall colors.

The generation logic itself is packaged as a separate, reusable,
pip-installable module (`mazegen`, see below) so it can be reused in other
projects without the CLI/display code.

## Instructions

Requirements: **Python 3.10+**. The project has no external runtime
dependencies.

```sh
# install (no-op, project has zero runtime dependencies)
make install

# run the program with the default config.txt
make run
# equivalent to:
python3 a_maze_ing.py config.txt

# run the program with a custom config file
python3 a_maze_ing.py path/to/your_config.txt

# run the main script under Python's debugger (pdb)
make debug

# remove __pycache__, .mypy_cache and the generated output file
make clean

# lint: flake8 + mypy (mandatory flags)
make lint

# lint: flake8 + mypy --strict
make lint-strict
```

Once running, the program shows the maze and a small menu:

```
=== A-Maze-ing ===
1. Re-generate a new maze
2. Show/Hide path from entry to exit
3. Rotate maze colors
4. Quit
```

The current entry cell, exit cell, wall color, and the "42" pattern are
each displayed in a distinct color; the shortest solution path can be
toggled on/off with option 2.

## Configuration file format

The configuration file is a plain text file with one `KEY=VALUE` pair per
line. Lines starting with `#` are treated as comments and ignored, as are
blank lines. Keys are case-insensitive.

| Key           | Required | Description                              | Example                 |
|---------------|----------|-------------------------------------------|-------------------------|
| `WIDTH`       | yes      | Maze width, in cells                      | `WIDTH=20`              |
| `HEIGHT`      | yes      | Maze height, in cells                     | `HEIGHT=15`             |
| `ENTRY`       | yes      | Entry coordinates, `x,y`                  | `ENTRY=0,0`             |
| `EXIT`        | yes      | Exit coordinates, `x,y`                   | `EXIT=19,14`            |
| `OUTPUT_FILE` | yes      | Path of the generated output file         | `OUTPUT_FILE=maze.txt`  |
| `PERFECT`     | yes      | `True`/`False` — single path if `True`    | `PERFECT=True`          |
| `SEED`        | no       | Integer seed, for reproducible mazes      | `SEED=42`               |

Example `config.txt`:

```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

Any missing required key, unknown key, or malformed line is rejected with
a clear error message and a non-zero exit code — the program never
crashes on bad input.

### Output file format

The output file contains the maze grid, one hexadecimal digit per cell,
one row per line. Each digit encodes which of the 4 walls of that cell
are **closed** (bit = 1) as a bitmask:

| Bit (LSB→MSB) | Direction |
|---------------|-----------|
| 0             | North     |
| 1             | East      |
| 2             | South     |
| 3             | West      |

After the grid, a blank line separates it from 3 final lines: the entry
coordinates (`x,y`), the exit coordinates (`x,y`), and the shortest path
from entry to exit as a string of `N`/`E`/`S`/`W` letters.

## Maze generation algorithm

The maze is generated with an **iterative Depth-First Search (a
"recursive backtracker", implemented with an explicit stack instead of
recursion)**:

1. A grid of fully-walled cells is built, and the "42" pattern cells are
   marked as excluded from generation (they stay isolated, all 4 walls
   closed).
2. Starting from the top-left cell, the algorithm repeatedly moves to a
   random unvisited, non-logo neighbor, removing the wall between the two
   cells, and backtracks (via the stack) whenever a cell has no unvisited
   neighbor left.
3. If `PERFECT=False`, a post-processing pass (`perfect_false`) randomly
   opens up to 30% of the remaining walls between non-logo cells,
   re-closing any wall whose removal would create an open 3×3 area, so
   corridors never become wider than 2 cells.
4. The shortest path from entry to exit is then computed with a
   **Breadth-First Search (BFS)** over the open walls.

### Why this algorithm

- DFS carving is, by construction, a **spanning tree** of the grid: it
  visits every reachable cell exactly once and never creates a cycle.
  That means a DFS-generated maze is automatically a *perfect* maze
  (exactly one path between any two cells) without any extra work — it
  matches the `PERFECT` requirement directly.
- It produces long, winding corridors with comparatively few branch
  points, which tends to look and play more "maze-like" than algorithms
  with a more uniform branching factor (e.g. plain randomized Prim's).
- The **iterative** version (explicit stack) avoids Python's recursion
  depth limit, which a naive recursive backtracker would hit on larger
  mazes.
- Starting from a perfect maze and only *removing extra walls afterward*
  keeps "perfect" and "imperfect" generation cleanly separated: the core
  carving logic doesn't need to know about the `PERFECT` flag at all.
- BFS is the natural choice to find the *shortest* path once the maze
  exists, since all edges (open walls) have equal weight.

## Reusable `mazegen` module

The maze generation logic (and the solver) lives in `src/mazegen/`, a
self-contained package with no dependency on the CLI, config parsing, or
terminal display code. It is built and distributed as a standalone,
pip-installable package (see `pyproject.toml`), independent from the rest
of this repository.

**Building the package** (from the repository root):

```sh
python3 -m venv venv
source venv/bin/activate
pip install build
python3 -m build
```

**Installing** it in any other project:

```sh
pip install mazegen-1.0.0-py3-none-any.whl
```

**Overall** (`mazegen/__init__.py`) — *Reusable maze generation module.*
This module provides the `MazeGenerator` class, which can be imported and
used in other projects to generate a maze. It exposes two public symbols:
the `MazeGenerator` class (below) and the `bfs` solver.

### `MazeGenerator` (generator)

```python
from mazegen import MazeGenerator
from mazegen import bfs

maze = MazeGenerator(
    width=20,
    height=20,
    entry_pos=(0, 0),
    exit_pos=(19, 19),
    perfect=True,
    seed=42,
)

# Access the generated structure
grid = maze.grid

# Access a solution path from entry to exit
solution = bfs(maze)
```

**Parameters:**

- `width`: Number of columns in the maze.
- `height`: Number of rows in the maze.
- `entry_pos`: Entry coordinates (x, y).
- `exit_pos`: Exit coordinates (x, y).
- `perfect`: If True, the maze has a single solution path.
- `seed`: Optional seed for reproducible generation.

**Accessing the result:**

`maze.grid` is a 2D list of `Cell` objects (`maze.grid[y][x]`). Each `Cell`
has:

- `maze.grid[y][x].walls`: dict with keys (N, E, S, W) — True = wall present.
- `maze.grid[y][x].x` / `.y`: the cell's column and row position.
- `maze.grid[y][x].is_path`: True if the cell lies on the solved path
  (after `bfs()`).
- `maze.grid[y][x].is_logo`: True if the cell is part of the maze's logo
  pattern.

> **Note:** `entry_pos`/`exit_pos` use `(x, y)` order when passed in, but
> grid access uses `[y][x]` order, matching standard indexing.

### `bfs` (solver)

> Find the shortest path from maze's entry to exit.
>
> Uses breadth-first search and sets every cell on the path to
> `is_path = True`.

- **Args:** `maze` — a `MazeGenerator` instance.
- **Returns:** a list of cardinal directions (`N`/`E`/`S`/`W`) to walk from
  entry to exit.
- **Raises:** `ValueError` if no path exists between entry and exit.

`MazeGenerator` and `Cell` are defined in `mazegen/maze_generator.py`,
and the `bfs` solver in `mazegen/maze_solver.py`; both are re-exported
from `mazegen/__init__.py`.

This is also the only part of the codebase that is reusable/importable
independently of this project; everything else (`src/config`,
`src/export`, `src/ui`, `a_maze_ing.py`) is specific to this CLI
application and depends on the `mazegen` package, not the other way
around.

## Resources

- [Maze generation algorithm — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [BFS, DFS Youtube video — YouTube](https://www.youtube.com/watch?v=cS-198wtfj0)
- [Python Packaging User Guide](https://packaging.python.org/) — building
  and installing the `mazegen` wheel with `build`/`setuptools`

**AI usage:** AI assistance (Claude / Claude Code) was used during this
project to review the codebase against the subject's requirements —
running edge-case test batteries (config parsing, constructor validation,
wall-coherence checks, "no open 3×3 area" checks, connectivity checks,
seed reproducibility), verifying `flake8`/`mypy` compliance, and
cross-checking the implementation against public 42 `a_maze_ing`
repositories for comparison. It was not used to generate the core
generation/solving logic or the docstrings, which were written by hand.

## Team and project management

**Roles:** 
- ***kdakovic:***
  - MazeGenerator
  - Parser
  - HexExport
  - Standalone module

- ***nkerstin:***
  - Solver
  - Display
  - Makefile
  - README

- ***Both:***
  - Main
  - Planning
  - Testing
  - DevOps
  - Project-Setup

**Anticipated planning and how it evolved until the end:**

- We had a MazeConfig class that was used as param for the MazeGenerator class, which would have prevented the reusability of the standalone mazegen package.

**What worked well and what could be improved:**

- Planing a project from top to bottom (function hierarchy). 

**Have you used any specific tools? Which ones?**
- VS Code
- Claude (see AI usage)
- Github