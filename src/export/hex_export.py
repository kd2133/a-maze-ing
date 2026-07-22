from src.generator.maze_generator import MazeGenerator
from src.solver.maze_solver import bfs

def hex_export(maze: MazeGenerator, filename: str) -> None:
    if not filename:
        raise ValueError("No output file was passed.")
    try:
        path = bfs(maze)
        with open(filename, "w") as file:
            for row in maze.grid:
                line = ""
                for cell in row:
                    value = 0
                    if cell.walls['N']:
                        value += 1
                    if cell.walls['E']:
                        value += 2
                    if cell.walls['S']:
                        value += 4
                    if cell.walls['W']:
                        value += 8
                    line += f"{value:X}"
                file.write(line + "\n")

            y, x = maze.entry
            entry_pos = f"{y},{x}"
            file.write("\n" + entry_pos + "\n")
            y, x = maze.exit
            exit_pos = f"{y},{x}"
            file.write(exit_pos)
            file.write("\n")
            file.write("".join(path) + "\n")
    except OSError as e:
        raise OSError(f"Could not write hex output file: {e}")

if __name__ == "__main__":
    maze = MazeGenerator()
    hex_export() 