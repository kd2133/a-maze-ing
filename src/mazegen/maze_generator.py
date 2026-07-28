import random
import sys
logo_42 = [
    [1, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1, 1]
]


class Cell:
    """Represents a single cell within the grid.

    Attributes:
        y: The y-coordinate (row) of the cell within the grid.
        x: The x-coordinate (column) of the cell within the grid.
        walls: A dictionary indicating whether the wall is closed (True)
            or open (False) for each cardinal direction.
        visited: Indicates if the cell was visited by DFS algorithm.
        is_logo: True if cell is part of the logo.
        is_path: True if the cell is part of the solution path.
    """
    def __init__(self, y: int, x: int) -> None:
        """Initializes a new cell with closed walls.

        Args:
            y: The coordinate (row) of the cell within the grid.
            x: The coordinate (column) of the cell within the grid.
        """
        self.x = x
        self.y = y
        self.walls = {'N': True, 'E': True, 'S': True, 'W': True}
        self.visited = False
        self.is_logo = False
        self.is_path = False
    
    def __repr__(self) -> str:
        return f"Cell({self.y},{self.x})"


class MazeGenerator:
    """Reusable maze generation module.

    This module provides the MazeGenerator class, which can be imported and used
    in other projects to generate a maze.

    Example:
        from mazegen import MazeGenerator
        from mazegen import bfs

        maze = MazeGenerator(
            width=20,
            height=20,
            entry_pos=(0, 0),
            exit_pos=(0, 0),
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
        perfect: If True, the maze has a single solution path
        seed: Optional seed for reproducible generation

    Accessing the result:
        - maze.grid contains generated maze as a 2D list of Cell objects.
        - bfs(maze) returns the solution path as a list of cardinal directions.
    """
    def __init__(
        self, width: int, height: int, entry_pos: tuple[int, int],
        exit_pos: tuple[int, int], perfect: bool,
        seed: int | None = None
    ) -> None:
        """Initializes MazeGenerator() and creates a maze.

        Args:
            width: Width of the labyrinth (amount of columns).
            height: Height of the labyrinth (amount of rows).
            entry_pos: Entry coordinates of the solver as (x, y).
            exit_pos: Exit coordinates of the solver as (x, y).
            seed: Seed for reproducibility.
            perfect: If True the maze has only one solution path.
                If False, additional walls will be removed to
                create alternative solution paths

        Raises:
            ValueError: If width or height too little,
                entry and exit identical or outside the grid.
        """
        if width <= 2 or height <= 2:
            raise ValueError(
                f"Height/ Width must be higher than 2, "
                f"height: {height}, width: {width}"
            )
        if entry_pos == exit_pos:
            raise ValueError(
                f"Entry/ exit can't be equal, "
                f"entry: {entry_pos}, exit: {exit_pos}"
            )
        x, y = entry_pos
        if x < 0 or x >= width or y < 0 or y >= height:
            raise ValueError(f"Entry {entry_pos} outside the maze.")
        x, y = exit_pos
        if x < 0 or x >= width or y < 0 or y >= height:
            raise ValueError(f"Exit {exit_pos} outside the maze.")
        self.width = width
        self.height = height
        self.entry = entry_pos
        self.exit = exit_pos
        self.perfect = perfect
        self.seed = random.Random(seed)
        self.grid: list[list[Cell]] = []
        self.generate_maze()

    def generate_maze(self) -> None:
        """Controls generation process."""
        self.build_grid()
        self.apply_logo()
        self.validate_logo_entry_exit()
        self.dfs()
        if not self.perfect:
            self.perfect_false()

    def build_grid(self) -> None:
        """Creates grid containing cell objects based on height and width."""
        grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(Cell(y, x))
            grid.append(row)
        self.grid = grid

    def get_neighbors(self, cell: Cell) -> dict[str, Cell]:
        """Determine all neighbors of a cell.

        Args:
            cell: The cell of which the neighbors are looked for.

        Returns:
            A dictionary that has the cardinal direction (key)
            and the position (value) of the neigbors.
        """
        y = cell.y
        x = cell.x
        neighbors = {}

        if y > 0:
            neighbors['N'] = self.grid[y - 1][x]
        if x < self.width - 1:
            neighbors['E'] = self.grid[y][x + 1]
        if y < self.height - 1:
            neighbors['S'] = self.grid[y + 1][x]
        if x > 0:
            neighbors['W'] = self.grid[y][x - 1]
        return neighbors

    def get_unvisited_neighbors(self, cell: Cell) -> dict[str, Cell]:
        """Specifically used in DFS, searches for neighbors that were
        neither visited nor are part of the logo.

        Args:
            cell: The cell of which the unvisited neighbors are looked for.

        Returns:
            A dictionary that has the cardinal direction (key)
            and the position (value) of the unvisited neighbors.
        """
        neighbors = self.get_neighbors(cell)
        unvisited_neighbors = {
            key: value for key, value in neighbors.items()
            if not value.visited and not value.is_logo
        }
        return unvisited_neighbors

    def set_walls(
        self, current_cell: Cell, next_cell: Cell, bool_var: bool
    ) -> None:
        """Sets or removes the wall between two neighboring cells.

        Args:
            current_cell: The current cell.
            next_cell: The neighbor cell.
            bool_var: True sets the wall - False removes the wall.
        """
        if current_cell.y - 1 == next_cell.y:
            current_cell.walls['N'] = bool_var
            next_cell.walls['S'] = bool_var
        elif current_cell.x + 1 == next_cell.x:
            current_cell.walls['E'] = bool_var
            next_cell.walls['W'] = bool_var
        elif current_cell.y + 1 == next_cell.y:
            current_cell.walls['S'] = bool_var
            next_cell.walls['N'] = bool_var
        elif current_cell.x - 1 == next_cell.x:
            current_cell.walls['W'] = bool_var
            next_cell.walls['E'] = bool_var

    def apply_logo(self) -> None:
        """Applies the logo to the grid, if enough room.
        Sets 'cell.is_logo' to True.
        """
        margin = 2
        logo = logo_42
        logo_h = len(logo)
        logo_w = len(logo[0])
        logo_fits = (
            self.width >= logo_w + margin * 2
            and self.height >= logo_h + margin * 2
        )
        if not logo_fits:
            print("Config to small for 42 Logo!", file=sys.stderr)
            return
        start_x = int((self.width - logo_w) / 2)
        start_y = int((self.height - logo_h) / 2)
        for y in range(logo_h):
            for x in range(logo_w):
                if logo_42[y][x] == 1:
                    self.grid[start_y + y][start_x + x].is_logo = True

    def validate_logo_entry_exit(self) -> None:
        """Validates if entry or exit are on the logo ('cell.is_logo = True').

        Raises:
            ValueError: If entry or exit are on the logo.
        """
        x, y= self.entry
        if self.grid[y][x].is_logo:
            raise ValueError("Entry can't be on logo")
        x, y = self.exit
        if self.grid[y][x].is_logo:
            raise ValueError("Exit can't be on logo")

    def dfs(self) -> None:
        """Generates paths in the grid, making it a maze."""
        stack = [self.grid[0][0]]
        while stack:
            current = stack[-1]
            current.visited = True
            neighbors = self.get_unvisited_neighbors(current)
            if neighbors:
                neighbor = self.seed.choice(list(neighbors.values()))
                self.set_walls(current, neighbor, False)
                stack.append(neighbor)
            else:
                stack.pop()

    def is_3x3(self, cell: Cell) -> bool:
        """Checks if there is an open 3x3 area (no interior walls).

        Args:
            cell: Upper left cell of the 3x3 area to be checked.

        Returns:
            True, if the area has no interior walls.
        """
        y = cell.y
        x = cell.x
        is_3x3 = [
            self.grid[y][x].walls['E'], self.grid[y][x + 1].walls['E'],
            self.grid[y][x].walls['S'], self.grid[y][x + 1].walls['S'],
            self.grid[y][x + 2].walls['S'],
            self.grid[y + 1][x + 2].walls['S'],
            self.grid[y + 1][x].walls['E'],
            self.grid[y + 1][x + 1].walls['E'],
            self.grid[y + 1][x].walls['S'],
            self.grid[y + 1][x + 1].walls['S'],
            self.grid[y + 2][x].walls['E'], self.grid[y + 2][x + 1].walls['E']
        ]
        if not any(is_3x3):
            return True
        return False

    def has_3x3(self) -> bool:
        """Searches the entire maze for open 3x3 areas.

        Returns:
            True, if one open 3x3 area is found.
        """
        for y in range(self.height - 2):
            for x in range(self.width - 2):
                if self.is_3x3(self.grid[y][x]):
                    return True
        return False

    def perfect_false(self) -> None:
        """Randomly removes extra walls to open alternative paths.

        30% of the walls will be opened.
        If there is an open 3x3 area, the wall will be placed again.
        """
        neighbors_with_wall = []
        for row in self.grid:
            for cell in row:
                for direction, neighbor in self.get_neighbors(cell).items():
                    if cell.is_logo or neighbor.is_logo:
                        continue
                    if direction in ('E', 'S') and cell.walls[direction]:
                        neighbors_with_wall.append((cell, neighbor))

        self.seed.shuffle(neighbors_with_wall)
        max_removals = int(len(neighbors_with_wall) * 0.3)
        removed_count = 0
        for current, neighbor in neighbors_with_wall:
            if removed_count >= max_removals:
                break
            self.set_walls(current, neighbor, False)
            if self.has_3x3():
                self.set_walls(current, neighbor, True)
            else:
                removed_count += 1
