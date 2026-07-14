
class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.walls = {'N': True, 'E': True, 'S': True, 'W': True}
        self.visited = False

# seed check hinzufuegen: wenn von user input, dann checken ob es zwischen 0 und max_int ist?, anonsten(also wenn seed=None), dann random zahl zwischen gegebenem Bereich
class MazeGenerator:
    def __init__(self, config: MazeConfig):
        self.config = config
        self.is_valid_config()
        self.grid = []
        self.build_grid()

    def build_grid(self) -> None:
        all_rows = []
        for y in range(self.config.height):
            row = []
            for x in range(self.config.width):
                new_cell = Cell(x, y)
                row.append(new_cell)
            all_rows.append(row)
        self.grid = all_rows
            


