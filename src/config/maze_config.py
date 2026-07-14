from dataclasses import dataclass

# seed check hinzufuegen: wenn von user input, dann checken ob es zwischen 0 und max_int ist?, anonsten(also wenn seed=None), dann random zahl zwischen gegebenem Bereich
@dataclass
class MazeConfig():
    width: int
    height: int
    entry_pos: tuple[int, int]
    exit_pos: tuple[int, int]
    output_file: str
    seed: int | None
    perfect: bool = False

    def __post_init__(self):
        if self.width <= 0 or self.height <= 0:
            raise ValueError(f"Height/ Width must be higher than 0, height: {self.height}, width: {self.width}")
        if self.entry_pos == self.exit_pos:
            raise ValueError(f"Entry/ exit can't be equal, entry: {self.entry_pos}, exit: {self.exit_pos}")
        x, y = self.entry_pos
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise ValueError(f"Entry {self.entry_pos} outside the maze.") 
        x, y = self.exit_pos
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise ValueError(f"Exit {self.exit_pos} outside the maze.")
        
