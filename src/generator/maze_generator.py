import random


logo_42 = [
    [1, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1, 1]
]


class Cell:
    def __init__(self, y: int, x: int) -> None:
        self.x = x
        self.y = y
        self.walls = {'N': True, 'E': True, 'S': True, 'W': True}
        self.visited = False
        self.is_logo = False
        self.is_path = False


class MazeGenerator:
    def __init__(
        self, width: int, height: int, entry_pos: tuple[int, int],
        exit_pos: tuple[int, int], output_file: str,
        seed: int | None, perfect: bool = False
    ) -> None:
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
        y, x = entry_pos
        if x < 0 or x >= width or y < 0 or y >= height:
            raise ValueError(f"Entry {entry_pos} outside the maze.")
        y, x = exit_pos
        if x < 0 or x >= width or y < 0 or y >= height:
            raise ValueError(f"Exit {exit_pos} outside the maze.")
        self.width = width
        self.height = height
        self.entry = entry_pos
        self.exit = exit_pos
        self.output_file = output_file
        self.perfect = perfect
        self.seed = seed
        if self.seed is not None:
            random.seed(self.seed)
        self.grid: list[list[Cell]] = []
        self.generate_maze()

    def generate_maze(self) -> None:
        self.build_grid()
        self.apply_logo()
        self.validate_logo_entry_exit()
        self.dfs()
        if not self.perfect:
            self.perfect_false()

    def build_grid(self) -> None:
        grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(Cell(y, x))
            grid.append(row)
        self.grid = grid

    def get_neighbors(self, cell: Cell) -> dict[str, Cell]:
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
        neighbors = self.get_neighbors(cell)
        unvisited_neighbors = {
            key: value for key, value in neighbors.items()
            if not neighbors[key].visited and not neighbors[key].is_logo
        }
        return unvisited_neighbors

    def set_walls(
        self, current_cell: Cell, next_cell: Cell, bool_var: bool
    ) -> None:
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
        margin = 2
        logo = logo_42
        logo_h = len(logo)
        logo_w = len(logo[0])
        logo_fits = (
            self.width >= logo_w + margin * 2
            and self.height >= logo_h + margin * 2
        )
        if not logo_fits:
            return
        start_x = int((self.width - logo_w) / 2)
        start_y = int((self.height - logo_h) / 2)
        for y in range(logo_h):
            for x in range(logo_w):
                if logo_42[y][x] == 1:
                    self.grid[start_y + y][start_x + x].is_logo = True

    def validate_logo_entry_exit(self) -> None:
        y, x = self.entry
        if self.grid[y][x].is_logo:
            raise ValueError("Entry can't be on logo")
        y, x = self.exit
        if self.grid[y][x].is_logo:
            raise ValueError("Exit can't be on logo")

    def dfs(self) -> None:
        stack = [self.grid[0][0]]
        while stack:
            current = stack[-1]
            current.visited = True
            neighbors = self.get_unvisited_neighbors(current)
            if neighbors:
                neighbor = random.choice(list(neighbors.values()))
                self.set_walls(current, neighbor, False)
                stack.append(neighbor)
            else:
                stack.pop()

    def is_3x3(self, cell: Cell) -> bool:
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
        for y in range(self.height - 2):
            for x in range(self.width - 2):
                if self.is_3x3(self.grid[y][x]):
                    return True
        return False

    def perfect_false(self) -> None:
        neighbors_with_wall = []
        for row in self.grid:
            for cell in row:
                for direction, neighbor in self.get_neighbors(cell).items():
                    if cell.is_logo or neighbor.is_logo:
                        continue
                    if direction in ('E', 'S') and cell.walls[direction]:
                        neighbors_with_wall.append((cell, neighbor))

        random.shuffle(neighbors_with_wall)
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
