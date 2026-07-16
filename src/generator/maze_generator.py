
logo_42 = [
    [1, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1],
    [0, 0, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1]
]

class Cell:
    def __init__(self, y: int, x: int) -> None:
        self.x = x
        self.y = y
        self.walls = {'N': True, 'E': True, 'S': True, 'W': True}
        self.visited = False
        self.is_logo = False

class MazeGenerator:
    def __init__(self, config: dict[str, str]):
        self.config = config
        self.grid = []
        self.build_grid()
        self.apply_logo()

    def generate(self) -> None:
        pass

    def build_grid(self) -> None:
        grid = []
        for y in range(self.config.height):
            row = []
            for x in range(self.config.width):
                new_cell = Cell(y, x)
                row.append(new_cell)
            grid.append(row)
        self.grid = grid

    def get_neighbors(self, cell: Cell) -> dict[str, Cell]:
        y = cell.y
        x = cell.x
        neighbors = {}

        if y > 0:
            neighbors['N'] = self.grid[y - 1][x]
        if x < self.config.width - 1:
            neighbors['E'] = self.grid[y][x + 1]
        if y < self.config.height - 1:
            neighbors['S'] = self.grid[y + 1][x]
        if x > 0:
            neighbors['W'] = self.grid[y][x - 1]
        return neighbors
    
    def get_unvisited_neighbors(self) -> dict[str, Cell]:
        neighbors = get_neighbors
        unvisited_neighbors = {key: value for key, value in neighbors.items() if not neighbors[key].visited and not neighbors[key].is_logo}
        return univisited_neighbors
    
    def remove_walls(self, current_cell: Cell, next_cell: Cell) -> None:
        if current_cell.y - 1 == next_cell.y:
            current_cell.walls['N'] = False
            next_cell.walls['S'] = False
        elif current_cell.x + 1 == next_cell.x:
            current_cell.walls['E'] = False
            next_cell.walls['W'] = False
        elif current_cell.y + 1 == next_cell.y:
            current_cell.walls['S'] = False
            next_cell.walls['N'] = False
        elif current_cell.x - 1 == next_cell.x:
            current_cell.walls['W'] = False
            next_cell.walls['E'] = False


    def apply_logo(self) -> None:
        margin = 2
        logo = logo_42
        logo_h = len(logo)
        logo_w = len(logo[0])
        logo_fits = (self.config.width >= logo_w + margin * 2 and
                    self.config.height >= logo_h + margin * 2)
        if not logo_fits:
            raise ValueError("Grid too small for logo!")
        start_x = int((self.config.width - logo_w) / 2)
        start_y = int((self.config.height - logo_h) / 2)
        for y in range(logo_h):
            for x in range(logo_w):
                if logo_42[y][x] == 1:
                    self.grid[start_y + y][start_x + x].is_logo = True
    
    def validate_logo_entry_exit(self) -> None:
        y, x = self.config.entry
        if self.grid[y][x].is_logo:
            raise ValueError(f"Entry can't be on logo")
        y, x = self.config.exit
        if self.grid[y][x].is_logo:
            raise ValueError(f"Exit can't be on logo")



    def print_grid(self) -> None:
        for row in self.grid:
            line = ""
            for cell in row:
                if cell.is_logo:
                    line += "@"
                else:
                    line += "#"
            print(line)
            
            


