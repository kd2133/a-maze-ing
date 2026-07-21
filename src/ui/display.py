import random
from src.generator.maze_generator import MazeGenerator

last_wall_color = None
last_logo_color = None
WALL_COLORS = ["\033[90m", "\033[30m", "\033[31m", "\033[33m"]
LOGO_COLORS = ["\033[1;96m", "\033[1;92m", "\033[1;97m"]
RESET = "\033[0m"
SPACE = "  "

def display(maze: MazeGenerator) -> None:
    global last_wall_color, last_logo_color

    av_wall_colors = [color for color in WALL_COLORS if color != last_wall_color]
    av_logo_colors = [color for color in LOGO_COLORS if color != last_logo_color]
    wall_color = random.choice(av_wall_colors)
    logo_color = random.choice(av_logo_colors)
    last_wall_color = wall_color
    last_logo_color = logo_color
    wall = f"{wall_color}██{RESET}"
    logo = f"{logo_color}██{RESET}"

    print(wall * (maze.width * 2 + 1))
    for row in maze.grid:
        line = wall
        for cell in row:
            if cell.is_logo:
                line += logo
            else:
                line += SPACE
            if cell.walls['E']:
                line += wall
            else:
                line += SPACE
        print(line)

        line = wall
        for cell in row:
            if cell.walls['S']:
                line += wall
            else:
                line += SPACE
            line += wall
        print(line)
