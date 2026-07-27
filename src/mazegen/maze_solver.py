from collections import deque
from src.mazegen import MazeGenerator, Cell


def get_open_neighbors(maze: MazeGenerator, cell: Cell) -> dict[str, Cell]:
    """Return the neighbors of a cell that are reachable (no walls)."""
    neighbors = maze.get_neighbors(cell)
    return {
        direction: neighbor
        for direction, neighbor in neighbors.items()
        if not cell.walls[direction]
    }


def bfs(maze: MazeGenerator) -> list[str]:
    """Find the shortest path from maze's entry to exit.

    Uses breadth-first search and sets every cell on the path
    to 'is_path = True'.

    Args:
        maze: MazeGenerator instance.

    Returns:
        A list of cardinal directions to walk from entry to exit.

    Raises:
        ValueError: If no path exists between entry and exit.
    """
    start_x, start_y = maze.entry
    end_x, end_y = maze.exit
    start = maze.grid[start_y][start_x]
    end = maze.grid[end_y][end_x]
    queue = deque([start])
    came_from: dict[Cell, tuple[Cell, str]] = {}
    visited = {start}
    while queue:
        current = queue.popleft()
        if current is end:
            return gen_path_list(came_from, start, end)
        for direction, neighbor in get_open_neighbors(maze, current).items():
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = (current, direction)
                queue.append(neighbor)
    raise ValueError("Couldn't find path between entry and exit")


def gen_path_list(
    came_from: dict[Cell, tuple[Cell, str]],
    start: Cell,
    end: Cell,
) -> list[str]:
    """Reconstruct the path from start to end using the came_from dict.

    Sets each cell on the path to 'is_path = True'.

    """
    path: list[str] = []
    current = end
    while current is not start:
        current, direction = came_from[current]
        current.is_path = True
        path.append(direction)
    path.reverse()
    return path
