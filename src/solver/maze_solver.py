from collections import deque
from src.generator.maze_generator import MazeGenerator, Cell


def get_open_neighbors(maze: MazeGenerator, cell: Cell) -> dict[str, Cell]:
    neighbors = maze.get_neighbors(cell)
    return {
        direction: neighbor
        for direction, neighbor in neighbors.items()
        if not cell.walls[direction]
    }


def bfs(maze: MazeGenerator) -> list[str]:
    start_y, start_x = maze.entry
    end_y, end_x = maze.exit
    start = maze.grid[start_y][start_x]
    end = maze.grid[end_y][end_x]
    queue = deque([start])
    came_from: dict[Cell, tuple[Cell, str]] = {}
    visited = {start}
    while queue:
        current = queue.popleft()
        if current is end:
            return _reconstruct_path(came_from, start, end)
        for direction, neighbor in get_open_neighbors(maze, current).items():
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = (current, direction)
                queue.append(neighbor)
    raise ValueError("couldn't find path between entry and exit")


def _reconstruct_path(
    came_from: dict[Cell, tuple[Cell, str]],
    start: Cell,
    end: Cell,
) -> list[str]:
    path: list[str] = []
    current = end
    while current is not start:
        current, direction = came_from[current]
        path.append(direction)
    path.reverse()
    return path