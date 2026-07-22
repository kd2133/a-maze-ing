import sys
import traceback
import random
from src.config.parser import parse_config
from src.generator.maze_generator import MazeGenerator
from src.export.hex_export import hex_export
from src.ui.display import display


# except Exception also sicherheitsnetz fuer unerwartete bugs, und traceback damit wir sehen was es ist weil Exception auch unsere coding Fehler handled und wir ohne traceback vielleicht nicht drauf kommen wuerden?
# noch hinzufuegen maybe: prints auf stderr statt stdout, und sys.exit() nach exception?



def build_maze_convert_config(config: dict[str, str]) -> None:
    width = int(config['width'])
    height = int(config['height'])

    y, x = config['entry'].replace('.', ',').split(",")
    entry_pos = int(y), int(x)
    y, x = config['exit'].replace('.', ',').split(",")
    exit_pos = int(y), int(x)
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
        config = parse_config("config.txt")
        maze = build_maze_convert_config(config)
        hex_export(maze, maze.output_file)
        display(maze)
        while True:
            print("\n=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Quit")
            user_input = input("Choice? (1-4): ")
            if user_input == "1":
                config = parse_config("config.txt")
                maze = build_maze_convert_config(config)
                hex_export(maze, maze.output_file)
                display(maze)
            elif user_input == "2":
                print("Not available yet")
            elif user_input == "3":
                display(maze)
            elif user_input == "4":
                print("\nGoodbye!")
                break
            else:
                print("\nNot a valid choice! Try again!")






    except FileNotFoundError:
        print(f"Error: File not found")
    except OSError as e:
        print(f"Error while accessing file '{filename}': {e}")
    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")

if __name__ == "__main__":
    main()
