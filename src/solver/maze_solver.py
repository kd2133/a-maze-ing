from collections import deque
from src.generator.maze_generator import MazeGenerator, Cell


class MazeSolver:
    def __init__(self, maze: MazeGenerator) -> None:
        self.maze = maze

    def get_open_neighbors(self, cell: Cell) -> dict[str, Cell]:
        neighbors = self.maze.get_neighbors(cell)
        return {
            direction: neighbor
            for direction, neighbor in neighbors.items()
            if not cell.walls[direction]
        }

    def bfs(self) -> list[str]:
        start_y, start_x = self.maze.entry
        end_y, end_x = self.maze.exit
        start = self.maze.grid[start_y][start_x]
        end = self.maze.grid[end_y][end_x]

        queue = deque([start])
        came_from: dict[Cell, tuple[Cell, str]] = {}
        visited = {start}

        while queue:
            current = queue.popleft()
            if current is end:
                return self._reconstruct_path(came_from, start, end)

            for direction, neighbor in self.get_open_neighbors(current).items():
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = (current, direction)
                    queue.append(neighbor)

        raise ValueError("Kein Pfad zwischen Entry und Exit gefunden.")

    def _reconstruct_path(
        self,
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