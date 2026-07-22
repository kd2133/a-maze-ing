import random
from src.generator.maze_generator import MazeGenerator, Cell


last_wall_color: str | None = None
last_logo_color: str | None = None

WALL_COLORS = [
    "\033[90m", "\033[30m", "\033[31m", "\033[33m",
    "\033[34m", "\033[35m",
]
LOGO_COLORS = [
    "\033[1;96m", "\033[1;92m", "\033[1;97m",
    "\033[1;93m", "\033[1;95m",
]

ENTRY_COLOR = "\033[1;31m"
EXIT_COLOR = "\033[1;32m"
PATH_COLOR = "\033[1;94m"

RESET = "\033[0m"
SPACE = "  "


def pick_color(color_list: list[str], last: str | None) -> str:
    choices = [color for color in color_list if color != last] or color_list
    return random.choice(choices)


def display(
        maze: MazeGenerator,
        path: bool = False,
        change_color: bool = False
        ) -> None:
    global last_wall_color, last_logo_color

    if change_color or last_wall_color is None or last_logo_color is None:
        last_wall_color = pick_color(WALL_COLORS, last_wall_color)
        last_logo_color = pick_color(LOGO_COLORS, last_logo_color)

    wall = f"{last_wall_color}██{RESET}"
    logo = f"{last_logo_color}██{RESET}"
    entry_cell = f"{ENTRY_COLOR}██{RESET}"
    exit_cell = f"{EXIT_COLOR}██{RESET}"
    path_cell = f"{PATH_COLOR}██{RESET}"

    def get_cell_type(cell: Cell) -> str:
        pos = (cell.y, cell.x)
        if pos == maze.entry:
            return entry_cell
        if pos == maze.exit:
            return exit_cell
        if path and cell.is_path:
            return path_cell
        if cell.is_logo:
            return logo
        return SPACE

    print(wall * (maze.width * 2 + 1))
    for row in maze.grid:
        line = wall
        for cell in row:
            line += get_cell_type(cell)
            line += wall if cell.walls['E'] else SPACE
        print(line)

        line = wall
        for cell in row:
            line += wall if cell.walls['S'] else SPACE
            line += wall
        print(line)
