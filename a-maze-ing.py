import sys
import traceback
from src.config.parser import parse_config
from src.generator.maze_generator import MazeGenerator

# except Exception also sicherheitsnetz fuer unerwartete bugs, und traceback damit wir sehen was es ist weil Exception auch unsere coding Fehler handled und wir ohne traceback vielleicht nicht drauf kommen wuerden?
# noch hinzufuegen maybe: prints auf stderr statt stdout, und sys.exit() nach exception?
def main() -> None:
    try:
        filename = "config.txt"
        config = parse_config(filename)
        maze = MazeGenerator(config)
        #cell = maze.grid[2][2]
        #maze.grid[2][3].visited = True
        #cell_visited = maze.grid[0][1]

        #neighbors = maze.is_neighbor(cell)
        #for key in neighbors:
            #print(f"{key}: {neighbors[key].y}, {neighbors[key].x}")

        current_cell = maze.grid[2][2]
        next_cell = maze.grid[2][3]
        maze.remove_walls(current_cell, next_cell)
        print(current_cell.walls)
        print(next_cell.walls)


    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
    except OSError as e:
        print(f"Error while accessing file '{filename}': {e}")
    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
