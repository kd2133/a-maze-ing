"""Reusable maze generation module.

This module provides the MazeGenerator class, which can be imported and
used in other projects to generate a maze.

Example:
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

Parameters:
    width: Number of columns in the maze.
    height: Number of rows in the maze.
    entry_pos: Entry coordinates (x, y).
    exit_pos: Exit coordinates (x, y).
    perfect: If True, the maze has a single solution path.
    seed: Optional seed for reproducible generation.

Accessing the result:
    maze.grid is a 2D list of Cell objects (maze.grid[y][x])
    Each Cell has:
        - maze.grid[y][x].walls: dict with keys (N, E, S, W) -
            True = wall present.
        - maze.grid[y][x].x / .y: the cell's column and row position.
        - maze.grid[y][x].is_path: True if the cell lies
            on the solved path (after bfs()).
        - maze.grid[y][x].is_logo: True if the cell is
            part of the maze's logo pattern.

    Note: entry_pos/exit_pos use (x, y) order when passed in, but
        grid access uses [y][x] order, matching standard indexing.

    - bfs(maze) returns the solution path as a list of cardinal directions.
"""
from .maze_generator import MazeGenerator, Cell
from .maze_solver import bfs

__all__ = ["MazeGenerator", "Cell", "bfs"]
