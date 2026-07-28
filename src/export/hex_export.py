from src.mazegen import MazeGenerator
from src.mazegen import bfs


def hex_export(maze: MazeGenerator, filename: str) -> None:
    """Shows the cell's walls state using one hex-digit.

    Args:
        maze: MazeGenerator instance.
        filename: output_file filename.

    Raises:
        ValueError: If filename is None / empty.
        OSError: If open / write process fails.
    """
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

            file.write(f"\n{maze.entry[0]},{maze.entry[1]}\n")
            file.write(f"{maze.exit[0]},{maze.exit[1]}")
            file.write("\n")
            file.write("".join(path) + "\n")
    except OSError as e:
        raise OSError(f"Could not write hex output file: {e}")
