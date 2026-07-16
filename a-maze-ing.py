import sys
import traceback
from src.config.parser import parse_config
from src.generator.maze_generator import MazeGenerator

# except Exception also sicherheitsnetz fuer unerwartete bugs, und traceback damit wir sehen was es ist weil Exception auch unsere coding Fehler handled und wir ohne traceback vielleicht nicht drauf kommen wuerden?
# noch hinzufuegen maybe: prints auf stderr statt stdout, und sys.exit() nach exception?



def convert_config_build_maze(config: dict[str, str]) -> None:
    width = int(config['width'])
    height = int(config['height'])

    x, y = config['entry'].replace('.', ',').split(",")
    entry_pos = int(x), int(y)
    x, y = config['exit'].replace('.', ',').split(",")
    exit_pos = int(x), int(y)
    perfect_val = config['perfect'].lower()

    if perfect_val == 'true':
        perfect_bool = True
    elif perfect_val == 'false':
        perfect_bool = False 
    else:
        raise ValueError(f"Invalid boolean expression for PERFECT: {config['perfect']}")

    if 'seed' in config:
        seed_value = int(config['seed'])
    else:
        seed_value = None
    return MazeGenerator (
        width=width,
        height=height,
        entry_pos=entry_pos,
        exit_pos=exit_pos,
        output_file=config['output_file'],
        perfect=perfect_bool,
        seed=seed_value
    )

def main() -> None:
    try:
        filename = "config.txt"
        config = parse_config(filename)
        maze = convert_config_build_maze(config)
        #cell = maze.grid[2][2]
        #maze.grid[2][3].visited = True
        #cell_visited = maze.grid[0][1]

        #neighbors = maze.is_neighbor(cell)
        #for key in neighbors:
            #print(f"{key}: {neighbors[key].y}, {neighbors[key].x}")

        #current_cell = maze.grid[2][2]
        #next_cell = maze.grid[2][3]
        #maze.remove_walls(current_cell, next_cell)
        #print(current_cell.walls)
        #print(next_cell.walls)

        #maze.grid[2][2].is_logo = True
        #maze.validate_logo_entry_exit()

        maze.dfs()
        for row in maze.grid:
            for cell in row:
                print(cell.x, cell.y, cell.visited)
        #cell1 = maze.grid[0][0]
        #cell2 = maze.grid[0][1]
        #print(f"{cell1.walls['E']}, {cell2.walls['W']}")




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
