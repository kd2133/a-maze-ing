import random

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
    def __init__(self, width: int, height: int, entry_pos: tuple[int, int],
                 exit_pos: tuple[int, int], output_file: str, perfect: bool, seed: int | None) -> None:
        if width <= 0 or height <= 0:
            raise ValueError(f"Height/ Width must be higher than 0, height: {height}, width: {width}")
        if entry_pos == exit_pos:
            raise ValueError(f"Entry/ exit can't be equal, entry: {entry_pos}, exit: {exit_pos}")
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
        self.grid = []
        self.generate_maze()

    def generate_maze(self) -> None:
        self.build_grid()
        #self.apply_logo()
    
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
        unvisited_neighbors = {key: value for key, value in neighbors.items() if not neighbors[key].visited and not neighbors[key].is_logo}
        return unvisited_neighbors
    
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
        logo_fits = (self.width >= logo_w + margin * 2 and
                    self.height >= logo_h + margin * 2)
        if not logo_fits:
            raise ValueError("Grid too small for logo!")
        start_x = int((self.width - logo_w) / 2)
        start_y = int((self.height - logo_h) / 2)
        for y in range(logo_h):
            for x in range(logo_w):
                if logo_42[y][x] == 1:
                    self.grid[start_y + y][start_x + x].is_logo = True
    
    def validate_logo_entry_exit(self) -> None:
        y, x = self.entry
        if self.grid[y][x].is_logo:
            raise ValueError(f"Entry can't be on logo")
        y, x = self.exit
        if self.grid[y][x].is_logo:
            raise ValueError(f"Exit can't be on logo")

    def dfs(self) -> None:
        stack = [self.grid[0][0]]
        stack[0].visited = True
        while(stack):
            current = stack[-1]
            neighbors = self.get_unvisited_neighbors(current)
            print(f"y:{current.y}, x:{current.x}")
            if neighbors:
                neighbor = random.choice(list(neighbors.values()))
                self.remove_walls(current, neighbor)
                stack.append(neighbor)
                neighbor.visited = True
            else:
                print("backtrack")
                stack.pop()



    def print_grid(self) -> None:
        for row in self.grid:
            line = ""
            for cell in row:
                if cell.is_logo:
                    line += "@"
                else:
                    line += "#"
            print(line)
            
            


